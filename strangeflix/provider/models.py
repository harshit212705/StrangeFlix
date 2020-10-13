from django.db import models
from accounts.models import CustomUser as User

# NAME OF ALL MODELS PRESENT IN THIS FILE
# Videos, SeriesDetails, SeriesSubCategories, SeriesSeasonDetails, SeriesVideos,
# SeriesVideosTags, MovieDetails, MovieSubCategories, MovieVideoTags, MovieVideo,
# FreeSeriesVideosTags, FreeSeriesVideos, FreeMovieVideoTags, FreeMovieVideo


# NAME OF COMMENTED TABLES
# SeriesVideosSubCategories, MoviesVideoSubCategories, FreeSeriesVideosSubCategories, FreeMovieVideoSubCategories

SUB_CATEGORY_TYPES = (

    # TYPES OF SUBCATEGORIES
    (1, 'cricket'),
    (2, 'football'),
    (3, 'tennis'),
    (4, 'martial arts'),
    (5, 'esports'),
    (6, 'hockey'),
    (7, 'badminton'),
    (8, 'wrestling'),
    (9, 'kabaddi'),
    (10, 'table tennis'),
    (11, 'action'),
    (12, 'adventure'),
    (13, 'animation'),
    (14, 'comedy'),
    (15, 'crime'),
    (16, 'drama'),
    (17, 'horror'),
    (18, 'romance'),
    (19, 'thriller')
)


VERIFICATION_STATUS_TYPES = (

    # TYPES OF VERIFICATION STATUS
    (1, 'pending'),
    (2, 'verified'),
    (3, 'rejected'),
    (4, 'not submitted')
)

VIDEO_EXTENSION_TYPES = (

    # TYPES OF VIDEO EXTENSIONS
    (1, 'mp4'),
    (2, 'mkv'),
    (3, 'flv'),
    (4, 'webm'),
    (5, 'ogg'),
)


VIDEO_QUALITY_TYPES = (

    # TYPES OF VIDEO QUALITY
    (1, '144'),
    (2, '240'),
    (3, '360'),
    (4, '480'),
    (5, '720'),
    (6, '1080')
)


LANGUAGES_TYPES = (

    # TYPES OF LANGUAGES
    (1, 'english'),
    (2, 'hindi'),
    (3, 'bengali'),
    (4, 'kannada'),
    (5, 'malayalam'),
    (6, 'marathi'),
    (7, 'tamil'),
    (8, 'telugu')
)

# function returning save location for series thumbnail image
def series_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / series_<id>/<filename>
    return 'series_{0}/{1}'.format(instance.series_id, filename)


# function returning save location for series season thumbnail image
def series_season_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / series_<id>/<filename>
    return 'series_season_{0}/{1}'.format(instance.series_season_id, filename)


# function returning save location for movie thumbnail image
def movie_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / series_<id>/<filename>
    return 'movie_{0}/{1}'.format(instance.movie_id, filename)


# function returning save location for video or episode thumbnail image
def video_thumbnail_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / series_<id>/<filename>
    return 'video_{0}/{1}'.format(instance.video_id, filename)


# model for storing reference to video file and the type of video
class Videos(models.Model):

    VIDEO_TYPES = (

        # TYPES OF VIDEOS
        (1, 'free'),
        (2, 'series'),
        (3, 'movie')
    )

    video_id = models.AutoField(primary_key=True)

    video_type = models.PositiveSmallIntegerField(choices=VIDEO_TYPES)

    class Meta:
        verbose_name_plural = "Videos"



# model for storing series video tags
class VideoRejectionComment(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    comment = models.TextField()

    class Meta:
        verbose_name_plural = "Video Rejection Comment"



# model for storing series details
class SeriesDetails(models.Model):

    CATEGORY_TYPES = (

        # TYPES OF CATEGORY
        (1, 'sports'),
        (2, 'entertainment'),
    )

    series_id = models.AutoField(primary_key=True)

    provider_id = models.ForeignKey(User, on_delete=models.PROTECT)

    series_name = models.CharField(max_length=100)

    description = models.TextField()

    language = models.PositiveSmallIntegerField(choices=LANGUAGES_TYPES)

    category = models.PositiveSmallIntegerField(choices=CATEGORY_TYPES)

    date_of_creation = models.DateTimeField()

    thumbnail_image = models.ImageField(upload_to=series_thumbnail_directory_path)

    class Meta:
        verbose_name_plural = "Series Details"


# model for storing series sub categories
class SeriesSubCategories(models.Model):

    series_id = models.ForeignKey(SeriesDetails, on_delete=models.PROTECT)

    sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

    class Meta:
        verbose_name_plural = "Series Sub Categories"


# model for storing series season details
class SeriesSeasonDetails(models.Model):

    series_season_id = models.AutoField(primary_key=True)

    series_id = models.ForeignKey(SeriesDetails, on_delete=models.PROTECT)

    season_no = models.PositiveSmallIntegerField()

    description = models.TextField()

    date_of_creation = models.DateTimeField()

    thumbnail_image = models.ImageField(upload_to=series_season_thumbnail_directory_path)

    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS_TYPES)

    class Meta:
        verbose_name_plural = "Series Season Details"


