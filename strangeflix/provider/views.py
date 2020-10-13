# importing models from provider/models.py
from .models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo

# importing other modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from django.utils import timezone
import os
import json
import uuid
from django.conf import settings

# For firebase connection and video file upload
import pyrebase

# modules for accessing metadata of file
import filetype
import magic
import ffmpeg
import moviepy.editor as mp

# python module to download video from links from more than 1000 websites
import youtube_dl

# local directory path to temporary store video files
VIDEO_BASE_FILEPATH = os.path.join(settings.BASE_DIR, 'videos')

# firebase configuration settings
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

# initializing firebase storage bucket
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# python dictionaries
LANGUAGE = {'english': 1, 'hindi': 2, 'bengali': 3, 'kannada': 4, 'malayalam': 5, 'marathi': 6, 'tamil': 7, 'telugu': 8}
CATEGORY = {'sports': 1, 'entertainment': 2}
SUBCATEGORY = {'cricket': 1, 'football': 2, 'tennis': 3, 'martial arts': 4, 'esports': 5, 'hockey': 6,
'badminton': 7, 'wrestling': 8, 'kabaddi': 9, 'table tennis': 10, 'action': 11, 'adventure': 12,
'animation': 13, 'comedy': 14, 'crime': 15, 'drama': 16, 'horror': 17, 'romance': 18, 'thriller': 19}
VIDEO_TYPE = {'free': 1, 'series': 2, 'movie': 3}
VIDEO_QUALITY = {'144': 1, '240': 2, '360': 3, '480': 4, '720': 5, '1080': 6}
VERIFICATION = {'pending': 1, 'verified': 2, 'rejected': 3, 'not submitted': 4}
VIDEO_EXTENSION = {'mp4': 1, 'mkv': 2, 'flv': 3, 'webm': 4, 'ogg': 5}

# python dictionaries
LANGUAGE_REVERSE = {1: 'english', 2: 'hindi', 3: 'bengali', 4: 'kannada', 5: 'malayalam', 6: 'marathi', 7: 'tamil', 8: 'telugu'}
CATEGORY_REVERSE = {1: 'sports', 2: 'entertainment'}
SUBCATEGORY_REVERSE = {1: 'cricket', 2: 'football', 3: 'tennis', 4: 'martial arts', 5: 'esports', 6: 'hockey', 7: 'badminton', 8: 'wrestling', 9: 'kabaddi', 10: 'table tennis', 11: 'action', 12: 'adventure', 13: 'animation', 14: 'comedy', 15: 'crime', 16: 'drama', 17: 'horror', 18: 'romance', 19: 'thriller'}
VIDEO_TYPE_REVERSE = {1: 'free', 2: 'series', 3: 'movie'}
VIDEO_QUALITY_REVERSE = {1: '144', 2: '240', 3: '360', 4: '480', 5: '720', 6: '1080'}
VERIFICATION_REVERSE = {1: 'pending', 2: 'verified', 3: 'rejected', 4: 'not submitted'}
VIDEO_EXTENSION_REVERSE = {1: 'mp4', 2: 'mkv', 3: 'flv', 4: 'webm', 5: 'ogg'}


# renders the provider dashboard page on get request from provider account
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


