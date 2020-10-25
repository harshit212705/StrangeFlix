# importing models from provider/models.py
from provider.models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo, MovieRating, SeriesRating, VideoComment, VideoRejectionComment

from django.shortcuts import render, redirect
from django.views.generic import View
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from subscribe.models import Subscriptions
from datetime import datetime
import os
import json
import uuid
import urllib.request
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import base64
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse


from .recommendations import recommend_movies, recommend_series, recent_movies_suggestion, \
    recent_series_suggestion, popular_movies_suggestion, popular_series_suggestion
from provider.views import LANGUAGE_REVERSE, SUBCATEGORY_REVERSE, CATEGORY_REVERSE, VERIFICATION_REVERSE, \
                            VIDEO_EXTENSION_REVERSE, VIDEO_QUALITY_REVERSE, VIDEO_TYPE_REVERSE, \
                            VIDEO_BASE_FILEPATH, storage



# function to render the mainpage or homepage
class HomeView(View):
    def get(self, request):

        # res = stream_video(request)
        # return res

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
                # print(movies_ids)
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

                context['recommended_movies'] = recommended_movies


            # fetching recommended series for logged in user
            series_ids = recommend_series(request)
            # print(series_ids)
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

            context['recent_movies'] = recent_movies


        # fetching recent series for everyone
        recent_series_ids = recent_series_suggestion(request)
        # print(series_ids)
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

            context['popular_movies'] = popular_movies


        # fetching popular series for everyone
        popular_series_ids = popular_series_suggestion(request)
        # print(series_ids)
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
            # print(all_subcategory_data)

            # fetching all subcategories for the movies that is to be included
            subcategory_data = {}
            subcategory_data.update({int(movie_id): []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())


            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in movie_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching movie video details
            movie_video_details = MovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            )

            movie_content_data = {}
            for obj in movie_video_details:

                # getting firebase url for uploaded video file
                # path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                # firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)
                movie_language = str(LANGUAGE_REVERSE[movie_details.language]).title()
                movie_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, '', obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id], subcategory_data[int(movie_id)], movie_language, obj.cost_of_video)})

            # returning success response to ajax request
            context['movie_content_data'] = movie_content_data

            # fetching movie free content details for the movie
            movie_video_id = FreeMovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')
            all_tags_data = FreeMovieVideoTags.objects.filter(video_id__in=movie_video_id)

            # fetching all tags for the free content that are to be included
            tags_data = {}
            for obj in movie_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            # fetching movie free content details
            movie_video_details = FreeMovieVideo.objects.filter(
                movie_id=movie_details,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('-date_of_release')

            movie_free_data = {}
            for obj in movie_video_details:

                # getting firebase url for uploaded video file
                # path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                # firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                movie_free_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, '', obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

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
            all_tags_data = FreeSeriesVideosTags.objects.filter(video_id__in=series_video_id)

            # fetching all tags for the free content that are to be included
            tags_data = {}
            for obj in series_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            # fetching series free content details
            series_video_details = FreeSeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('-date_of_release')

            season_free_data = {}
            for obj in series_video_details:

                season_free_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, subcategory_data[int(season_details[0].series_id.series_id)], obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_free_data'] = season_free_data


            # fetching season episodes details
            series_video_id = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('video_id')
            all_tags_data = SeriesVideosTags.objects.filter(video_id__in=series_video_id)

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in series_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            # fetching series episodes details
            series_video_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).order_by('episode_no')

            max_episode_no = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2,
                date_of_release__lte=datetime.now(tz=timezone.utc),
            ).values('episode_no').order_by('-episode_no')[0]
            max_episode_no = max_episode_no['episode_no']

            season_episodes = {}
            for obj in series_video_details:

                season_episodes.update({int(obj.episode_no): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, subcategory_data[int(season_details[0].series_id.series_id)], obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id], obj.cost_of_video)})

            for i in range(max_episode_no):
                if i+1 not in season_episodes.keys():
                    season_episodes.update({int(i+1): (-1, 'Not Available', 'Not Available', '', subcategory_data[int(season_details[0].series_id.series_id)], '', '', str(VERIFICATION_REVERSE[3]).title(), [], 0)})

            season_episodes = {k: v for k, v in sorted(season_episodes.items(), key=lambda item: item[0])}

            # returning success response to ajax request
            context['season_episodes'] = season_episodes

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



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
            if request.user.is_authenticated and request.user.user_type == 'U':
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
            if request.user.is_authenticated and request.user.user_type == 'U':
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


import requests
def response_iter(url, first_byte, subscription_required, request):
    ran = 'bytes=' + str(first_byte) + '-'
    headers = {'Range': ran}
    r = requests.get(url, headers=headers, stream=True)
    # r.raise_for_status()
    # with open("/home/harshit/Desktop/webster2020/check.mp4", 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
            # print(chunk)
            if subscription_required:
                if request.user.is_authenticated:
                    # checking logged in user subscription plan details
                    subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
                    if subscribe:
                        yield chunk
                    else:
                        return redirect('subscription_plans')
                else:
                    return redirect('home_page')
            else:
                yield chunk