# model for storing series videos
class SeriesVideos(models.Model):

    series_season_id = models.ForeignKey(SeriesSeasonDetails, on_delete=models.PROTECT)

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    video_name = models.CharField(max_length=100)

    firebase_save_name = models.CharField(max_length=50)

    firebase_token = models.CharField(max_length=50)

    description = models.TextField()

    thumbnail_image = models.ImageField(upload_to=video_thumbnail_directory_path)

    date_of_upload = models.DateTimeField()

    date_of_release = models.DateTimeField()

    episode_no = models.PositiveSmallIntegerField()

    duration_of_video = models.IntegerField()

    quality_of_video = models.PositiveSmallIntegerField(choices=VIDEO_QUALITY_TYPES)

    extension = models.PositiveSmallIntegerField(choices=VIDEO_EXTENSION_TYPES, default=1)

    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS_TYPES)

    cost_of_video = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Series Videos"



# class SeriesVideosSubCategories(models.Model):

#     video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

#     episode_no = models.PositiveSmallIntegerField()

#     sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

#     class Meta:
#         verbose_name_plural = "Series Videos Sub Categories"


# model for storing series video tags
class SeriesVideosTags(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    episode_no = models.PositiveSmallIntegerField()

    tag_word = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Series Videos Tags"


# model for storing movie details
class MovieDetails(models.Model):

    movie_id = models.AutoField(primary_key=True)

    provider_id = models.ForeignKey(User, on_delete=models.PROTECT)

    movie_name = models.CharField(max_length=100)

    description = models.TextField()

    language = models.PositiveSmallIntegerField(choices=LANGUAGES_TYPES)

    date_of_creation = models.DateTimeField()

    thumbnail_image = models.ImageField(upload_to=movie_thumbnail_directory_path)

    class Meta:
        verbose_name_plural = "Movie Details"



# model for storing movie sub categories
class MovieSubCategories(models.Model):

    movie_id = models.ForeignKey(MovieDetails, on_delete=models.PROTECT)

    sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

    class Meta:
        verbose_name_plural = "Movie Sub Categories"


# model for storing movie video tags
class MovieVideoTags(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    tag_word = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Movie Video Tags"



# class MoviesVideoSubCategories(models.Model):

#     video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

#     sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

#     class Meta:
#         verbose_name_plural = "Movie Video Sub Categories"


# model for storing movie video
class MovieVideo(models.Model):

    movie_id = models.ForeignKey(MovieDetails, on_delete=models.PROTECT)

    video_name = models.CharField(max_length=100)

    description = models.TextField()

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    firebase_save_name = models.CharField(max_length=50)

    firebase_token = models.CharField(max_length=50)

    thumbnail_image = models.ImageField(upload_to=video_thumbnail_directory_path)

    date_of_upload = models.DateTimeField()

    date_of_release = models.DateTimeField()

    duration_of_video = models.IntegerField()

    quality_of_video = models.PositiveSmallIntegerField(choices=VIDEO_QUALITY_TYPES)

    extension = models.PositiveSmallIntegerField(choices=VIDEO_EXTENSION_TYPES, default=1)

    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS_TYPES)

    cost_of_video = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Movie Video"



# class FreeSeriesVideosSubCategories(models.Model):

#     video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

#     sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

#     class Meta:
#         verbose_name_plural = "Free Series Videos Sub Categories"


# model for storing series free video tags
class FreeSeriesVideosTags(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    tag_word = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Free Series Videos Tags"


# model for storing series free video
class FreeSeriesVideos(models.Model):

    series_season_id = models.ForeignKey(SeriesSeasonDetails, on_delete=models.PROTECT)

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    video_name = models.CharField(max_length=100)

    firebase_save_name = models.CharField(max_length=50)

    firebase_token = models.CharField(max_length=50)

    description = models.TextField()

    thumbnail_image = models.ImageField(upload_to=video_thumbnail_directory_path)

    date_of_upload = models.DateTimeField()

    date_of_release = models.DateTimeField()

    duration_of_video = models.IntegerField()

    quality_of_video = models.PositiveSmallIntegerField(choices=VIDEO_QUALITY_TYPES)

    extension = models.PositiveSmallIntegerField(choices=VIDEO_EXTENSION_TYPES, default=1)

    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS_TYPES)

    class Meta:
        verbose_name_plural = "Free Series Videos"



# class FreeMovieVideoSubCategories(models.Model):

#     video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

#     sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

#     class Meta:
#         verbose_name_plural = "Free Movie Video Sub Categories"


# model for storing movie free video tags
class FreeMovieVideoTags(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    tag_word = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Free Movie Video Tags"


# model for storing movie free video
class FreeMovieVideo(models.Model):

    movie_id = models.ForeignKey(MovieDetails, on_delete=models.PROTECT)

    video_name = models.CharField(max_length=100)

    description = models.TextField()

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    firebase_save_name = models.CharField(max_length=50)

    firebase_token = models.CharField(max_length=50)

    thumbnail_image = models.ImageField(upload_to=video_thumbnail_directory_path)

    date_of_upload = models.DateTimeField()

    date_of_release = models.DateTimeField()

    duration_of_video = models.IntegerField()

    quality_of_video = models.PositiveSmallIntegerField(choices=VIDEO_QUALITY_TYPES)

    extension = models.PositiveSmallIntegerField(choices=VIDEO_EXTENSION_TYPES, default=1)

    verification_status = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS_TYPES)

    class Meta:
        verbose_name_plural = "Free Movie Video"