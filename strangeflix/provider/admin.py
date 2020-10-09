from django.contrib import admin
from .models import Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos, \
                    SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo, \
                    FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo


# Register your models here.
admin.site.register(Videos)
admin.site.register(SeriesDetails)
admin.site.register(SeriesSubCategories)
admin.site.register(SeriesSeasonDetails)
admin.site.register(SeriesVideos)
# admin.site.register(SeriesVideosSubCategories)
admin.site.register(SeriesVideosTags)
admin.site.register(MovieDetails)
admin.site.register(MovieSubCategories)
admin.site.register(MovieVideoTags)
# admin.site.register(MoviesVideoSubCategories)
admin.site.register(MovieVideo)
# admin.site.register(FreeSeriesVideosSubCategories)
admin.site.register(FreeSeriesVideosTags)
admin.site.register(FreeSeriesVideos)
# admin.site.register(FreeMovieVideoSubCategories)
admin.site.register(FreeMovieVideoTags)
admin.site.register(FreeMovieVideo)