# def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
#     with open(file_name, "rb") as f:
#         f.seek(offset, os.SEEK_SET)
#         remaining = length
#         while True:
#             bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
#             data = f.read(bytes_length)
#             if not data:
#                 break
#             if remaining:
#                 remaining -= len(data)
#             # print(data)
#             yield data


from django.views.decorators.http import condition

@condition(etag_func=None)
def stream_video(request, video_obj):
    # print(request.META)
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
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fab783e7c-1bfb-4992-89e3-fa1fcd708936.mp4?alt=media&token=69b4c009-4bf3-4ef7-ad68-faafc91fcd4c'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F0b3aaf33-f04d-4949-aafc-f147571b2a6e.mp4?alt=media&token=0c45781c-001f-48f4-a7cd-ed0f569f5c1d'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F05628f4f-11b2-4bb0-bc93-76bb13fa3221.mp4?alt=media&token=47726f97-1404-40bf-bdf9-75b389c8f836'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fa5674582-2005-4f44-a9b0-abc25016a246.mp4?alt=media&token=d74a389b-ce2a-478f-9c16-4d68fd95c9d8'
    # firebase_video_url = '/home/harshit/Desktop/webster2020/song.mp4'
    # path = '/home/harshit/Desktop/webster2020/sample_video.mp4'

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    base_url = str(firebase_video_url).split('?')[0]
    video_details = requests.get(base_url).text
    details_dict = eval(video_details)
    size = int(details_dict['size'])

    if range_match:
        print("range perfect")
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        content_type = 'video/mp4'

        chunk_response = response_iter(firebase_video_url, first_byte, subscription_required, request)
        print(chunk_response)
        # <generator object response_iter at 0x7f23487eb6d0>
        resp = StreamingHttpResponse(chunk_response, status=206, content_type=content_type)
        # resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        # print('response sent')
        # os.remove(video_fragment_save_path)
    else:
        return render(request, 'templates/404.html')
        # print("range not fine")
        # extension = str(firebase_video_url).split('?')[0][-3:]
        # unique_video_name = str(uuid.uuid4())
        # video_fragment_save_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + 'flv'

        # req = urllib.request.Request(firebase_video_url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0')
        # # req.add_header('Range', range_header) # <=== range header
        # res = urllib.request.urlopen(req)

        # with open(video_fragment_save_path, 'wb') as f:
        #     f.write(res.read())

        # content_type, encoding = mimetypes.guess_type(video_fragment_save_path)
        # content_type = content_type or 'application/octet-stream'
        # # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        # resp = StreamingHttpResponse(FileWrapper(open(video_fragment_save_path, 'rb')), content_type=content_type)
        # resp['Content-Length'] = str(size)
        # # os.remove(video_fragment_save_path)
    resp['accept-ranges'] = 'bytes'
    print('go')
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
                    return render(request, 'templates/404.html')
            else:
                return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')





# @csrf_exempt
# def stream_movie(request):
#     if request.method == 'POST' and request.user.user_type == 'U':

#         # extracting form data coming from ajax request
#         json_data = json.loads(request.POST['data'])
#         movie_id = json_data['movie_id']
#         movie_start_time = json_data['start_time']

#         print(movie_start_time)

#         # response object to return as response to ajax request
#         context = {
#             'is_movie_exists': '',
#             'is_user_subscribed': '',
#             'is_successful': '',
#             'stream': '',
#             'movie_duration': '',
#         }

#         # checking if movie exists
#         movie_details = MovieDetails.objects.filter(movie_id=movie_id).first()
#         if movie_details is None:
#             context['is_movie_exists'] = 'This movie do not exists'
#         else:
#             # checking logged in user subscription plan details
#             subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
#             if subscribe:
#                 # fetching movie video details for the movie
#                 movie_video_details = MovieVideo.objects.filter(movie_id=movie_details).first()
                # # getting firebase url for uploaded video file
                # path_on_cloud = 'videos/' + movie_video_details.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[movie_video_details.extension]
                # firebase_video_url = storage.child(path_on_cloud).get_url(movie_video_details.firebase_token)

#                 start_time = movie_start_time
#                 end_time = start_time + 10
#                 if end_time > movie_video_details.duration_of_video:
#                     end_time = movie_video_details.duration_of_video

                # extension = str(firebase_video_url).split('?')[0][-3:]
                # unique_video_name = str(uuid.uuid4())
                # video_fragment_save_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension

#                 ffmpeg_extract_subclip("https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fab783e7c-1bfb-4992-89e3-fa1fcd708936.mp4?alt=media&token=69b4c009-4bf3-4ef7-ad68-faafc91fcd4c", start_time, end_time, targetname=video_fragment_save_path)

#                 with open(video_fragment_save_path, "rb") as videoFile:
#                     text = base64.b64encode(videoFile.read()).decode('utf-8')
#                     # print(text)
#                 context['stream'] = text
#                 context['movie_duration'] = movie_video_details.duration_of_video
#                 os.remove(video_fragment_save_path)
#                 context['is_successful'] = 'Packet fetched successfully'
#             else:
#                 context['is_user_subscribed'] = 'You are not subscribed to watch this movie. Go buy a subscription plan.'
#         return JsonResponse(context)
#     else:
#         return render(request, 'templates/404.html')


