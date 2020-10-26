# importing models from provider/models.py
from provider.models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo, \
                    VideoRejectionComment

# importing dictionaries from provider/views.py
from provider.views import SUBCATEGORY_REVERSE, VERIFICATION_REVERSE, LANGUAGE_REVERSE, CATEGORY_REVERSE, VIDEO_EXTENSION_REVERSE


# importing firebase storage bucket reference
from provider.views import storage

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

#  imports required for Email Sending:-
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from accounts.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.views import send_email


# renders the admin dashboard page on get request from admin account
@login_required(login_url='home_page')
def admin_dashboard(request):
    if request.method == 'GET' and request.user.user_type == 'A':
        return render(request, 'Admin/admin.html')
    else:
        return render(request, 'templates/404.html')


# get all the pending series
@csrf_exempt
@login_required(login_url='home_page')
def get_series(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # response object to return as response to ajax request
        context = {
            'is_any_pending_series_exists': '',
            'is_successful': '',
            'pending_series_data': '',
        }

        # fetching series id of all those series whose any season is in pending stage
        pending_series_id = SeriesVideos.objects.filter(verification_status=1).values('series_season_id__series_id').distinct().union(
            FreeSeriesVideos.objects.filter(verification_status=1).values('series_season_id__series_id').distinct()
        )

        if pending_series_id is None:
            context['is_any_pending_series_exists'] = 'There are no pending series to verify!!'
        else:
            # fetching series details of pending series
            pending_series_details = SeriesDetails.objects.filter(series_id__in=pending_series_id).order_by('date_of_creation')

            # fetching all subcategories for the series that are to be included
            all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=pending_series_id)
            subcategory_data = {}
            for obj in pending_series_id:
                subcategory_data.update({obj['series_season_id__series_id']: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # sending series details to ajax request
            pending_series_data = {}
            for obj in pending_series_details:
                pending_series_data.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], obj.provider_id.username)})

            # returning success response to ajax request
            context['pending_series_data'] = pending_series_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# returning previously uploaded episode for a season to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def pending_uploaded_episodes(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_season_id = json_data['series_season_id']

        # response object to return as response to ajax request
        context = {
            'is_series_season_exists': '',
            'is_successful': '',
            'season_episode_data': '',
            'season_content_data': '',
        }

        # checking if season of that series exists
        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:

            # fetching episodes details for the season
            all_video_id = SeriesVideos.objects.filter(
                series_season_id=series_season,
                verification_status=1,
            ).values('video_id')
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
                verification_status=1
            ).order_by('episode_no')

            season_episode_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_episode_data'] = season_episode_data


            # fetching free content details for the season
            all_video_id = FreeSeriesVideos.objects.filter(
                series_season_id=series_season,
                verification_status=1,
            ).values('video_id')
            all_tags_data = FreeSeriesVideosTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the free content that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching free content ordered by their date of upload
            episode_details = FreeSeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=1
            ).order_by('date_of_upload')

            season_content_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_content_data'] = season_content_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning previously uploaded series seasons info to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def pending_uploaded_seasons(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']

        # response object to return as response to ajax request
        context = {
            'is_any_series_season_exists': '',
            'is_successful': '',
            'all_series_season_data': '',
        }

        # checking if any season exists for that series
        pending_series_season_id = SeriesVideos.objects.filter(
            verification_status=1,
            series_season_id__series_id=series_id,
        ).values('series_season_id__series_season_id').distinct().union(
            FreeSeriesVideos.objects.filter(
                verification_status=1,
                series_season_id__series_id=series_id,
            ).values('series_season_id__series_season_id').distinct()
        )
        if pending_series_season_id is None:
            context['is_any_series_season_exists'] = 'There are no seasons to verify for this series.'
        else:
            all_series_seasons = SeriesSeasonDetails.objects.filter(
                series_season_id__in=pending_series_season_id,
            ).order_by('season_no')

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



