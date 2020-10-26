# importing models from provider/models.py
from provider.models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo, \
                    SeriesRating, MovieRating, History, VideoComment

from provider.views import SUBCATEGORY_REVERSE
from django.db.models import Count, Avg, Sum
from datetime import datetime
from django.utils import timezone


# modules to import for classify the comment positivity or negativity
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews


def recommend_movies(request):
    # response to the function call , it returns an array of movie ids that are recommended for the user
    result = []

    # find all the video ids that are movie videos
    movies_video_ids = MovieVideo.objects.filter(date_of_release__lte=datetime.now(tz=timezone.utc)).values('video_id')
    # searching the user history to know which movies he/she had watched till now
    user_history_details = History.objects.filter(
        user_id=request.user,
        video_id__in=movies_video_ids
    )

    # if user has no history return empty
    if user_history_details is None:
        return result

    # searching the user history to know which movie videos he/she had watched till now
    user_video_id_history = History.objects.filter(
        user_id=request.user,
        video_id__in=movies_video_ids
    ).values('video_id')

    # movie ids of the movies user had watched
    movies_ids = MovieVideo.objects.filter(
        video_id__in=user_video_id_history,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('movie_id').distinct()

    # getting subcategories for the user watched movies
    movies_subcat_data = MovieSubCategories.objects.filter(movie_id__in=movies_ids)
    movies_subcat_dict = {}
    for obj in movies_ids:
        movies_subcat_dict.update({obj['movie_id']: []})

    for sub_cat in movies_subcat_data:
        movies_subcat_dict[sub_cat.movie_id.movie_id].append(sub_cat.sub_category)

    # getting movie video duration
    video_duration = MovieVideo.objects.filter(
        video_id__in=user_video_id_history,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('movie_id', 'video_id', 'duration_of_video').distinct()

    # getting movies_duration and relationship between movie_id and video_id
    movies_duration = {}
    movie_video_relation = {}
    for obj in video_duration:
        movies_duration[obj['video_id']] = obj['duration_of_video']
        movie_video_relation[obj['video_id']] = obj['movie_id']


    # counting the number of movies user had watched according to language
    language_values = {}
    language = MovieVideo.objects.filter(movie_id__in=movies_ids,date_of_release__lte=datetime.now(tz=timezone.utc)).values('movie_id__language').annotate(total=Count('movie_id__language'))
    for obj in language:
        language_values[obj['movie_id__language']] = obj['total']


    # finding the weight of each subcategory watched by user
    subcategories_values = {}
    for obj in user_history_details:
        original_length = movies_duration[obj.video_id.video_id]
        watch_time = obj.video_watched

        # finding fraction of video watched by user
        fraction = watch_time / original_length

        # calculating values/weight of each subcategory
        for sub_cat in movies_subcat_dict[movie_video_relation[obj.video_id.video_id]]:
            if sub_cat in subcategories_values.keys():
                subcategories_values[sub_cat] += fraction
            else:
                subcategories_values[sub_cat] = fraction

    # print(subcategories_values)


    # finding movies that are not watched by user
    not_watched_movies = MovieVideo.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).exclude(movie_id__in=movies_ids)

    not_watched_movies_ids = MovieVideo.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).exclude(movie_id__in=movies_ids).values('movie_id')

    # finding movies subcategories of those movies that are not watched by user
    not_watched_movies_subcategories = MovieSubCategories.objects.filter(
        movie_id__in=not_watched_movies_ids
    )
    movies_subcats = {}
    for m_id in not_watched_movies_ids:
        movies_subcats.update({m_id['movie_id']: []})

    for obj in not_watched_movies_subcategories:
        movies_subcats[obj.movie_id.movie_id].append(obj.sub_category)

    # calculating movie values based on subcategory
    movie_values = {}
    for obj in not_watched_movies:
        movie_values[obj.movie_id.movie_id] = 0
        for cat in movies_subcats[obj.movie_id.movie_id]:
            if cat in subcategories_values.keys():
                movie_values[obj.movie_id.movie_id] += subcategories_values[cat]

    # filtering out movies from resulting set
    for key in list(movie_values.keys()):
        if movie_values[key] == 0:
            movie_values.pop(key)

    # finding movie average rating
    movie_avg_rating = MovieRating.objects.filter(
        movie_id__in=list(movie_values.keys())
    ).values('movie_id__movie_id').annotate(avg_rating=Avg('rating'))

    # normalizing the movies that has no rating until now
    for key in movie_values.keys():
        movie_values[key] *= 2.5

    # calculating movie values based on average rating
    for obj in movie_avg_rating:
        movie_values[obj['movie_id__movie_id']] /= 2.5
        movie_values[obj['movie_id__movie_id']] *= obj['avg_rating']

    # calculating movie values based on language
    for obj in not_watched_movies:
        if obj.movie_id.movie_id in movie_values.keys():
            if obj.movie_id.language in language_values.keys():
                movie_values[obj.movie_id.movie_id] *= language_values[obj.movie_id.language]
            else:
                movie_values[obj.movie_id.movie_id] = 0

    # filtering out the result set
    for key in list(movie_values.keys()):
        if movie_values[key] == 0:
            movie_values.pop(key)

    # filtering out videos whose comments to be considered
    filtered_video_ids = MovieVideo.objects.filter(
        movie_id__in=list(movie_values.keys()),
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('video_id')

    # getting relationship between movie and video id
    mov_vid = MovieVideo.objects.filter(
        video_id__in=filtered_video_ids,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('movie_id', 'video_id').distinct()

    # finding relation between movie_id and video_id
    movie_video_relation = {}
    for obj in mov_vid:
        movie_video_relation[obj['video_id']] = obj['movie_id']

    # counting number of positive or negative comments on a movie
    positive_comments_count = {}
    negative_comments_count = {}
    for obj in list(movie_values.keys()):
        positive_comments_count.update({obj: 0})
        negative_comments_count.update({obj: 0})

    # fetching comments on all the required videos with counting positive and negative comment
    comments = VideoComment.objects.filter(video_id__in=filtered_video_ids).values('video_id', 'comment_type').annotate(count=Count('comment_type'))

    for obj in comments:
        if obj['comment_type'] == 1:
            positive_comments_count[movie_video_relation[obj['video_id']]] = obj['count']
        elif obj['comment_type'] == 2:
            negative_comments_count[movie_video_relation[obj['video_id']]] = obj['count']

    # using a naive bayes classifier to predict the positivity/negativity of a comment
    # for obj in comments:
    #     probdist = classifier.prob_classify(extract_features(obj.split()))
    #     pred_sentiment = probdist.max()
    #     if pred_sentiment == 'Positive' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
    #         positive_comments_count[movie_video_relation[obj.video_id.video_id]] += 1
    #     elif pred_sentiment == 'Negative' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
    #         negative_comments_count[movie_video_relation[obj.video_id.video_id]] += 1

    # updating the movie values based on comment positivity/negativity
    for key in movie_values.keys():
        pos = positive_comments_count[key]
        neg = negative_comments_count[key]

        if pos == 0 and neg == 0:
            movie_values[key] *= 0.5
        else:
            movie_values[key] *= (pos/(pos+neg))

    # print(movie_values)
    # sorting the movies based on their movie values in descending order
    movie_values = {k: v for k, v in sorted(movie_values.items(), key=lambda item: item[1], reverse=True)}
    result = list(movie_values.keys())
    # returning result
    return result



def recommend_series(request):
    # response to the function call, it returns an array of series ids that are recommended for the user
    result = []

    # find all the video ids that are series videos
    series_video_ids = SeriesVideos.objects.filter(date_of_release__lte=datetime.now(tz=timezone.utc)).values('video_id')
    # searching the user history to know which series he/she had watched till now
    user_history_details = History.objects.filter(
        user_id=request.user,
        video_id__in=series_video_ids
    )

    # if user has no history return empty
    if user_history_details is None:
        return result

    # searching the user history to know which series videos he/she had watched till now
    user_video_id_history = History.objects.filter(
        user_id=request.user,
        video_id__in=series_video_ids
    ).values('video_id')

    # series ids of the series of which user had watched some episode
    series_ids = SeriesVideos.objects.filter(
        video_id__in=user_video_id_history,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id').distinct()

    # getting subcategories for the user watched series
    series_subcat_data = SeriesSubCategories.objects.filter(series_id__in=series_ids)
    series_subcat_dict = {}
    for obj in series_ids:
        series_subcat_dict.update({obj['series_season_id__series_id']: []})

    for sub_cat in series_subcat_data:
        series_subcat_dict[sub_cat.series_id.series_id].append(sub_cat.sub_category)

    # getting series full videos duration
    series_duration = SeriesVideos.objects.filter(
        series_season_id__series_id__in=series_ids,
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id').annotate(duration=Sum('duration_of_video'))

    original_series_length = {}
    for obj in series_duration:
        original_series_length.update({obj['series_season_id__series_id']: obj['duration']})

    # establishing relationship between video_id and series_id
    relationship = SeriesVideos.objects.filter(
        video_id__in=user_video_id_history,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id', 'video_id')

    series_video_relation = {}
    for obj in relationship:
        series_video_relation[obj['video_id']] = obj['series_season_id__series_id']


    # getting series videos duration watched by the user
    series_duration_watched = {}
    for obj in series_ids:
        series_duration_watched.update({obj['series_season_id__series_id']: 0})

    for obj in user_history_details:
        series_duration_watched[series_video_relation[obj.video_id.video_id]] += obj.video_watched


    # counting the number of series user had watched according to language
    language_values = {}
    language = SeriesDetails.objects.filter(series_id__in=series_ids).values('language').annotate(total=Count('language'))
    for obj in language:
        language_values[obj['language']] = obj['total']


    # finding the weight of each subcategory watched by user
    subcategories_values = {}
    for obj in series_ids:
        original_length = original_series_length[obj['series_season_id__series_id']]
        watch_time = series_duration_watched[obj['series_season_id__series_id']]

        # finding fraction of video watched by user
        fraction = watch_time / original_length

        for sub_cat in series_subcat_dict[obj['series_season_id__series_id']]:
            if sub_cat in subcategories_values.keys():
                subcategories_values[sub_cat] += fraction
            else:
                subcategories_values[sub_cat] = fraction

    # print(subcategories_values)

    # fetching all the series that are not watched by the user
    not_watched_series_ids = SeriesVideos.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id').distinct().exclude(series_season_id__series_id__in=series_ids)

    # fetching series details of the series that are not atched by the user
    not_watched_series = SeriesDetails.objects.filter(
        series_id__in=not_watched_series_ids
    )

    # fetching subcategory details of the series that are not watched by the user
    not_watched_series_subcategories = SeriesSubCategories.objects.filter(
        series_id__in=not_watched_series_ids
    )
    series_subcats = {}
    for s_id in not_watched_series_ids:
        series_subcats.update({s_id['series_season_id__series_id']: []})

    for obj in not_watched_series_subcategories:
        series_subcats[obj.series_id.series_id].append(obj.sub_category)

    # initializing series values based on series subcategories
    series_values = {}
    for obj in not_watched_series_ids:
        series_values[obj['series_season_id__series_id']] = 0
        for cat in series_subcats[obj['series_season_id__series_id']]:
            if cat in subcategories_values.keys():
                series_values[obj['series_season_id__series_id']] += subcategories_values[cat]

    # print(series_values)
    # filtering out the result set
    for key in list(series_values.keys()):
        if series_values[key] == 0:
            series_values.pop(key)

    # finding series average rating
    series_avg_rating = SeriesRating.objects.filter(
        series_id__in=list(series_values.keys())
    ).values('series_id__series_id').annotate(avg_rating=Avg('rating'))

    # normalizing those series that have no rating until now
    for key in series_values.keys():
        series_values[key] *= 2.5

    # updating series values based on average series rating
    for obj in series_avg_rating:
        series_values[obj['series_id__series_id']] /= 2.5
        series_values[obj['series_id__series_id']] *= obj['avg_rating']
    # print(series_values)

    # considering the language factor and updating the series values
    for obj in not_watched_series:
        if obj.series_id in series_values.keys():
            if obj.language in language_values.keys():
                series_values[obj.series_id] *= language_values[obj.language]
            else:
                series_values[obj.series_id] = 0

    # filtering out the result set
    for key in list(series_values.keys()):
        if series_values[key] == 0:
            series_values.pop(key)

    # print(series_values)
    # considering comments on videos based on their positivity or negativity
    filtered_video_ids = SeriesVideos.objects.filter(
        series_season_id__series_id__in=list(series_values.keys()),
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('video_id')

    # establishing relationship between video_id and series_id
    relationship = SeriesVideos.objects.filter(
        video_id__in=filtered_video_ids,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id', 'video_id')

    series_video_relation = {}
    for obj in relationship:
        series_video_relation[obj['video_id']] = obj['series_season_id__series_id']

    # fetching comments on all videos that are to be included
    # comments = VideoComment.objects.filter(video_id__in=filtered_video_ids)

    # count number of positive and negative comments on the series
    positive_comments_count = {}
    negative_comments_count = {}
    for obj in list(series_values.keys()):
        positive_comments_count.update({obj: 0})
        negative_comments_count.update({obj: 0})

    # fetching comments on all the required videos with counting positive and negative comment
    comments = VideoComment.objects.filter(video_id__in=filtered_video_ids).values('video_id', 'comment_type').annotate(count=Count('comment_type'))

    for obj in comments:
        if obj['comment_type'] == 1:
            positive_comments_count[series_video_relation[obj['video_id']]] += obj['count']
        elif obj['comment_type'] == 2:
            negative_comments_count[series_video_relation[obj['video_id']]] += obj['count']


    # predicting comment positivity/negativity using a naive bayes classifier of nltk module
    # for obj in comments:
    #     probdist = classifier.prob_classify(extract_features(obj.split()))
    #     pred_sentiment = probdist.max()
    #     if pred_sentiment == 'Positive' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
    #         positive_comments_count[series_video_relation[obj.video_id.video_id]] += 1
    #     elif pred_sentiment == 'Negative' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
    #         negative_comments_count[series_video_relation[obj.video_id.video_id]] += 1

    # updating series values based on comments count
    for key in series_values.keys():
        pos = positive_comments_count[key]
        neg = negative_comments_count[key]

        if pos == 0 and neg == 0:
            series_values[key] *= 0.5
        else:
            series_values[key] *= (pos/(pos+neg))

    # print(series_values)
    # sorting out the series based on their series values
    series_values = {k: v for k, v in sorted(series_values.items(), key=lambda item: item[1], reverse=True)}
    result = list(series_values.keys())
    # returning result
    return result



def recent_movies_suggestion(request):
    # response to the function call, it returns an array of movie ids that are recently uploadeed
    result = []
    movie_ids = MovieVideo.objects.filter(verification_status=2, date_of_release__lte=datetime.now(tz=timezone.utc)).order_by('-date_of_release').values('movie_id__movie_id')
    for obj in movie_ids:
        result.append(obj['movie_id__movie_id'])
    return result


def recent_series_suggestion(request):
    # response to the function call, it returns an array of series ids that are recently uploadeed
    result = []
    series_ids = SeriesVideos.objects.filter(verification_status=2, date_of_release__lte=datetime.now(tz=timezone.utc)).order_by('-date_of_release').values('series_season_id__series_id').distinct()
    for obj in series_ids:
        result.append(obj['series_season_id__series_id'])
    # print(result)
    return result


def popular_movies_suggestion(request):
    # response to the function call, it returns an array of movie ids that are recently uploadeed
    result = []

    movie_values = {}
    all_movie_ids = MovieVideo.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('movie_id')

    # initializing all movie value as 2.5 (average rating)
    for obj in all_movie_ids:
        movie_values.update({obj['movie_id']: 2.5})

    # finding movie average rating
    movie_avg_rating = MovieRating.objects.all().values('movie_id__movie_id').annotate(avg_rating=Avg('rating'))

    # calculating movie values based on average rating
    for obj in movie_avg_rating:
        movie_values[obj['movie_id__movie_id']] = obj['avg_rating']

    # print(movie_values)

    # filtering out videos whose comments to be considered
    filtered_video_ids = MovieVideo.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('video_id')

    # getting relationship between movie and video id
    mov_vid = MovieVideo.objects.filter(
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('movie_id', 'video_id').distinct()

    # finding relation between movie_id and video_id
    movie_video_relation = {}
    for obj in mov_vid:
        movie_video_relation[obj['video_id']] = obj['movie_id']

    # counting number of positive or negative comments on a movie
    positive_comments_count = {}
    negative_comments_count = {}
    for obj in list(movie_values.keys()):
        positive_comments_count.update({obj: 0})
        negative_comments_count.update({obj: 0})

    # fetching comments on all the required videos with counting positive and negative comment
    comments = VideoComment.objects.filter(video_id__in=filtered_video_ids).values('video_id', 'comment_type').annotate(count=Count('comment_type'))

    for obj in comments:
        if obj['comment_type'] == 1:
            positive_comments_count[movie_video_relation[obj['video_id']]] = obj['count']
        elif obj['comment_type'] == 2:
            negative_comments_count[movie_video_relation[obj['video_id']]] = obj['count']


    # updating the movie values based on comment positivity/negativity
    for key in movie_values.keys():
        pos = positive_comments_count[key]
        neg = negative_comments_count[key]

        if pos == 0 and neg == 0:
            movie_values[key] *= 0.5
        else:
            movie_values[key] *= (pos/(pos+neg))

    # print(movie_values)
    # sorting the movies based on their movie values in descending order
    movie_values = {k: v for k, v in sorted(movie_values.items(), key=lambda item: item[1], reverse=True)}
    result = list(movie_values.keys())
    # print(result)
    # returning result
    return result



def popular_series_suggestion(request):
    # response to the function call, it returns an array of series ids that are recently uploadeed
    result = []

    series_values = {}
    all_series_ids = SeriesVideos.objects.filter(verification_status=2, date_of_release__lte=datetime.now(tz=timezone.utc)).values('series_season_id__series_id').distinct()


    # initializing all series value as 2.5 (average rating)
    for obj in all_series_ids:
        series_values.update({obj['series_season_id__series_id']: 2.5})

    # finding series average rating
    series_avg_rating = SeriesRating.objects.all().values('series_id__series_id').annotate(avg_rating=Avg('rating'))

    # calculating series values based on average rating
    for obj in series_avg_rating:
        series_values[obj['series_id__series_id']] = obj['avg_rating']

    # print(series_values)

    # filtering out videos whose comments to be considered
    filtered_video_ids = SeriesVideos.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('video_id')

    # getting relationship between series_id and video id
    ser_vid = SeriesVideos.objects.filter(
        verification_status=2,
        date_of_release__lte=datetime.now(tz=timezone.utc)
    ).values('series_season_id__series_id', 'video_id').distinct()

    # finding relation between series_id and video_id
    series_video_relation = {}
    for obj in ser_vid:
        series_video_relation[obj['video_id']] = obj['series_season_id__series_id']

    # counting number of positive or negative comments on a series
    positive_comments_count = {}
    negative_comments_count = {}
    for obj in list(series_values.keys()):
        positive_comments_count.update({obj: 0})
        negative_comments_count.update({obj: 0})

    # fetching comments on all the required videos with counting positive and negative comment
    comments = VideoComment.objects.filter(video_id__in=filtered_video_ids).values('video_id', 'comment_type').annotate(count=Count('comment_type'))

    for obj in comments:
        if obj['comment_type'] == 1:
            positive_comments_count[series_video_relation[obj['video_id']]] += obj['count']
        elif obj['comment_type'] == 2:
            negative_comments_count[series_video_relation[obj['video_id']]] += obj['count']


    # updating the series values based on comment positivity/negativity
    for key in series_values.keys():
        pos = positive_comments_count[key]
        neg = negative_comments_count[key]

        if pos == 0 and neg == 0:
            series_values[key] *= 0.5
        else:
            series_values[key] *= (pos/(pos+neg))

    # print(series_values)
    # sorting the movies based on their movie values in descending order
    series_values = {k: v for k, v in sorted(series_values.items(), key=lambda item: item[1], reverse=True)}
    result = list(series_values.keys())
    # print(result)
    # returning result
    return result



def extract_features(word_list):
    return dict([(word, True) for word in word_list])


def train_comment_judging_classifier():
    # Load positive and negative reviews
    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')
    features_positive = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]

    # Split the data into train and test (80/20)
    threshold_factor = 0.8
    threshold_positive = int(threshold_factor * len(features_positive))
    threshold_negative = int(threshold_factor * len(features_negative))
    features_train = features_positive[:threshold_positive]+features_negative[:threshold_negative]
    features_test = features_positive[threshold_positive:]+features_negative[threshold_negative:]

    # print("Number of training datapoints: ", len(features_train))
    # print("Number of test datapoints: ", len(features_test))

    classifier = NaiveBayesClassifier.train(features_train)
    # print("Accuracy of the classifier: ", nltk.classify.util.accuracy(classifier, features_test))

    return classifier



classifier = train_comment_judging_classifier()
#Sample input reviews
# input_reviews = [
#     "Started off as the greatest series of all time, but had the worst ending of all time.",
#     "Exquisite. 'Big Little Lies' takes us to an incredible journey with its emotional and intriguing storyline.",
#     "I love Brooklyn 99 so much. It has the best crew ever!!",
#     "The Big Bang Theory and to me it's one of the best written sitcoms currently on network TV.",
#     "'Friends' is simply the best series ever aired. The acting is amazing.",
#     "SUITS is smart, sassy, clever, sophisticated, timely and immensely entertaining!",
#     "Cumberbatch is a fantastic choice for Sherlock Holmes-he is physically right (he fits the traditional reading of the character) and he is a damn good actor",
#     "What sounds like a typical agent hunting serial killer, surprises with great characters, surprising turning points and amazing cast."
#     "This is one of the most magical things I have ever had the fortune of viewing.",
#     "I don't recommend watching this at all!"
# ]
# print("Predictions: ")

# for review in input_reviews:
#     print("\nReview:", review)
#     probdist = classifier.prob_classify(extract_features(review.split()))
#     pred_sentiment = probdist.max()
#     print("Predicted sentiment: ", pred_sentiment)
#     print("Probability: ", round(probdist.prob(pred_sentiment), 2))