# Handles adding new series
@csrf_exempt
@login_required(login_url='home_page')
def add_new_series(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_name = json_data['series_name']
        series_description = json_data['series_description']
        language = json_data['language']
        category = json_data['category']
        subcategory = json_data['subcategory'].split(',')

        # response object to return as response to ajax request
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
        # check if series already exists
        if series:
            context['is_series_exists'] = 'Series with this name already exists. Try another name!!'

        # check if language is selected by the user
        elif language == 'Languages':
            context['is_language_selected'] = 'No language selected'

        # check if category is selected by the user
        elif category == 'Choose Category':
            context['is_category_selected'] = 'No category selected'

        # check if subcategory is selected by the user
        elif len(subcategory) == 1 and subcategory[0] == '':
            context['is_subcategory_selected'] = 'No subcategory selected'

        # check if thumbnail size is greater than threshold value
        elif clean_file(request.FILES['file']) == False:
            context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'

        else:
            mime = check_in_memory_mime(request.FILES['file'])

            # checking the mime type of the uploaded thumbnail image
            if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':

                # adding new series details to the database
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

                # adding series related subcategory data to the database
                for i in range(len(subcategory)):
                    sub_category = SUBCATEGORY[subcategory[i].lower()]
                    series_subcategory = SeriesSubCategories.objects.create(
                        series_id=new_series,
                        sub_category=sub_category
                    )
                    series_subcategory.save()

                # returning successful response of ajax request
                context['is_successful'] = 'New series added successfully!!'
                context['series_id'] = str(new_series.series_id)
            else:
                context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'

        # returning json response to ajax request
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# view to handle add new season requests
@csrf_exempt
@login_required(login_url='home_page')
def add_new_season(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']
        season_no = json_data['season_no']
        season_description = json_data['season_description']

        # response object to return as response to ajax request
        context = {
            'is_series_exists': '',
            'is_season_no_exists': '',
            'is_thumbnail_too_large': '',
            'is_thumbnail_mimetype_problem': '',
            'is_successful': '',
            'series_season_id': '',
            'all_season_details': '',
        }

        # checking if series already exists
        series = SeriesDetails.objects.filter(series_id=series_id).first()
        if series is None:
            context['is_series_exists'] = 'This series do not exists'
        else:
            season_details = SeriesSeasonDetails.objects.filter(
                series_id=series_id,
                season_no=season_no
            ).first()

            # checking if season number already exists
            if season_details is None:

                # checking threshold size of thumbnail image
                if clean_file(request.FILES['file']) == False:
                    context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'
                else:
                    mime = check_in_memory_mime(request.FILES['file'])

                    # checking the mime type of upoaded thumbnail image
                    if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':

                        # saving new season details to database
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

                        # successful response to ajax request
                        context['is_successful'] = 'New season added successfully!!'
                        context['series_season_id'] = str(new_season.series_season_id)
                        all_season_data = {}
                        obj = new_season

                        # returning the above added season details to ajax request
                        all_season_data.update({str(obj.pk): (obj.description, obj.thumbnail_image.url, str(VERIFICATION_REVERSE[obj.verification_status]).title())})
                        context['all_season_details'] = all_season_data
                    else:
                        context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'
            else:
                context['is_season_no_exists'] = 'This season number for the given series already exists'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to save video file locally
def save_video_file(file, filepath):
    with open(filepath,"wb") as f:
        for chunk in file.chunks():
            f.write(chunk)


# view to handle add new episode request
@csrf_exempt
@login_required(login_url='home_page')
def add_new_episode(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_season_id = json_data['series_season_id']
        episode_no = json_data['episode_no']
        episode_name = json_data['episode_name']
        episode_description = json_data['episode_description']
        episode_tags = json_data['episode_tags'].split(',')
        episode_quality = json_data['episode_quality']
        episode_release_date = json_data['episode_release_date']
        episode_linkorvideo = json_data['episode_linkorvideo']
        episode_link = json_data['episode_link']

        # response object to return as response to ajax request
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

        # check if series season already exists
        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:
            episode_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                episode_no=episode_no
            ).first()

            # check if episode already exists for that season of series
            if episode_details is None:

                # checking if quality of episode not selected by the user
                if episode_quality == 'Quality':
                    context['is_quality_selected'] = 'No episode quality selected'

                # checking if release date of episode is of past
                elif str(date.today()) >= episode_release_date:
                    context['is_release_date_future'] = 'Episode release date should be of future'

                # checking that the thumbnail image must be less than threshold size
                elif clean_file(request.FILES['file']) == False:
                    context['is_thumbnail_too_large'] = 'Thumbnail Image Too Large to upload'
                else:
                    mime = check_in_memory_mime(request.FILES['file'])

                    # checking the mime type of thumbnail image
                    if mime == 'image/jpg' or mime == 'image/jpeg' or mime == 'image/png':

                        # checking whether user has provided the video or link to the video
                        if episode_linkorvideo == 'Video':
                            mime = check_in_memory_mime(request.FILES['video'])
                            # checking mime type of the uploaded video
                            if mime == 'video/mp4' or mime == 'video/x-flv' or mime == 'video/mkv' or mime == 'video/flv' or mime == 'video/x-matroska' or mime == 'video/webm' or mime == 'video/ogg':
                                video_file_name = request.FILES['video'].name.split('.')

                                # checking if video not in correct format
                                if len(video_file_name) == 1:
                                    context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                                else:

                                    # getting video extension
                                    extension = video_file_name[1]
                                    unique_video_name = str(uuid.uuid4())
                                    video_filepath = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension

                                    # saving video file locally
                                    save_video_file(request.FILES['video'], video_filepath)
                                    # getting video quality
                                    episode_quality = calculate_video_quality(video_filepath)
                                    # getting video duration
                                    video_duration =  calculate_video_duration(video_filepath)

                                    # stoing video to firebase cloud
                                    path_on_cloud = 'videos/' + unique_video_name + '.' + extension
                                    firebase_upload = storage.child(path_on_cloud).put(video_filepath)
                                    firebase_video_url = storage.child(path_on_cloud).get_url(firebase_upload['downloadTokens'])

                                    # deleting the locally saved video file
                                    os.remove(video_filepath)

                                    # saving new episode details
                                    new_season_episode = save_video_file_details_to_database(series_season, episode_name, unique_video_name, firebase_upload['downloadTokens'], episode_description, episode_release_date, episode_no, video_duration, VIDEO_QUALITY[episode_quality], VIDEO_EXTENSION[extension.lower()], request.FILES['file'], episode_tags)

                                    # returning successful response to ajax request
                                    context['is_successful'] = 'New season episode added successfully!!'
                                    season_episode_data = {}
                                    obj = new_season_episode

                                    if len(episode_tags) == 1 and episode_tags[0] == '':
                                        episode_tags = []

                                    # returning the above added episode details to ajax request
                                    season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), episode_tags)})
                                    context['season_episode_data'] = season_episode_data
                            else:
                                context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                        else:
                            # if link to the video is provided by the user
                            extension = 'mp4'
                            unique_video_name = str(uuid.uuid4())
                            video_filepath = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension

                            # downloading file from link to local storage using youtube_dl module
                            ydl_opts = {'outtmpl': video_filepath, 'ignoreerrors': True}
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                try:
                                    dictMeta = ydl.extract_info(episode_link, download=True)

                                    # checking if file is protected ot unavailable
                                    if dictMeta is None:
                                        context['is_video_mimetype_problem'] = 'Episode video is either protected or unavailable'
                                        return JsonResponse(context)
                                except Exception as e:
                                    print(e)

                            # Assuming I have all the video extensions in my dictionary
                            for ext in VIDEO_EXTENSION:
                                temp_video_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + ext
                                if os.path.exists(temp_video_path):
                                    video_filepath = temp_video_path
                                    break

                            kind = filetype.guess(video_filepath)

                            # checking extension of downloaded file
                            if kind is None:
                                context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                                return JsonResponse(context)
                            extension = kind.extension
                            mime = kind.mime

                            # checking mimetype of downloaded file
                            if mime != 'video/mp4' and mime != 'video/mkv' and mime != 'video/x-flv' and mime != 'video/flv' and mime != 'video/x-matroska' and mime != 'video/webm' and mime != 'video/ogg':
                                context['is_video_mimetype_problem'] = 'Episode video Not in Correct Format'
                                return JsonResponse(context)

                            dest = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension
                            os.rename(video_filepath, dest)
                            video_filepath = dest

                            # getting video quality
                            episode_quality = calculate_video_quality(video_filepath)
                            # getting video duration
                            video_duration =  calculate_video_duration(video_filepath)

                            # saving file to firebase cloud storage
                            path_on_cloud = 'videos/' + unique_video_name + '.' + extension
                            firebase_upload = storage.child(path_on_cloud).put(video_filepath)
                            firebase_video_url = storage.child(path_on_cloud).get_url(firebase_upload['downloadTokens'])

                            # deleting the locally saved video file
                            os.remove(video_filepath)

                            # saving new episode details
                            new_season_episode = save_video_file_details_to_database(series_season, episode_name, unique_video_name, firebase_upload['downloadTokens'], episode_description, episode_release_date, episode_no, video_duration, VIDEO_QUALITY[episode_quality], VIDEO_EXTENSION[extension.lower()], request.FILES['file'], episode_tags)

                            # returning successful response to ajax request
                            context['is_successful'] = 'New season episode added successfully!!'
                            season_episode_data = {}
                            obj = new_season_episode

                            if len(episode_tags) == 1 and episode_tags[0] == '':
                                episode_tags = []

                            # sending the above added new episode details to ajax request
                            season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), episode_tags)})
                            context['season_episode_data'] = season_episode_data
                    else:
                        context['is_thumbnail_mimetype_problem'] = 'Thumbnail Image Not in Correct Format'
            else:
                context['is_episode_no_exists'] = 'This episode number for the given series season already exists'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# saving new episode details to database