# returning previously uploaded episode for a season to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def pending_movie_videos(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        movie_id = json_data['movie_id']

        # response object to return as response to ajax request
        context = {
            'is_movie_exists': '',
            'is_successful': '',
            'movie_episode_data': '',
            'movie_content_data': '',
        }

        # checking if movie exists
        movie = MovieDetails.objects.filter(movie_id=movie_id).first()
        if movie is None:
            context['is_movie_exists'] = 'This movie do not exists'
        else:

            # fetching episodes details for the movie
            all_video_id = MovieVideo.objects.filter(
                movie_id=movie,
                verification_status=1,
            ).values('video_id')
            all_tags_data = MovieVideoTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching episodes ordered by their date of upload
            episode_details = MovieVideo.objects.filter(
                movie_id=movie,
                verification_status=1
            ).order_by('date_of_upload')

            movie_episode_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                movie_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_episode_data'] = movie_episode_data


            # fetching free content details for the movie
            all_video_id = FreeMovieVideo.objects.filter(
                movie_id=movie,
                verification_status=1,
            ).values('video_id')
            all_tags_data = FreeMovieVideoTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the free content that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching free content ordered by their date of upload
            episode_details = FreeMovieVideo.objects.filter(
                movie_id=movie,
                verification_status=1
            ).order_by('date_of_upload')

            movie_content_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                movie_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_content_data'] = movie_content_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# get all the pending series
