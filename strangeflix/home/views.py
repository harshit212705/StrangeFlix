# importing models from provider/models.py
from provider.models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo, MovieRating, \
                    SeriesRating, VideoComment, VideoRejectionComment, ReportComment, ReportVideo, \
                    Favourites, History

# importing required models from different apps
from .models import PayPerViewTransaction
from accounts.models import UserDetails
from subscribe.models import Subscriptions

# importing django modules needed
from django.shortcuts import render, redirect
from django.views.generic import View
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta, timezone
import os
import json
import uuid
import urllib.request
import hashlib
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import re
import os
import itertools
import mimetypes

# importing modules to Stream video to user
import base64
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import requests
from django.views.decorators.http import condition

# modules to import for classify the comment positivity or negativity
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

# importing other functions or variables from other files
from .recommendations import recommend_movies, recommend_series, recent_movies_suggestion, \
    recent_series_suggestion, popular_movies_suggestion, popular_series_suggestion
from provider.views import LANGUAGE_REVERSE, SUBCATEGORY_REVERSE, CATEGORY_REVERSE, VERIFICATION_REVERSE, \
                            VIDEO_EXTENSION_REVERSE, VIDEO_QUALITY_REVERSE, VIDEO_TYPE_REVERSE, \
                            VIDEO_BASE_FILEPATH, storage, SUBCATEGORY