def save_video_file_details_to_database(series_season, episode_name, unique_video_name, download_token, episode_description, episode_release_date, episode_no, video_duration, video_quality, video_extension, thumbnail_image, episode_tags):

    # creating a video instance
    video = Videos.objects.create(
        video_type=2
    )
    video.save()

    # saving new episode details to database
    new_season_episode = SeriesVideos.objects.create(
        series_season_id=series_season,
        video_id=video,
        video_name=episode_name,
        firebase_save_name=unique_video_name,
        firebase_token=download_token,
        description=episode_description,
        date_of_upload=datetime.now(tz=timezone.utc),
        date_of_release=episode_release_date,
        episode_no=episode_no,
        duration_of_video=video_duration,
        quality_of_video=video_quality,
        extension=video_extension,
        verification_status=1,
        cost_of_video=0
    )
    new_season_episode.save()
    new_season_episode.thumbnail_image=thumbnail_image
    new_season_episode.save()

    # adding series video related tag data to the database
    for i in range(len(episode_tags)):
        if episode_tags[i] != '':
            series_video_tag = SeriesVideosTags.objects.create(
                video_id=video,
                episode_no=episode_no,
                tag_word=episode_tags[i],
            )
            series_video_tag.save()

    return new_season_episode

# function to calculate video duration
def calculate_video_duration(video_filepath):

    video_duration =  mp.VideoFileClip(video_filepath).duration
    video_duration = int(video_duration)
    return video_duration