@csrf_exempt
@login_required(login_url='home_page')
def get_movies(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # response object to return as response to ajax request
        context = {
            'is_any_pending_movie_exists': '',
            'is_successful': '',
            'pending_movies_data': '',
        }

        # fetching series id of all those series whose any season is in pending stage
        pending_movies_id = MovieVideo.objects.filter(verification_status=1).values('movie_id__movie_id').distinct().union(
            FreeMovieVideo.objects.filter(verification_status=1).values('movie_id__movie_id').distinct()
        )

        if pending_movies_id is None:
            context['is_any_pending_movie_exists'] = 'There are no pending movies to verify!!'
        else:
            # fetching movies details of pending movies
            pending_movies_details = MovieDetails.objects.filter(movie_id__in=pending_movies_id).order_by('date_of_creation')

            # fetching all subcategories for the movies that are to be included
            all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=pending_movies_id)
            subcategory_data = {}
            for obj in pending_movies_id:
                subcategory_data.update({obj['movie_id__movie_id']: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # sending movies details to ajax request
            pending_movies_data = {}
            for obj in pending_movies_details:
                pending_movies_data.update({str(obj.pk): (obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], obj.provider_id.username)})

            # returning success response to ajax request
            context['pending_movies_data'] = pending_movies_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


def video_status_email(video_type, provider_username, provider_email, video_name, season_no, series_name, movie_name, status):

    # Sending email process starts
    if video_type == 'series_episode':
        mail_subject = 'Series episode video status'
    elif video_type == 'series_content':
        mail_subject = 'Series content video status'
    elif video_type == 'movies_episode':
        mail_subject = 'Movie episode video status'
    elif video_type == 'movies_content':
        mail_subject = 'Movie content video status'
    else:
        return

    email_context = {
        'provider': provider_username,
        'message': ''
    }

    if video_type == 'series_episode':
        email_context['message'] = 'Episode ' + video_name + ' for season ' + str(season_no) + ' in series ' + series_name + ' is ' + status
    elif video_type == 'series_content':
        email_context['message'] = 'Content ' + video_name + ' for season ' + str(season_no) + ' in series ' + series_name + ' is ' + status
    elif video_type == 'movies_episode':
        email_context['message'] = 'Movie video ' + video_name + ' in movie ' + movie_name + ' is ' + status
    elif video_type == 'movies_content':
        email_context['message'] = 'Movie content ' + video_name + ' in movie ' + movie_name + ' is ' + status

    # message to be displayed to user is render from a html template
    html_message = render_to_string("Admin/video_status_template.html",
                                    context=email_context)
    to_email_list = [provider_email]
    # calling the send email function to send verification email and checking if mail is sent successfully
    if send_email(subject=mail_subject,
                html_message=html_message,
                to_email=to_email_list):  # to_email must be a tuple of list

        response = f'A video Confirmation email has been sent to {provider_email}.'
    else:
        response = 'Mail can\'t be send now. Possible Cause - Connection Issue.'



# function to verify video uploaded by the provider
@csrf_exempt
@login_required(login_url='home_page')
def verify_video(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        video_type = json_data['type']
        cost_per_video = json_data['cost_per_video']

        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_video_already_evaluated': '',
            'is_cost_provided': '',
            'is_successful': '',
            'video_id': '',
        }

        # checking if video exists or not
        if video_type == 'series_episode':
            video_details = SeriesVideos.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'series_content':
            video_details = FreeSeriesVideos.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'movies_episode':
            video_details = MovieVideo.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'movies_content':
            video_details = FreeMovieVideo.objects.filter(video_id__video_id=video_id).first()
        else:
            context['is_video_exists'] = 'Unidentified type of video.'
            return JsonResponse(context)

        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            # checking if video already evaluated or not
            if video_details.verification_status != 1:
                context['is_video_already_evaluated'] = 'This video has already been evaluated.'
            else:
                # checking if cost is provided or not
                if cost_per_video == '' and (video_type == 'series_episode' or video_type == 'movies_episode'):
                    context['is_cost_provided'] = 'No cost is provided for the video.'
                    return JsonResponse(context)

                video_details.verification_status = 2
                if video_type == 'series_episode' or video_type == 'movies_episode':
                    video_details.cost_of_video = cost_per_video
                video_details.save()


                # checking if provider has his email registered with our website then send him confirmation of his uploaded video verification
                if video_type == 'series_episode' or video_type == 'series_content':
                    provider_username = video_details.series_season_id.series_id.provider_id.username
                    provider_email = video_details.series_season_id.series_id.provider_id.email
                    if provider_email != '':
                        video_status_email(video_type, provider_username, provider_email, video_details.video_name, video_details.series_season_id.season_no, video_details.series_season_id.series_id.series_name, '', 'verified')
                elif video_type == 'movie_episode' or video_type == 'movie_content':
                    provider_username = video_details.movie_id.provider_id.username
                    provider_email = video_details.movie_id.provider_id.email
                    if provider_email != '':
                        video_status_email(video_type, provider_username, provider_email, video_details.video_name, '', '', video_details.movie_id.movie_name, 'verified')


                # checking if all the episodes of current season are verified then make season status as verified
                if video_type == 'series_episode' or video_type == 'series_content':
                    series_season_id = video_details.series_season_id
                    pending_episodes = SeriesVideos.objects.filter(
                        series_season_id=series_season_id,
                        verification_status=1,
                    ).values('video_id').union(
                        FreeSeriesVideos.objects.filter(
                            series_season_id=series_season_id,
                            verification_status=1,
                        ).values('video_id')
                    )

                    rejected_episodes = SeriesVideos.objects.filter(
                        series_season_id=series_season_id,
                        verification_status=3,
                    ).values('video_id').union(
                        FreeSeriesVideos.objects.filter(
                            series_season_id=series_season_id,
                            verification_status=3,
                        ).values('video_id')
                    )

                    if pending_episodes is None:
                        series_season = SeriesSeasonDetails.objects.filter(
                            series_season_id=series_season_id.series_season_id
                        ).first()
                        if rejected_episodes is None:
                            series_season.verification_status = 2
                        else:
                            series_season.verification_status = 3
                        series_season.save()

                # returning success response to ajax request
                context['video_id'] = video_details.video_id.video_id
                context['is_successful'] = 'Video verified successfully!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# function to verify video uploaded by the provider
@csrf_exempt
@login_required(login_url='home_page')
def reject_video(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        video_type = json_data['type']
        comment = json_data['comment']
        # print(comment)
        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_video_already_evaluated': '',
            'is_comment_provided': '',
            'is_successful': '',
            'video_id': '',
        }

        # checking if video exists or not
        if video_type == 'series_episode':
            video_details = SeriesVideos.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'series_content':
            video_details = FreeSeriesVideos.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'movies_episode':
            video_details = MovieVideo.objects.filter(video_id__video_id=video_id).first()
        elif video_type == 'movies_content':
            video_details = FreeMovieVideo.objects.filter(video_id__video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            # checking if video already evaluated or not
            if video_details.verification_status != 1:
                context['is_video_already_evaluated'] = 'This video has already been evaluated.'
            else:
                # checking if comment is provided or not
                if comment == '':
                    context['is_comment_provided'] = 'No comment provided.'
                    return JsonResponse(context)

                video_details.verification_status = 3
                video_details.save()

                video_obj = Videos.objects.filter(video_id=video_id).first()
                comment_exists = VideoRejectionComment.objects.filter(video_id=video_obj).first()
                if comment_exists:
                    comment_exists.comment = comment
                    comment_exists.save()
                else:
                    video_comment = VideoRejectionComment.objects.create(
                        video_id=video_obj,
                        comment=comment
                    )
                    video_comment.save()


                # checking if provider has his email registered with our website then send him confirmation of his uploaded video verification
                if video_type == 'series_episode' or video_type == 'series_content':
                    provider_username = video_details.series_season_id.series_id.provider_id.username
                    provider_email = video_details.series_season_id.series_id.provider_id.email
                    if provider_email != '':
                        video_status_email(video_type, provider_username, provider_email, video_details.video_name, video_details.series_season_id.season_no, video_details.series_season_id.series_id.series_name, '', 'rejected')
                elif video_type == 'movie_episode' or video_type == 'movie_content':
                    provider_username = video_details.movie_id.provider_id.username
                    provider_email = video_details.movie_id.provider_id.email
                    if provider_email != '':
                        video_status_email(video_type, provider_username, provider_email, video_details.video_name, '', '', video_details.movie_id.movie_name, 'rejected')



                # checking if all the episodes of current season are verified then make season status as verified
                if video_type == 'series_episode' or video_type == 'series_content':
                    series_season_id = video_details.series_season_id
                    pending_episodes = SeriesVideos.objects.filter(
                        series_season_id=series_season_id,
                        verification_status=1,
                    ).values('video_id').union(
                        FreeSeriesVideos.objects.filter(
                            series_season_id=series_season_id,
                            verification_status=1,
                        ).values('video_id')
                    )

                    if pending_episodes is None:
                        series_season = SeriesSeasonDetails.objects.filter(
                            series_season_id=series_season_id.series_season_id
                        ).first()

                        series_season.verification_status = 3
                        series_season.save()

                # returning success response to ajax request
                context['video_id'] = video_details.video_id.video_id
                context['is_successful'] = 'Video rejected!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# get all the verified series
@csrf_exempt
@login_required(login_url='home_page')
def added_series(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # response object to return as response to ajax request
        context = {
            'is_any_verified_series_exists': '',
            'is_successful': '',
            'verified_series_data': '',
        }

        # fetching series id of all those series whose any season is in verified stage
        pending_series_id = SeriesVideos.objects.filter(verification_status=2).values('series_season_id__series_id').distinct().union(
            FreeSeriesVideos.objects.filter(verification_status=2).values('series_season_id__series_id').distinct()
        )
        if pending_series_id is None:
            context['is_any_verified_series_exists'] = 'There are no verified series!!'
        else:
            # fetching series details of verified series
            pending_series_details = SeriesDetails.objects.filter(series_id__in=pending_series_id).order_by('-date_of_creation')

            # fetching all subcategories for the series that are to be included
            all_subcategory_data = SeriesSubCategories.objects.filter(series_id__in=pending_series_id)
            subcategory_data = {}
            for obj in pending_series_id:
                subcategory_data.update({obj['series_season_id__series_id']: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.series_id.series_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # sending series details to ajax request
            pending_series_data = {}
            for obj in pending_series_details:
                pending_series_data.update({str(obj.pk): (obj.series_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), str(CATEGORY_REVERSE[obj.category]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], obj.provider_id.username)})

            # returning success response to ajax request
            context['verified_series_data'] = pending_series_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')


# returning previously uploaded and verified episodes for a season to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def added_episodes(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_season_id = json_data['series_season_id']

        # response object to return as response to ajax request
        context = {
            'is_series_season_exists': '',
            'is_successful': '',
            'season_episode_data': '',
            'season_content_data': '',
        }

        # checking if season of that series exists
        series_season = SeriesSeasonDetails.objects.filter(series_season_id=series_season_id).first()
        if series_season is None:
            context['is_series_season_exists'] = 'This season or series do not exists'
        else:

            # fetching episodes details for the season
            all_video_id = SeriesVideos.objects.filter(
                series_season_id=series_season,
                verification_status=2,
            ).values('video_id')
            all_tags_data = SeriesVideosTags.objects.filter(video_id__in=all_video_id).order_by('episode_no')

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            # fetching episodes ordered by their episode number
            episode_details = SeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2
            ).order_by('episode_no')

            season_episode_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_episode_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.episode_no, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_episode_data'] = season_episode_data


            # fetching episodes details for the season
            all_video_id = FreeSeriesVideos.objects.filter(
                series_season_id=series_season,
                verification_status=2,
            ).values('video_id')
            all_tags_data = FreeSeriesVideosTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching free content ordered by their date of upload
            episode_details = FreeSeriesVideos.objects.filter(
                series_season_id=series_season_id,
                verification_status=2
            ).order_by('date_of_upload')

            season_content_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                season_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release,  obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['season_content_data'] = season_content_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning previously uploaded and verified series seasons info to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def added_seasons(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        series_id = json_data['series_id']

        # response object to return as response to ajax request
        context = {
            'is_any_series_season_exists': '',
            'is_successful': '',
            'all_series_season_data': '',
        }

        # checking if any season exists for that series
        pending_series_season_id = SeriesVideos.objects.filter(
            verification_status=2,
            series_season_id__series_id=series_id,
        ).values('series_season_id__series_season_id').distinct().union(
            FreeSeriesVideos.objects.filter(
                verification_status=2,
                series_season_id__series_id=series_id,
            ).values('series_season_id__series_season_id').distinct()
        )
        if pending_series_season_id is None:
            context['is_any_series_season_exists'] = 'No verified season in this series.'
        else:
            all_series_seasons = SeriesSeasonDetails.objects.filter(
                series_season_id__in=pending_series_season_id,
            ).order_by('season_no')

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



# get all the verified movies
@csrf_exempt
@login_required(login_url='home_page')
def added_movies(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # response object to return as response to ajax request
        context = {
            'is_any_verified_movies_exists': '',
            'is_successful': '',
            'verified_movies_data': '',
        }

        # fetching movies id of all those movies whose any video is in verified stage
        pending_movies_id = MovieVideo.objects.filter(verification_status=2).values('movie_id__movie_id').distinct().union(
            FreeMovieVideo.objects.filter(verification_status=2).values('movie_id__movie_id').distinct()
        )
        if pending_movies_id is None:
            context['is_any_verified_movies_exists'] = 'There are no verified movies!!'
        else:
            # fetching movies details of verified movie
            pending_movies_details = MovieDetails.objects.filter(movie_id__in=pending_movies_id).order_by('-date_of_creation')

            # fetching all subcategories for the movies that are to be included
            all_subcategory_data = MovieSubCategories.objects.filter(movie_id__in=pending_movies_id)
            subcategory_data = {}
            for obj in pending_movies_id:
                subcategory_data.update({obj['movie_id__movie_id']: []})

            for sub_cat in all_subcategory_data:
                subcategory_data[sub_cat.movie_id.movie_id].append(SUBCATEGORY_REVERSE[sub_cat.sub_category].title())

            # sending movies details to ajax request
            verified_movies_data = {}
            for obj in pending_movies_details:
                verified_movies_data.update({str(obj.pk): (obj.movie_name, obj.description, str(LANGUAGE_REVERSE[obj.language]).title(), obj.date_of_creation, obj.thumbnail_image.url, subcategory_data[obj.pk], obj.provider_id.username)})

            # returning success response to ajax request
            context['verified_movies_data'] = verified_movies_data
            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



# returning previously uploaded and verified videos for a movie to ajax request
@csrf_exempt
@login_required(login_url='home_page')
def added_movie_videos(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        movie_id = json_data['movie_id']

        # response object to return as response to ajax request
        context = {
            'is_movie_exists': '',
            'is_successful': '',
            'movie_video_data': '',
            'movie_content_data': '',
        }

        # checking if season of that series exists
        movie = MovieDetails.objects.filter(movie_id=movie_id).first()
        if movie is None:
            context['is_movie_exists'] = 'This movie do not exists.'
        else:

            # fetching episodes details for the season
            all_video_id = MovieVideo.objects.filter(
                movie_id=movie,
                verification_status=2,
            ).values('video_id')
            all_tags_data = MovieVideoTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)

            # fetching movie video
            episode_details = MovieVideo.objects.filter(
                movie_id=movie_id,
                verification_status=2
            )

            movie_video_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                movie_video_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release, obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_video_data'] = movie_video_data


            # fetching episodes details for the season
            all_video_id = FreeMovieVideo.objects.filter(
                movie_id=movie,
                verification_status=2,
            ).values('video_id')
            all_tags_data = FreeMovieVideoTags.objects.filter(video_id__in=all_video_id)

            # fetching all tags for the episodes that are to be included
            tags_data = {}
            for obj in all_video_id:
                tags_data.update({obj['video_id']: []})

            for tag in all_tags_data:
                tags_data[tag.video_id.video_id].append(tag.tag_word)


            # fetching free content ordered by their date of upload
            episode_details = FreeMovieVideo.objects.filter(
                movie_id=movie_id,
                verification_status=2
            ).order_by('date_of_upload')

            movie_content_data = {}
            for obj in episode_details:

                # getting firebase url for uploaded video file
                path_on_cloud = 'videos/' + obj.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[obj.extension]
                firebase_video_url = storage.child(path_on_cloud).get_url(obj.firebase_token)

                movie_content_data.update({str(obj.pk): (obj.video_id.video_id, obj.video_name, obj.description, obj.thumbnail_image.url, firebase_video_url, obj.date_of_release,  obj.duration_of_video, str(VERIFICATION_REVERSE[obj.verification_status]).title(), tags_data[obj.video_id.video_id])})

            # returning success response to ajax request
            context['movie_content_data'] = movie_content_data

            context['is_successful'] = 'Result Found!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')