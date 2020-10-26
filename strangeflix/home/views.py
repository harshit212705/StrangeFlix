# importing models from provider/models.py
from provider.models import Videos, SeriesDetails, SeriesSubCategories, MovieDetails, MovieSubCategories

from django.shortcuts import render
from django.views.generic import View
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from subscribe.models import Subscriptions
from datetime import datetime
from django.utils import timezone

from .recommendations import recommend_movies, recommend_series, recent_movies_suggestion, \
    recent_series_suggestion, popular_movies_suggestion, popular_series_suggestion
from provider.views import LANGUAGE_REVERSE, SUBCATEGORY_REVERSE, CATEGORY_REVERSE



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