# function to calculate video quality
def calculate_video_quality(video_filepath):

    # Extracting metadata from video file
    vid = ffmpeg.probe(video_filepath)
    episode_quality = ''
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

    return episode_quality


# returning previously uploaded episode for a season to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def previously_uploaded_episodes(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_season_id = json_data['series_season_id']

        # response object to return as response to ajax request
        context = {
            'is_series_belongs_to_provider': '',
            'is_series_season_exists': '',
            'is_successful': '',
            'season_episode_data': '',
        }

        # checking if season of that series exists
        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:

            # checking if series actually belongs to provider or not
            if request.user.user_type == 'P':
                # print(series_season.series_id)
                series_details = SeriesDetails.objects.filter(
                    provider_id=request.user,
                    series_id=series_season.series_id.series_id
                ).first()
                if series_details is None:
                    context['is_series_belongs_to_provider'] = 'This series does not belongs to you.'
                    return JsonResponse(context)

            # fetching episodes details for the season
            all_video_id = SeriesVideos.objects.filter(series_season_id=series_season).values('video_id')
            all_tags_data = SeriesVideosTags.objects.filter(video_id__in=all_video_id).order_by('episode_no')

            # print(all_video_id)
            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching episodes ordered by their episode number
            episode_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
            ).order_by('episode_no')

            season_episode_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_episode_data'] = season_episode_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning previously uploaded series info to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def previously_uploaded_series(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # response object to return as response to ajax request
        context = {
            'is_any_series_exists': '',
            'is_successful': '',
            'all_series_data': '',
        }

        # checking if any series exists for that provider
        all_series = SeriesDetails.objects.filter(provider_id=request.user).order_by('-date_of_creation')
        if all_series is None:
            context['is_any_series_exists'] = 'You have not uploaded any series yet. Upload new series in Add content section.'
        else:
            # fetching series details for the provider with last series added at top
            all_series_id = SeriesDetails.objects.filter(provider_id=request.user).values('series_id')
            all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=all_series_id).order_by('-series_id__series_id')

            # fetching all subcategories for the series that are to be included
            subcategory_data = {}
            for obj in all_series_id:
                subcategory_data.update({obj['series_id']: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # sending series details to ajax request
            all_series_data = {}
            for obj in all_series:
                all_series_data.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk])})

            # returning success response to ajax request
            context['all_series_data'] = all_series_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning previously uploaded series seasons info to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def previously_uploaded_seasons(request):
    if request.method == 'POST' and request.user.user_type == 'P':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']

        # response object to return as response to ajax request
        context = {
            'is_series_belongs_to_provider': '',
            'is_any_series_season_exists': '',
            'is_successful': '',
            'all_series_season_data': '',
        }

        # checking if series actually belongs to provider or not
        if request.user.user_type == 'P':
            series_details = SeriesDetails.objects.filter(
                provider_id=request.user,
                series_id=series_id
            ).first()
            if series_details is None:
                context['is_series_belongs_to_provider'] = 'This series does not belongs to you.'
                return JsonResponse(context)

        # checking if any season exists for that series
        all_series_seasons = SeriesSeasonDetails.objects.filter(series_id__series_id=series_id).order_by('season_no')
        if all_series_seasons is None:
            context['is_any_series_season_exists'] = 'You have not added any season for this series yet. Add new season now.'
        else:
            # sending series season details to ajax request
            all_series_season_data = {}
            for obj in all_series_seasons:
                all_series_season_data.update({str(obj.pk): (obj.season_no, obj.description, obj.date_of_creation, obj.thumbnail_image.url, str(VERIFICATION_REVERSE[obj.verification_status]).title())})

            # returning success response to ajax request
            context['all_series_season_data'] = all_series_season_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')