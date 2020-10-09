from .models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from django.utils import timezone
import os
import json
import uuid
import magic
import ffmpeg
from django.conf import settings
import pyrebase

VIDEO_BASE_FILEPATH = os.path.join(settings.BASE_DIR, 'videos')

config = {
    "apiKey": settings.FIREBASE_API_KEY,
    "authDomain": settings.FIREBASE_AUTH_DOMAIN,
    "databaseURL": settings.FIREBASE_DATABASE_URL,
    "projectId": settings.FIREBASE_PROJECT_ID,
    "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
    "appId": settings.FIREBASE_APP_ID,
    "measurementId": settings.FIREBASE_MEASUREMENT_ID
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


LANGUAGE = {'english': 1, 'hindi': 2, 'bengali': 3, 'kannada': 4, 'malayalam': 5, 'marathi': 6, 'tamil': 7, 'telugu': 8}
CATEGORY = {'sports': 1, 'entertainment': 2}
SUBCATEGORY = {'cricket': 1, 'football': 2, 'tennis': 3, 'martial arts': 4, 'esports': 5, 'hockey': 6,
'badminton': 7, 'wrestling': 8, 'kabaddi': 9, 'table tennis': 10, 'action': 11, 'adventure': 12,
'animation': 13, 'comedy': 14, 'crime': 15, 'drama': 16, 'horror': 17, 'romance': 18, 'thriller': 19}
VIDEO_TYPE = {'free': 1, 'series': 2, 'movie': 3}
VIDEO_QUALITY = {'144': 1, '240': 2, '360': 3, '480': 4, '720': 5, '1080': 6}
VERIFICATION = {'pending': 1, 'verified': 2, 'rejected': 3, 'not submitted': 4}
VIDEO_EXTENSION = {'mp4': 1, 'mkv': 2, 'flv': 3, 'webm': 4, 'ogg': 5}


LANGUAGE_REVERSE = {1: 'english', 2: 'hindi', 3: 'bengali', 4: 'kannada', 5: 'malayalam', 6: 'marathi', 7: 'tamil', 8: 'telugu'}
CATEGORY_REVERSE = {1: 'sports', 2: 'entertainment'}
SUBCATEGORY_REVERSE = {1: 'cricket', 2: 'football', 3: 'tennis', 4: 'martial arts', 5: 'esports', 6: 'hockey', 7: 'badminton', 8: 'wrestling', 9: 'kabaddi', 10: 'table tennis', 11: 'action', 12: 'adventure', 13: 'animation', 14: 'comedy', 15: 'crime', 16: 'drama', 17: 'horror', 18: 'romance', 19: 'thriller'}
VIDEO_TYPE_REVERSE = {1: 'free', 2: 'series', 3: 'movie'}
VIDEO_QUALITY_REVERSE = {1: '144', 2: '240', 3: '360', 4: '480', 5: '720', 6: '1080'}
VERIFICATION_REVERSE = {1: 'pending', 2: 'verified', 3: 'rejected', 4: 'not submitted'}
VIDEO_EXTENSION_REVERSE = {1: 'mp4', 2: 'mkv', 3: 'flv', 4: 'webm', 5: 'ogg'}



@login_required(login_url='home_page')
def provider_dashboard(request):
    if request.method == 'GET' and request.user.user_type == 'P':
        return render(request, 'provider/provider.html')
    else:
        return render(request, 'templates/404.html')


# Function to restrict the size of the file
def clean_file(file):
    if file.size > 10242000:
        return False
    return True


# Function to return the mime-type of the file
def check_in_memory_mime(file):
    mime = magic.from_buffer(file.read(), mime=True)
    return mime



@csrf_exempt
@login_required(login_url='home_page')
def add_new_series(request):
    if request.method == 'POST' and request.user.user_type == 'P':
        json_data = json.loads(request.POST['data'])
        series_name = json_data['series_name']
        series_description = json_data['series_description']
        language = json_data['language']
        category = json_data['category']
        subcategory = json_data['subcategory'].split(',')

        context = {
            'is_series_exists': '',
            'is_language_selected': '',
            'is_category_selected': '',
            'is_subcategory_selected': '',
            'is_thumbnail_too_large': '',
            'is_thumbnail_mimetype_problem': '',
            'is_successful': '',
            'series_id': '',
        }

        series = SeriesDetails.objects.filter(series_name__iexact=series_name.lower()).first()
        if series:
            context['is_series_exists'] = 'Series with this name already exists. Try another name!!'
        elif language == 'Languages':
            context['is_language_selected'] = 'No language selected'
        elif category == 'Choose Category':
            context['is_category_selected'] = 'No category selected'
        elif len(subcategory) == 1 and subcategory[0] == '':
            context['is_subcategory_selected'] = 'No subcategory selected'
        elif clean_file(request.FILES['file']) == False:
            context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'
        else:
            mime = check_in_memory_mime(request.FILES['file'])
            if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':
                new_series = SeriesDetails.objects.create(
                    provider_id=request.user,
                    series_name=series_name,
                    description=series_description,
                    language=LANGUAGE[language.lower()],
                    category=CATEGORY[category.lower()],
                    date_of_creation=datetime.now(tz=timezone.utc)
                )
                new_series.save()
                new_series.thumbnail_image=request.FILES['file']
                new_series.save()

                for i in range(len(subcategory)):
                    sub_category = SUBCATEGORY[subcategory[i].lower()]
                    series_subcategory = SeriesSubCategories.objects.create(
                        series_id=new_series,
                        sub_category=sub_category
                    )
                    series_subcategory.save()
                context['is_successful'] = 'New series added successfully!!'
                context['series_id'] = str(new_series.series_id)
            else:
                context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'

        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



@csrf_exempt
@login_required(login_url='home_page')
def add_new_season(request):
    if request.method == 'POST' and request.user.user_type == 'P':
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']
        season_no = json_data['season_no']
        season_description = json_data['season_description']
        # print(series_id)
        # print(season_no)
        # print(season_description)

        context = {
            'is_series_exists': '',
            'is_season_no_exists': '',
            'is_thumbnail_too_large': '',
            'is_thumbnail_mimetype_problem': '',
            'is_successful': '',
            'series_season_id': '',
            'all_season_details': '',
        }

        series = SeriesDetails.objects.filter(series_id=series_id).first()
        if series is None:
            context['is_series_exists'] = 'This series do not exists'
        else:
            season_details = SeriesSeasonDetails.objects.filter(
                series_id=series_id,
                season_no=season_no
            ).first()

            if season_details is None:
                if clean_file(request.FILES['file']) == False:
                    context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'
                else:
                    mime = check_in_memory_mime(request.FILES['file'])
                    if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':
                        new_season = SeriesSeasonDetails.objects.create(
                            series_id=series,
                            season_no=season_no,
                            description=season_description,
                            date_of_creation=datetime.now(tz=timezone.utc),
                            verification_status=1
                        )
                        new_season.save()
                        new_season.thumbnail_image=request.FILES['file']
                        new_season.save()

                        context['is_successful'] = 'New season added successfully!!'
                        context['series_season_id'] = str(new_season.series_season_id)
                        all_season_data = {}
                        obj = new_season

                        all_season_data.update({str(obj.pk): (obj.description, obj.thumbnail_image.url, VERIFICATION_REVERSE[obj.verification_status])})
                        context['all_season_details'] = all_season_data
                    else:
                        context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'
            else:
                context['is_season_no_exists'] = 'This season number for the given series already exists'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


def save_video_file(file, filepath):
    with open(filepath,"wb") as f:
        for chunk in file.chunks():
            f.write(chunk)



@csrf_exempt
@login_required(login_url='home_page')
def add_new_episode(request):
    if request.method == 'POST' and request.user.user_type == 'P':
        json_data = json.loads(request.POST['data'])

        series_season_id = json_data['series_season_id']
        episode_no = json_data['episode_no']
        episode_name = json_data['episode_name']
        episode_description = json_data['episode_description']
        episode_tags = json_data['episode_tags'].split(',')
        episode_quality = json_data['episode_quality']
        episode_release_date = json_data['episode_release_date']

        context = {
            'is_series_season_exists': '',
            'is_episode_no_exists': '',
            'is_quality_selected': '',
            'is_release_date_future': '',
            'is_thumbnail_too_large': '',
            'is_thumbnail_mimetype_problem': '',
            'is_video_mimetype_problem': '',
            'is_successful': '',
            'season_episode_data': '',
        }

        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:
            episode_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                episode_no=episode_no
            ).first()
            if episode_details is None:
                if episode_quality == 'Quality':
                    context['is_quality_selected'] = 'No episode quality selected'
                elif str(date.today()) >= episode_release_date:
                    context['is_release_date_future'] = 'Episode release date should be of future'
                elif clean_file(request.FILES['file']) == False:
                    context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'
                else:
                    mime = check_in_memory_mime(request.FILES['file'])
                    if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':
                        mime = check_in_memory_mime(request.FILES['video'])
                        if mime == 'video/mp4' or mime == 'video/mkv' or mime == 'video/flv' or mime == 'video/webm' or mime == 'video/ogg':
                            video_file_name = request.FILES['video'].name.split('.')
                            if len(video_file_name) == 1:
                                context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                            else:
                                extension = video_file_name[1]
                                unique_video_name = str(uuid.uuid4())
                                video_filepath = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension
                                save_video_file(request.FILES['video'], video_filepath)

                                # Extracting metadata from video file
                                vid = ffmpeg.probe(video_filepath)
                                actual_video_quality = int(vid['streams'][0]['coded_height'])
                                if actual_video_quality <= 200:
                                    episode_quality = '144'
                                elif actual_video_quality <= 320:
                                    episode_quality = '240'
                                elif actual_video_quality <= 440:
                                    episode_quality = '360'
                                elif actual_video_quality <= 660:
                                    episode_quality = '480'
                                elif actual_video_quality <= 960:
                                    episode_quality = '720'
                                else:
                                    episode_quality = '1080'
                                # print(int(float(vid['streams'][0]['duration'])))

                                path_on_cloud = 'videos/' + unique_video_name + '.' + extension
                                firebase_upload = storage.child(path_on_cloud).put(video_filepath)
                                firebase_video_url = storage.child(path_on_cloud).get_url(firebase_upload['downloadTokens'])
                                # print(firebase_upload)
                                # print(firebase_upload['downloadTokens'])

                                os.remove(video_filepath)

                                video = Videos.objects.create(
                                    video_type=2
                                )
                                video.save()
                                new_season_episode = SeriesVideos.objects.create(
                                    series_season_id=series_season,
                                    video_id=video,
                                    video_name=episode_name,
                                    firebase_save_name=unique_video_name,
                                    firebase_token=firebase_upload['downloadTokens'],
                                    description=episode_description,
                                    date_of_upload=datetime.now(tz=timezone.utc),
                                    date_of_release=episode_release_date,
                                    episode_no=episode_no,
                                    duration_of_video=int(float(vid['streams'][0]['duration'])),
                                    quality_of_video=VIDEO_QUALITY[episode_quality],
                                    extension=VIDEO_EXTENSION[extension.lower()],
                                    verification_status=1,
                                    cost_of_video=0
                                )
                                new_season_episode.save()
                                new_season_episode.thumbnail_image=request.FILES['file']
                                new_season_episode.save()

                                context['is_successful'] = 'New season episode added successfully!!'
                                season_episode_data = {}
                                obj = new_season_episode

                                season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, VERIFICATION_REVERSE[obj.verification_status])})
                                context['season_episode_data'] = season_episode_data
                        else:
                            context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                    else:
                        context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'
            else:
                context['is_episode_no_exists'] = 'This episode number for the given series season already exists'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



@csrf_exempt
@login_required(login_url='home_page')
def previously_uploaded_episodes(request):
    if request.method == 'POST' and request.user.user_type == 'P':
        json_data = json.loads(request.POST['data'])

        series_season_id = json_data['series_season_id']

        context = {
            'is_series_season_exists': '',
            'is_successful': '',
            'season_episode_data': '',
        }

        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:
            episode_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
            ).order_by('episode_no')

            season_episode_data = {}
            for obj in episode_details:

                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, VERIFICATION_REVERSE[obj.verification_status])})

            context['season_episode_data'] = season_episode_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')