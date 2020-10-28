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

    def __str__(self):
        return str('Video_id--') + str(self.video_id) + str(' || Video_type--') + str(self.video_type)



# model for storing series video tags
class VideoRejectionComment(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    comment = models.TextField()

    class Meta:
        verbose_name_plural = "Video Rejection Comment"

    def __str__(self):
        return str('Video_id--') + str(self.video_id.video_id) + str(' || comment--') + str(self.comment)



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

    def __str__(self):
        return str('Series_id--') + str(self.series_id) + str(' || Series--') + str(self.series_name) + str(' || Provider--') + str(self.provider_id.username)


# model for storing series sub categories
class SeriesSubCategories(models.Model):

    series_id = models.ForeignKey(SeriesDetails, on_delete=models.PROTECT)

    sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

    class Meta:
        verbose_name_plural = "Series Sub Categories"

    def __str__(self):
        return str('Series_id--') + str(self.series_id.series_id) + str(' || Series--') + str(self.series_id.series_name) + str(' || Subcategory--') + str(SUB_CATEGORY_TYPES[self.sub_category-1][1])


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

    def __str__(self):
        return str('Series--') + str(self.series_id.series_name) + str(' || Series_season_id--') + str(self.series_season_id) + str(' || Season_no--') + str(self.season_no) + str(' || Status--') + str(self.verification_status)


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

    def __str__(self):
        return str('Series_id--') + str(self.series_season_id.series_id.series_id) + str(' || Series--') + str(self.series_season_id.series_id.series_name) + str(' || Season_no--') + str(self.series_season_id.season_no) + str(' || Episode_no--') + str(self.episode_no) + str(' || video_id--') + str(self.video_id.video_id) + str(' || Video_name--') + str(self.video_name) + str(' || Status--') + str(self.verification_status)



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

    def __str__(self):
        return str('video_id--') + str(self.video_id.video_id) + str(' || Episode_no--') + str(self.episode_no) + str(' || tag--') + str(self.tag_word)


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

    def __str__(self):
        return str('Movie_id--') + str(self.movie_id) + str(' || Movie--') + str(self.movie_name) + str(' || Provider--') + str(self.provider_id.username)



# model for storing movie sub categories
class MovieSubCategories(models.Model):

    movie_id = models.ForeignKey(MovieDetails, on_delete=models.PROTECT)

    sub_category = models.PositiveSmallIntegerField(choices=SUB_CATEGORY_TYPES)

    class Meta:
        verbose_name_plural = "Movie Sub Categories"

    def __str__(self):
        return str('Movie_id--') + str(self.movie_id.movie_id) + str(' || Movie--') + str(self.movie_id.movie_name) + str(' || Subcategory--') + str(SUB_CATEGORY_TYPES[self.sub_category-1][1])


# model for storing movie video tags
class MovieVideoTags(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    tag_word = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Movie Video Tags"

    def __str__(self):
        return str('video_id--') + str(self.video_id.video_id) + str(' || tag--')  + str(self.tag_word)



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

    def __str__(self):
        return str('Movie_id--') + str(self.movie_id.movie_id) + str(' || Movie--') + str(self.movie_id.movie_name) + str(' || video_id--') + str(self.video_id.video_id) + str(' || Video_name--') + str(self.video_name) + str(' || Status--') + str(self.verification_status)



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

    def __str__(self):
        return str('video_id--') + str(self.video_id.video_id) + str(' || tag--') + str(self.tag_word)


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

    def __str__(self):
        return str('Series_id--') + str(self.series_season_id.series_id.series_id) + str(' || Series--') + str(self.series_season_id.series_id.series_name) + str(' || Season_no--') + str(self.series_season_id.season_no) + str(' || video_id--') + str(self.video_id.video_id) + str(' || Video_name--') + str(self.video_name) + str(' || Status--') + str(self.verification_status)



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

    def __str__(self):
        return str('video_id--') + str(self.video_id.video_id) + str(' || tag--') + str(self.tag_word)


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

    def __str__(self):
        return str('Movie_id--') + str(self.movie_id.movie_id) + str(' || Movie--') + str(self.movie_id.movie_name) + str(' || video_id--') + str(self.video_id.video_id) + str(' || Video_name--') + str(self.video_name) + str(' || Status--') + str(self.verification_status)



# model for storing series rating given by user
class SeriesRating(models.Model):

    series_id = models.ForeignKey(SeriesDetails, on_delete=models.PROTECT)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Series Rating"

    def __str__(self):
        return str('Series_id--') + str(self.series_id.series_id) + str(' || Series--') + str(self.series_id.series_name) + str(' || User--') + str(self.user_id.username) + str(' || rating--') + str(self.rating)



# model for storing movie rating given by user
class MovieRating(models.Model):

    movie_id = models.ForeignKey(MovieDetails, on_delete=models.PROTECT)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Movie Rating"

    def __str__(self):
        return str('Movie_id--') + str(self.movie_id.movie_id) + str(' || Movie--') + str(self.movie_id.movie_name) + str(' || User--') + str(self.user_id.username) + str(' || rating--') + str(self.rating)


# model for storing user History
class History(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    video_watched = models.PositiveSmallIntegerField()

    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "History"

    def __str__(self):
        return str('User--') + str(self.user_id.username) + str(' || video_id--') + str(self.video_id.video_id) + str(' || watch_time--') + str(self.video_watched)


# model for storing video comments on videos
class VideoComment(models.Model):

    COMMENT_TYPES = (
        # TYPES OF COMMENTS
        (1, 'positive'),
        (2, 'negative'),
        (3, 'neutral'),
    )

    comment_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    comment = models.TextField()

    comment_type = models.PositiveSmallIntegerField(choices=COMMENT_TYPES, default=1)

    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Video Comment"

    def __str__(self):
        return str('User--') + str(self.user_id.username) + str(' || video_id--') + str(self.video_id.video_id) + str(' || comment--') + str(self.comment) + str(' || comment_type--') + str(self.comment_type)



# model for storing reports on comments
class ReportComment(models.Model):

    REPORT_COMMENT_TYPES = (
        # TYPES OF COMMENT REPORTING
        (1, 'Unwanted commercial content or spam'),
        (2, 'Sexually explicit material'),
        (3, 'Child abuse'),
        (4, 'Hate speech or graphic violence'),
        (5, 'Harassment or bullying'),
    )

    comment_id = models.ForeignKey(VideoComment, on_delete=models.PROTECT)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    flag_val = models.PositiveSmallIntegerField(choices=REPORT_COMMENT_TYPES, default=1)

    class Meta:
        verbose_name_plural = "Report Comment"

    def __str__(self):
        return str('User--') + str(self.user_id.username) + str(' || comment_id--') + str(self.comment_id.pk) + str(' || flag_val--') + str(self.flag_val)



# model for storing reports on videos
class ReportVideo(models.Model):

    REPORT_VIDEO_TYPES = (
        # TYPES OF VIDEO REPORTING
        (1, 'Violent or repulsive content'),
        (2, 'Hateful or abusive content'),
        (3, 'Harmful or dangerous act'),
        (4, 'Sexual content'),
        (5, 'Child abuse'),
        (6, 'Promotes terrorism'),
        (7, 'Spam or misleading'),
        (8, 'Infringes my rights'),
        (9, 'Captions issue'),
    )

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    flag_val = models.PositiveSmallIntegerField(choices=REPORT_VIDEO_TYPES, default=1)

    class Meta:
        verbose_name_plural = "Report Video"

    def __str__(self):
        return str('User--') + str(self.user_id.username) + str(' || video_id--') + str(self.video_id.video_id) + str(' || flag_val--') + str(self.flag_val)


# model for storing user faviurites
class Favourites(models.Model):

    video_id = models.ForeignKey(Videos, on_delete=models.PROTECT)

    users = models.ManyToManyField(User, related_name='favourites')

    class Meta:
        verbose_name_plural = "Favourites"

    def __str__(self):
        return str('video_id--') + str(self.video_id.video_id)