# function to render the mainpage or homepage
class HomeView(View):
    def get(self, request):

        registration_form = CustomUserCreationForm()
        login_form = AuthenticationForm()
        is_subscribed = False
        context = {
            'registration_form': registration_form,
            'login_form': login_form,
            'is_subscribed': is_subscribed,
            'recommended_movies': '',
            'recommended_series': '',
            'recent_movies': '',
            'recent_series': '',
            'popular_movies': '',
            'popular_series':  '',
        }
        if request.user.is_authenticated:
            # checking logged in user subscription plan details
            subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
            if subscribe:
                is_subscribed = True
            else:
                is_subscribed = False
            context['is_subscribed'] = is_subscribed

            # fetching recommended movies for logged in user
            movies_ids = recommend_movies(request)
            if len(movies_ids) != 0:
                # fetching movie details in the same order as received from recommend_movies function
                clauses = ' '.join(['WHEN movie_id=%s THEN %s' % (pk, i) for i, pk in enumerate(movies_ids)])
                ordering = 'CASE %s END' % clauses
                movies_data = MovieDetails.objects.filter(movie_id__in=movies_ids).extra(
                        select={'ordering': ordering}, order_by=('ordering',))[:24]

                all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=movies_ids)

                # fetching all subcategories for the movies that are to be included
                subcategory_data = {}
                for obj in movies_ids:
                    subcategory_data.update({obj: []})

                for sub_cat in all_subcategory_data:
                    subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

                recommended_movies = {}
                for obj in movies_data:
                    recommended_movies.update({str(obj.pk): (obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), 'Entertainment', obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

                # returning recommended movies
                context['recommended_movies'] = recommended_movies


            # fetching recommended series for logged in user
            series_ids = recommend_series(request)
            if len(series_ids) != 0:
                # fetching series details in the same order as received from recommend_series function
                clauses = ' '.join(['WHEN series_id=%s THEN %s' % (pk, i) for i, pk in enumerate(series_ids)])
                ordering = 'CASE %s END' % clauses
                series_data = SeriesDetails.objects.filter(series_id__in=series_ids).extra(
                        select={'ordering': ordering}, order_by=('ordering',))[:24]

                all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=series_ids)

                # fetching all subcategories for the series that are to be included
                subcategory_data = {}
                for obj in series_ids:
                    subcategory_data.update({obj: []})

                for sub_cat in all_subcategory_data:
                    subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

                recommended_series = {}
                for obj in series_data:
                    recommended_series.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

                # returning recommended series
                context['recommended_series'] = recommended_series


        # fetching recent movies for everyone
        recent_movies_ids = recent_movies_suggestion(request)
        if len(recent_movies_ids) != 0:
            # fetching movie details in the same order as received from recent_movies function
            clauses = ' '.join(['WHEN movie_id=%s THEN %s' % (pk, i) for i, pk in enumerate(recent_movies_ids)])
            ordering = 'CASE %s END' % clauses
            movies_data = MovieDetails.objects.filter(movie_id__in=recent_movies_ids).extra(
                    select={'ordering': ordering}, order_by=('ordering',))[:24]

            all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=recent_movies_ids)

            # fetching all subcategories for the movies that are to be included
            subcategory_data = {}
            for obj in recent_movies_ids:
                subcategory_data.update({obj: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            recent_movies = {}
            for obj in movies_data:
                recent_movies.update({str(obj.pk): (obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), 'Entertainment', obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

            # returning recent movies
            context['recent_movies'] = recent_movies


        # fetching recent series for everyone
        recent_series_ids = recent_series_suggestion(request)
        if len(recent_series_ids) != 0:
            # fetching series details in the same order as received from recent_series function
            clauses = ' '.join(['WHEN series_id=%s THEN %s' % (pk, i) for i, pk in enumerate(recent_series_ids)])
            ordering = 'CASE %s END' % clauses
            series_data = SeriesDetails.objects.filter(series_id__in=recent_series_ids).extra(
                    select={'ordering': ordering}, order_by=('ordering',))[:24]

            all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=recent_series_ids)

            # fetching all subcategories for the series that are to be included
            subcategory_data = {}
            for obj in recent_series_ids:
                subcategory_data.update({obj: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            recent_series = {}
            for obj in series_data:
                recent_series.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

            # returning recent series
            context['recent_series'] = recent_series


        # fetching popular movies for everyone
        popular_movies_ids = popular_movies_suggestion(request)
        if len(popular_movies_ids) != 0:
            # fetching movie details in the same order as received from popular_movies_suggestion function
            clauses = ' '.join(['WHEN movie_id=%s THEN %s' % (pk, i) for i, pk in enumerate(popular_movies_ids)])
            ordering = 'CASE %s END' % clauses
            movies_data = MovieDetails.objects.filter(movie_id__in=popular_movies_ids).extra(
                    select={'ordering': ordering}, order_by=('ordering',))[:24]

            all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=popular_movies_ids)

            # fetching all subcategories for the movies that are to be included
            subcategory_data = {}
            for obj in popular_movies_ids:
                subcategory_data.update({obj: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            popular_movies = {}
            for obj in movies_data:
                popular_movies.update({str(obj.pk): (obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), 'Entertainment', obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

            # returning popular movies
            context['popular_movies'] = popular_movies


        # fetching popular series for everyone
        popular_series_ids = popular_series_suggestion(request)
        if len(popular_series_ids) != 0:
            # fetching series details in the same order as received from popular_series_suggestion function
            clauses = ' '.join(['WHEN series_id=%s THEN %s' % (pk, i) for i, pk in enumerate(popular_series_ids)])
            ordering = 'CASE %s END' % clauses
            series_data = SeriesDetails.objects.filter(series_id__in=popular_series_ids).extra(
                    select={'ordering': ordering}, order_by=('ordering',))[:24]

            all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=popular_series_ids)

            # fetching all subcategories for the series that are to be included
            subcategory_data = {}
            for obj in popular_series_ids:
                subcategory_data.update({obj: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            popular_series = {}
            for obj in series_data:
                popular_series.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

            # returning popular series
            context['popular_series'] = popular_series

        return render(request, 'home/index.html', context)



# returning movie details info to ajax request
@csrf_exempt
def get_movie_details(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        movie_id = json_data['movie_id']

        # response object to return as response to ajax request
        context = {
            'is_movie_exists': '',
            'is_successful': '',
            'movie_content_data': '',
            'movie_free_data': '',
        }

        # checking if movie exists
        movie_details = MovieDetails.objects.filter(movie_id=movie_id).first()
        if movie_details is None:
            context['is_movie_exists'] = 'This movie do not exists'
        else:
            # fetching movie video details for the movie
            movie_video_id = MovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')
            all_tags_data = MovieVideoTags.objects.filter(video_id__in=movie_video_id)

            all_subcategory_data = MovieSubCategories.objects.filter(movie_id=movie_id)

            # fetching all subcategories for the movies that is to be included
            subcategory_data = {}
            subcategory_data.update({int(movie_id): []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # fetching comments data for the movie
            all_comments_data = VideoComment.objects.filter(video_id__in=movie_video_id).order_by('timestamp')

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            comments_data = {}
            for obj in movie_video_id:
                tags_data.update({obj['video_id']: []})
                comments_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            for comment in all_comments_data:
                comments_data[comment.video_id.video_id].append([comment.user_id.username, comment.comment, comment.comment_id])

            # fetching movie video details
            movie_video_details = MovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            )

            movie_content_data = {}
            movie_language = str(LANGUAGE_REVERSE[movie_details.language]).title()
            for obj in movie_video_details:

                movie_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, 'Entertainment', obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id], subcategory_data[int(movie_id)], movie_language, obj.cost_of_video, comments_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_content_data'] = movie_content_data

            # fetching movie free content details for the movie
            movie_video_id = FreeMovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')

            # fetching tags and comments data
            all_tags_data = FreeMovieVideoTags.objects.filter(video_id__in=movie_video_id)
            all_comments_data = VideoComment.objects.filter(video_id__in=movie_video_id).order_by('timestamp')

            # fetching all tags for the free content that are to be included
            tags_data = {}
            comments_data = {}
            for obj in movie_video_id:
                tags_data.update({obj['video_id']: []})
                comments_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            for comment in all_comments_data:
                comments_data[comment.video_id.video_id].append([comment.user_id.username, comment.comment, comment.comment_id])

            # fetching movie free content details
            movie_video_details = FreeMovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('-date_of_release')

            movie_free_data = {}
            for obj in movie_video_details:

                movie_free_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, 'Entertainment', obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id],
                subcategory_data[int(movie_id)], movie_language, 0, comments_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_free_data'] = movie_free_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning series details info to ajax request
@csrf_exempt
def get_series_details(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']

        # response object to return as response to ajax request
        context = {
            'is_series_exists': '',
            'is_successful': '',
            'series_content_data': '',
            'series_season_data': '',
        }

        # checking if series exists
        series_details = SeriesDetails.objects.filter(series_id=series_id)
        if series_details is None:
            context['is_series_exists'] = 'This series do not exists'
        else:
            # fetching series details for the series

            all_subcategory_data = SeriesSubCategories.objects.filter(series_id=series_id)

            # fetching all subcategories for the series that is to be included
            subcategory_data = {}
            subcategory_data.update({int(series_id): []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            series_content_data = {}
            for obj in series_details:
                series_language = obj.language
                series_category = str(CATEGORY_REVERSE[obj.category]).title()
                series_content_data.update({str(obj.series_id): (obj.series_name, obj.description, obj.language, str(CATEGORY_REVERSE[obj.category]).title(), obj.thumbnail_image.url, subcategory_data[int(series_id)])})

            # returning success response to ajax request
            context['series_content_data'] = series_content_data

            # fetching series season details for the series
            series_season_id = SeriesVideos.objects.filter(
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
                series_season_id__series_id=series_id,
            ).values('series_season_id__series_season_id').distinct().union(
                FreeSeriesVideos.objects.filter(
                    verification_status=2,
                    date_of_release__lte=datetime.now(tz=timezone.utc),
                    series_season_id__series_id=series_id,
                ).values('series_season_id__series_season_id').distinct()
            )
            # fetching series season details that need to be included
            series_seasons_details = SeriesSeasonDetails.objects.filter(series_season_id__in=series_season_id).order_by('season_no')

            series_season_data = {}
            for obj in series_seasons_details:

                series_season_data.update({str(obj.series_season_id): (obj.series_id.series_id, obj.season_no, obj.description, series_language, series_category, obj.thumbnail_image.url, subcategory_data[int(series_id)])})

            # returning success response to ajax request
            context['series_season_data'] = series_season_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# returning season details info to ajax request
@csrf_exempt
def get_season_details(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_season_id = json_data['series_season_id']

        # response object to return as response to ajax request
        context = {
            'is_season_exists': '',
            'is_successful': '',
            'season_content_data': '',
            'season_free_data': '',
            'season_episodes': '',
        }

        # checking if season exists
        season_details = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id)
        if season_details is None:
            context['is_season_exists'] = 'This season do not exists'
        else:
            # fetching season details for the series
            all_subcategory_data = SeriesSubCategories.objects.filter(series_id=season_details[0].series_id)

            # fetching all subcategories for the series season that is to be included
            subcategory_data = {}
            subcategory_data.update({int(season_details[0].series_id.series_id): []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            season_content_data = {}
            for obj in season_details:
                series_language = obj.series_id.language
                series_category = str(CATEGORY_REVERSE[obj.series_id.category]).title()
                season_content_data.update({str(obj.series_season_id): (obj.season_no, obj.description, series_language, series_category, obj.thumbnail_image.url, subcategory_data[int(season_details[0].series_id.series_id)])})

            # returning success response to ajax request
            context['season_content_data'] = season_content_data

            # fetching season free content details
            series_video_id = FreeSeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')

            # fetching tags and comments data
            all_tags_data = FreeSeriesVideosTags.objects.filter(video_id__in=series_video_id)
            all_comments_data = VideoComment.objects.filter(video_id__in=series_video_id).order_by('timestamp')

            # fetching all tags for the free content that are to be included
            tags_data = {}
            comments_data = {}
            for obj in series_video_id:
                tags_data.update({obj['video_id']: []})
                comments_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            for comment in all_comments_data:
                comments_data[comment.video_id.video_id].append([comment.user_id.username, comment.comment, comment.comment_id])

            # fetching series free content details
            series_video_details = FreeSeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('-date_of_release')

            season_free_data = {}
            series_category = str(CATEGORY_REVERSE[season_details[0].series_id.category]).title()
            series_language = str(LANGUAGE_REVERSE[season_details[0].series_id.language]).title()
            for obj in series_video_details:

                season_free_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, subcategory_data[int(season_details[0].series_id.series_id)], obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id], 0, series_category, series_language, comments_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_free_data'] = season_free_data


            # fetching season episodes details
            series_video_id = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')

            # fetching tags and comments data
            all_tags_data = SeriesVideosTags.objects.filter(video_id__in=series_video_id)
            all_comments_data = VideoComment.objects.filter(video_id__in=series_video_id).order_by('timestamp')

            # fetching all tags, comments and locking info for the episodes that are to be included
            tags_data = {}
            comments_data = {}
            is_video_locked = {}
            for obj in series_video_id:
                tags_data.update({obj['video_id']: []})
                comments_data.update({obj['video_id']: []})
                is_video_locked.update({obj['video_id']: 0})
            if request.user.is_authenticated and  request.user.user_type == 'U':
                # checking logged in user subscription plan details
                subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()

                # calculating locking info here using subscription and pay per piew
                curr_time = datetime.today() - timedelta(days=1)
                get_pay_per_view_videos = PayPerViewTransaction.objects.filter(
                    user_id=request.user,
                    video_id__in=series_video_id,
                    transaction_start_time__gt=curr_time,
                ).values('video_id')

                videos_with_pay_per_view = {}
                for vid in get_pay_per_view_videos:
                    videos_with_pay_per_view.update({vid['video_id']: 1})

                for v_id in is_video_locked.keys():
                    if subscribe or (v_id in videos_with_pay_per_view.keys()):
                        is_video_locked[v_id] = 1
                    else:
                        is_video_locked[v_id] = 0

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            for comment in all_comments_data:
                comments_data[comment.video_id.video_id].append([comment.user_id.username, comment.comment, comment.comment_id])

            # fetching series episodes details
            series_video_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('episode_no')

            # finding max episode number available
            max_episode_no = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('episode_no').order_by('-episode_no')[0]
            max_episode_no = max_episode_no['episode_no']

            # adding episodes info to response
            season_episodes = {}
            for obj in series_video_details:
                season_episodes.update({int(obj.episode_no): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, subcategory_data[int(season_details[0].series_id.series_id)], obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id], obj.cost_of_video, series_category, series_language, comments_data[obj.video_id.video_id], is_video_locked[obj.video_id.video_id])})

            # adding missing episodes data as dummy data
            for i in range(max_episode_no):
                if i+1 not in season_episodes.keys():
                    season_episodes.update({int(i+1): (-1, 'Not Available', 'Not Available', '', subcategory_data[int(season_details[0].series_id.series_id)], '', '', str(VERIFICATION_REVERSE[3]).title(), [], 0, series_category, series_language, [], 0)})

            # sorting episodes on episode number basis
            season_episodes = {k: v for k, v in sorted(season_episodes.items(), key=lambda item: item[0])}

            # returning success response to ajax request
            context['season_episodes'] = season_episodes

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to handle when user wants to rate a movie
@csrf_exempt
def rate_movie(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        movie_id = json_data['movie_id']
        rating = json_data['movie_rating']

        # response object to return as response to ajax request
        context = {
            'is_movie_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if movie exists
        movie_details = MovieDetails.objects.filter(movie_id=movie_id).first()
        if movie_details is None:
            context['is_movie_exists'] = 'This movie do not exists'
        else:
            # checking if user is authenticated to do so or not
            if request.user.is_authenticated and request.user.user_type == 'U':
                # checking if user has already rated a movie just update it
                rated = MovieRating.objects.filter(user_id=request.user, movie_id=movie_details).first()
                if rated:
                    rated.rating = rating
                    rated.save()
                else:
                    rate = MovieRating.objects.create(
                        movie_id=movie_details,
                        user_id=request.user,
                        rating=rating,
                    )
                    rate.save()
                context['is_successful'] = 'Your rating for the movie is recorded.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to rate series by user
@csrf_exempt
def rate_series(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']
        rating = json_data['series_rating']

        # response object to return as response to ajax request
        context = {
            'is_series_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if series exists
        series_details = SeriesDetails.objects.filter(series_id=series_id).first()
        if series_details is None:
            context['is_series_exists'] = 'This series do not exists'
        else:
            # checking if user is logged in or not
            if request.user.is_authenticated and request.user.user_type == 'U':
                # checking if user has already rated a series
                rated = SeriesRating.objects.filter(user_id=request.user, series_id=series_details).first()
                if rated:
                    rated.rating = rating
                    rated.save()
                else:
                    rate = SeriesRating.objects.create(
                        series_id=series_details,
                        user_id=request.user,
                        rating=rating,
                    )
                    rate.save()
                context['is_successful'] = 'Your rating for the series is recorded.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to handle user comment report request
@csrf_exempt
def report_comment(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        comment_id = json_data['comment_id']
        comment_flag_val = json_data['comment_flag_val']

        # response object to return as response to ajax request
        context = {
            'is_comment_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if comment exists
        comment_details = VideoComment.objects.filter(comment_id=comment_id).first()
        if comment_details is None:
            context['is_comment_exists'] = 'There is no such comment.'
        else:
            # checking user logged in info
            if request.user.is_authenticated and request.user.user_type == 'U':
                # if user has already flag that comment just change it or update it
                comment_flag = ReportComment.objects.filter(user_id=request.user, comment_id=comment_id).first()
                if comment_flag:
                    comment_flag.flag_val = comment_flag_val
                    comment_flag.save()
                else:
                    report = ReportComment.objects.create(
                        comment_id=comment_details,
                        user_id=request.user,
                        flag_val=int(comment_flag_val),
                    )
                    report.save()
                context['is_successful'] = 'Comment is reported.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to handle user video report request
@csrf_exempt
def report_video(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        video_flag_val = json_data['video_flag_val']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            # checking if user is logged in
            if request.user.is_authenticated and request.user.user_type == 'U':
                # check if user has already flagged that video just update it
                video_flag = ReportVideo.objects.filter(user_id=request.user, video_id=video_id).first()
                if video_flag:
                    video_flag.flag_val = video_flag_val
                    video_flag.save()
                else:
                    report = ReportVideo.objects.create(
                        video_id=video_details,
                        user_id=request.user,
                        flag_val=int(video_flag_val),
                    )
                    report.save()
                context['is_successful'] = 'Video is reported.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to get the video actual duration
def get_video_duration(video_obj):
    # checking the video video_type to know the video duration
    if video_obj.video_type == 1:
        # is_free_series = FreeSeriesVideos.objects.filter(video_id=video_obj).first()
        # if is_free_series:
        #     duration = is_free_series.duration_of_video
        # else:
        #     duration = FreeMovieVideo.objects.filter(video_id=video_obj).first().duration_of_video
        duration = 0
    elif video_obj.video_type == 2:
        duration = SeriesVideos.objects.filter(video_id=video_obj).first().duration_of_video
    elif video_obj.video_type == 3:
        duration = MovieVideo.objects.filter(video_id=video_obj).first().duration_of_video

    return duration


# function to handle user save video history request
@csrf_exempt
def save_video_history(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        curr_time = int(json_data['curr_time'])

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':
                video_duration = get_video_duration(video_details)
                curr_time = min(curr_time, video_duration)
                if curr_time != 0:
                    history = History.objects.filter(user_id=request.user, video_id=video_id).first()
                    if history:
                        history.video_watched = curr_time
                        history.save()
                    else:
                        history = History.objects.create(
                            video_id=video_details,
                            user_id=request.user,
                            video_watched=curr_time,
                            timestamp=datetime.now(tz=timezone.utc),
                        )
                        history.save()
                context['is_successful'] = 'Video is added to history.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# function to handle user search query request
@csrf_exempt
def get_search_results(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        search_based_on = json_data['search_based_on']
        search_query = json_data['search_query']

        # response object to return as response to ajax request
        context = {
            'is_successful': '',
            'search_results': '',
        }

        if search_based_on == 'search by name':
            movies = MovieVideo.objects.filter(
                movie_id__movie_name__icontains=search_query,
                date_of_release__lte=datetime.now(tz=timezone.utc),
                verification_status=2,
            ).values('movie_id__movie_id', 'movie_id__movie_name', 'date_of_release')
            series = SeriesVideos.objects.filter(
                series_season_id__series_id__series_name__icontains=search_query,
                date_of_release__lte=datetime.now(tz=timezone.utc),
                verification_status=2,
            ).values('series_season_id__series_id__series_id', 'series_season_id__series_id__series_name').annotate(max_release_date=Max('date_of_release'))

            search_results = {}
            for obj in movies:
                diff = (datetime.now(tz=timezone.utc) - obj['date_of_release']).total_seconds()
                search_results.update({diff: ('M', obj['movie_id__movie_id'], obj['movie_id__movie_name'])})

            for obj in series:
                diff = (datetime.now(tz=timezone.utc) - obj['max_release_date']).total_seconds()
                search_results.update({diff: ('S', obj['series_season_id__series_id__series_id'], obj['series_season_id__series_id__series_name'])})

            search_results = {k: v for k, v in sorted(search_results.items(), key=lambda item: item[0])}

            context['search_results'] = search_results

        elif search_based_on == 'search by tag':
            movie_video_ids = MovieVideoTags.objects.filter(
                tag_word__icontains=search_query,
            ).values('video_id')
            movies = MovieVideo.objects.filter(
                video_id__in=movie_video_ids,
                date_of_release__lte=datetime.now(tz=timezone.utc),
                verification_status=2,
            ).values('movie_id__movie_id', 'movie_id__movie_name', 'date_of_release')

            series_video_ids = SeriesVideosTags.objects.filter(
                tag_word__icontains=search_query,
            ).values('video_id')
            series = SeriesVideos.objects.filter(
                video_id__in=series_video_ids,
                date_of_release__lte=datetime.now(tz=timezone.utc),
                verification_status=2,
            ).values('series_season_id__series_id__series_id', 'series_season_id__series_id__series_name').annotate(max_release_date=Max('date_of_release'))

            search_results = {}
            for obj in movies:
                diff = (datetime.now(tz=timezone.utc) - obj['date_of_release']).total_seconds()
                search_results.update({diff: ('M', obj['movie_id__movie_id'], obj['movie_id__movie_name'])})

            for obj in series:
                diff = (datetime.now(tz=timezone.utc) - obj['max_release_date']).total_seconds()
                search_results.update({diff: ('S', obj['series_season_id__series_id__series_id'], obj['series_season_id__series_id__series_name'])})

            search_results = {k: v for k, v in sorted(search_results.items(), key=lambda item: item[0])}

            context['search_results'] = search_results

        context['is_successful'] = 'Results Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to handle user search query by subcategory request
@csrf_exempt
def search_results_by_subcategory(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        subcategory = json_data['subcategory']

        # response object to return as response to ajax request
        context = {
            'is_successful': '',
            'search_results': '',
        }

        all_movie_ids_with_subcategory = MovieSubCategories.objects.filter(
            sub_category=SUBCATEGORY[str(subcategory).lower()],
        ).values('movie_id').distinct()

        released_movie_ids = MovieVideo.objects.filter(
            movie_id__in=all_movie_ids_with_subcategory,
            date_of_release__lte=datetime.now(tz=timezone.utc),
            verification_status=2,
        ).values('movie_id__movie_id')

        movie_release_dates = MovieVideo.objects.filter(
            movie_id__in=released_movie_ids,
        ).values('movie_id__movie_id', 'date_of_release')

        movie_release_date_mapping = {}
        for obj in movie_release_dates:
            movie_release_date_mapping.update({obj['movie_id__movie_id']: obj['date_of_release']})
        # print(movie_release_date_mapping)

        movies_data = MovieDetails.objects.filter(movie_id__in=released_movie_ids)
        all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=released_movie_ids)

        # fetching all subcategories for the movies that are to be included
        subcategory_data = {}
        for obj in released_movie_ids:
            subcategory_data.update({obj['movie_id__movie_id']: []})

        for sub_cat in all_subcategory_data:
            subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

        search_results = {}
        for obj in movies_data:
            diff = (datetime.now(tz=timezone.utc) - movie_release_date_mapping[obj.pk]).total_seconds()
            search_results.update({diff: ('M', obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), 'Entertainment', obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], str(obj.pk))})
        # print(search_results)

        all_series_ids_with_subcategory = SeriesSubCategories.objects.filter(
            sub_category=SUBCATEGORY[str(subcategory).lower()],
        ).values('series_id').distinct()

        released_series_ids = SeriesVideos.objects.filter(
            series_season_id__series_id__in=all_series_ids_with_subcategory,
            date_of_release__lte=datetime.now(tz=timezone.utc),
            verification_status=2,
        ).values('series_season_id__series_id__series_id').distinct()

        series_max_release_dates = SeriesVideos.objects.filter(
            series_season_id__series_id__in=released_series_ids,
        ).values('series_season_id__series_id__series_id').annotate(max_release_date=Max('date_of_release'))

        series_max_release_date_mapping = {}
        for obj in series_max_release_dates:
            series_max_release_date_mapping.update({obj['series_season_id__series_id__series_id']: obj['max_release_date']})
        # print(series_max_release_date_mapping)

        series_data = SeriesDetails.objects.filter(series_id__in=released_series_ids)
        all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=released_series_ids)

        # fetching all subcategories for the series that are to be included
        subcategory_data = {}
        for obj in released_series_ids:
            subcategory_data.update({obj['series_season_id__series_id__series_id']: []})

        for sub_cat in all_subcategory_data:
            subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

        for obj in series_data:
            diff = (datetime.now(tz=timezone.utc) - series_max_release_date_mapping[obj.pk]).total_seconds()
            search_results.update({diff: ('S', obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], str(obj.pk))})

        search_results = {k: v for k, v in sorted(search_results.items(), key=lambda item: item[0])}
        # print(search_results)

        context['search_results'] = dict(itertools.islice(search_results.items(), 24))
        context['is_successful'] = 'Results Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# function to handle ad new comment to video
@csrf_exempt
def add_video_comment(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        comment = json_data['comment']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
            'comment_id': '',
            'username': '',
            'comment': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':

                # using a naive bayes classifier to predict the positivity/negativity of a comment
                probdist = classifier.prob_classify(extract_features(comment.split()))
                pred_sentiment = probdist.max()
                comment_type = 0
                if pred_sentiment == 'Positive' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
                    comment_type = 1
                elif pred_sentiment == 'Negative' and round(probdist.prob(pred_sentiment), 2) >= 0.6:
                    comment_type = 2
                else:
                    comment_type = 3

                new_comment = VideoComment.objects.create(
                    user_id=request.user,
                    video_id=video_details,
                    comment=comment,
                    comment_type=comment_type,
                    timestamp=datetime.now(tz=timezone.utc),
                )
                new_comment.save()
                context['is_successful'] = 'Comment added successfully.'
                context['comment_id'] = new_comment.pk
                context['username'] = request.user.username
                context['comment'] = new_comment.comment
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to handle add video to favourite request
@csrf_exempt
def add_to_favourite(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'is_successful': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':
                favourite = Favourites.objects.filter(video_id=video_id).first()
                if favourite is None:
                    favourite = Favourites.objects.create(
                        video_id=video_details,
                    )
                    favourite.save()
                favourite.users.add(request.user)
                context['is_successful'] = 'Video is added to your favourites.'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to get video cost
@csrf_exempt
def get_video_cost(video_obj):

    if video_obj.video_type == 1:
        cost = 0
    elif video_obj.video_type == 2:
        cost = SeriesVideos.objects.filter(video_id=video_obj).first().cost_of_video
    elif video_obj.video_type == 3:
        cost = MovieVideo.objects.filter(video_id=video_obj).first().cost_of_video

    return cost


# function to handle min wallet bal check for paying for pay per view service
@csrf_exempt
def get_pay_per_view_video(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'insufficient_balance': '',
            'is_successful': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':
                cost = get_video_cost(video_details)
                user_details = UserDetails.objects.filter(user=request.user).first()
                wallet_bal = user_details.wallet_money
                if wallet_bal < cost:
                    context['insufficient_balance'] = 'You do not have enough money in your wallet. Add money to your wallet first to continue paying for this video.'
                else:
                    # generating a unique transaction id for wallet payment
                    transaction_id = str(request.user.id) + str(datetime.now())
                    hash_object = hashlib.sha1(transaction_id.encode('utf-8'))
                    hex_dig = hash_object.hexdigest()

                    transaction = PayPerViewTransaction.objects.create(
                        transaction_id=hex_dig,
                        user_id=request.user,
                        video_id=video_details,
                        transaction_start_time=datetime.now(tz=timezone.utc),
                    )
                    transaction.save()

                    user_details.wallet_money -= cost
                    user_details.save()

                    context['is_successful'] = 'Paid successful for video!!'
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# function to handle min wallet bal check for paying for pay per view service
@csrf_exempt
def check_min_wallet_bal(request):
    if request.method == 'POST':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_user_logged_in': '',
            'insufficient_balance': '',
            'is_successful': '',
            'video_cost': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':
                cost = get_video_cost(video_details)
                wallet_bal = UserDetails.objects.filter(user=request.user).first().wallet_money
                if wallet_bal < cost:
                    context['insufficient_balance'] = 'You do not have enough money in your wallet. Add money to your wallet first to continue paying for this video.'
                else:
                    context['is_successful'] = 'Sufficient balance found!!'
                    context['video_cost'] = cost
            else:
                context['is_user_logged_in'] = 'You are not logged in.'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to check whther user has bought a pay per view for current video
def check_pay_per_view_for_video(user, video_id):
    curr_time = datetime.today() - timedelta(days=1)
    is_allowed = PayPerViewTransaction.objects.filter(
        user_id=user,
        video_id=video_id,
        transaction_start_time__gt=curr_time
    )
    if is_allowed:
        return True
    else:
        return False



# function to check whether user is subsscribed or not
@csrf_exempt
def check_user_subscription(request):
    if request.method == 'POST':
        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']

        context = {
            'is_video_exists': '',
            'is_subscribed': '',
            'is_video_in_history': '',
            'video_watched': '',
        }

        # checking if video exists
        video_details = Videos.objects.filter(video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            if request.user.is_authenticated and request.user.user_type == 'U':
                # checking logged in user subscription plan details
                subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
                history = History.objects.filter(user_id=request.user, video_id=video_details).first()

                if subscribe:
                    context['is_subscribed'] = 'true'
                    if history:
                        context['is_video_in_history'] = 'This video exists in history.'
                        context['video_watched'] = history.video_watched
                else:
                    if video_id != '' and video_id != -1:
                        video_obj = Videos.objects.filter(video_id=video_id).first()
                        if video_obj and video_obj.video_type == 1:
                            context['is_subscribed'] = 'true'
                            if history:
                                context['is_video_in_history'] = 'This video exists in history.'
                                context['video_watched'] = history.video_watched
                        else:
                            is_subscribe_for_video = check_pay_per_view_for_video(request.user, video_id)
                            if is_subscribe_for_video:
                                context['is_subscribed'] = 'true'
                                if history:
                                    context['is_video_in_history'] = 'This video exists in history.'
                                    context['video_watched'] = history.video_watched
                            else:
                                context['is_subscribed'] = 'false'
                    else:
                        context['is_subscribed'] = 'false'
            else:
                context['is_subscribed'] = 'false'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# sending chunk by chunk video data to the video tag on request
def response_iter(url, first_byte, subscription_required, request, video_id):
    ran = 'bytes=' + str(first_byte) + '-'
    headers = {'Range': ran}
    r = requests.get(url, headers=headers, stream=True)
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
            if subscription_required:
                if request.user.is_authenticated:
                    # checking logged in user subscription plan details
                    subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
                    if subscribe:
                        yield chunk
                    else:
                        is_subscribe_for_video = check_pay_per_view_for_video(request.user, video_id)
                        if is_subscribe_for_video:
                            yield chunk
                        else:
                            return redirect('subscription_plans')
                else:
                    return redirect('home_page')
            else:
                yield chunk



@condition(etag_func=None)
def stream_video(request, video_obj):
    if video_obj.video_type == 1:
        subscription_required = False
        video_details = FreeSeriesVideos.objects.filter(video_id=video_obj).first()
        if video_details is None:
            video_details = FreeMovieVideo.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 2:
        subscription_required = True
        video_details = SeriesVideos.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 3:
        subscription_required = True
        video_details = MovieVideo.objects.filter(video_id=video_obj).first()

    # getting firebase url for uploaded video file
    path_on_cloud = 'videos/' + video_details.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[video_details.extension]
    firebase_video_url = storage.child(path_on_cloud).get_url(video_details.firebase_token)

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    base_url = str(firebase_video_url).split('?')[0]
    video_details = requests.get(base_url).text
    details_dict = eval(video_details)
    print(details_dict)
    size = int(details_dict['size'])

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        content_type = 'video/mp4'

        chunk_response = response_iter(firebase_video_url, first_byte, subscription_required, request, video_obj)
        resp = StreamingHttpResponse(chunk_response, status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        return render(request, 'templates/404.html')
    resp['accept-ranges'] = 'bytes'
    print('response_sent')
    return resp



def fetch_video(request, video_id):
    video_obj = Videos.objects.filter(video_id=video_id).first()
    if video_obj:
        if video_obj.video_type == 1:
            return stream_video(request, video_obj)
        else:
            if request.user.is_authenticated:
                # checking logged in user subscription plan details
                subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
                if subscribe:
                    return stream_video(request, video_obj)
                else:
                    is_subscribe_for_video = check_pay_per_view_for_video(request.user, video_id)
                    if is_subscribe_for_video:
                        return stream_video(request, video_obj)
                    else:
                        return render(request, 'templates/404.html')
            else:
                return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')



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

    classifier = NaiveBayesClassifier.train(features_train)
    return classifier


classifier = train_comment_judging_classifier()