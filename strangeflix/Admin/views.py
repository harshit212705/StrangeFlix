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
        pending_series_id = SeriesVideos.objects.filter(verification_status=1).values('series_season_id__series_id').distinct()
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
        ).values('series_season_id__series_season_id').distinct()
        if pending_series_season_id is None:
            context['is_any_series_season_exists'] = 'You have not added any season for this series yet. Add new season now.'
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



# function to verify video uploaded by the provider
@csrf_exempt
@login_required(login_url='home_page')
def verify_video(request):
    if request.method == 'POST' and request.user.user_type == 'A':

        # extracting form data coming from ajax request
        json_data = json.loads(request.POST['data'])
        video_id = json_data['video_id']
        cost_per_video = json_data['cost_per_video']
        # print(cost_per_video)
        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_video_already_evaluated': '',
            'is_cost_provided': '',
            'is_successful': '',
            'episode_no': '',
        }

        # checking if video exists or not
        video_details = SeriesVideos.objects.filter(video_id__video_id=video_id).first()
        if video_details is None:
            context['is_video_exists'] = 'This video does not exists.'
        else:
            # checking if video already evaluated or not
            if video_details.verification_status != 1:
                context['is_video_already_evaluated'] = 'This video has already been evaluated.'
            else:
                # checking if comment is provided or not
                if cost_per_video == '':
                    context['is_cost_provided'] = 'No cost for video provided.'
                    return JsonResponse(context)

                video_details.verification_status = 2
                video_details.cost_of_video = cost_per_video
                video_details.save()

                # checking if all the episodes of current season are verified then make season status as verified
                series_season_id = video_details.series_season_id
                pending_episodes = SeriesVideos.objects.filter(
                    series_season_id=series_season_id,
                    verification_status=1,
                ).first()

                rejected_episodes = SeriesVideos.objects.filter(
                    series_season_id=series_season_id,
                    verification_status=3,
                ).first()

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
                context['episode_no'] = video_details.episode_no
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
        comment = json_data['comment']
        # print(comment)
        # response object to return as response to ajax request
        context = {
            'is_video_exists': '',
            'is_video_already_evaluated': '',
            'is_comment_provided': '',
            'is_successful': '',
            'episode_no': '',
        }

        # checking if video exists or not
        video_details = SeriesVideos.objects.filter(video_id__video_id=video_id).first()
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
                video_comment = VideoRejectionComment.objects.create(
                    video_id=video_obj,
                    comment=comment
                )
                video_comment.save()

                # checking if all the episodes of current season are verified then make season status as verified
                series_season_id = video_details.series_season_id
                pending_episodes = SeriesVideos.objects.filter(
                    series_season_id=series_season_id,
                    verification_status=1,
                ).first()

                rejected_episodes = SeriesVideos.objects.filter(
                    series_season_id=series_season_id,
                    verification_status=3,
                ).first()

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
                context['episode_no'] = video_details.episode_no
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
        pending_series_id = SeriesVideos.objects.filter(verification_status=2).values('series_season_id__series_id').distinct()
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
        ).values('series_season_id__series_season_id').distinct()
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
