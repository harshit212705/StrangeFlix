// custom-select
// series-category
var entsel = document.querySelectorAll("#chkbxo");
var txtval = document.querySelector("#movie__subcategory__choosen");
var chkb = document.querySelector("#savecho");
chkb.addEventListener('click', function (e) {
    txtval.value = "";
    entsel.forEach(element => {
        if (element.checked) {
            txtval.value += element.value + ",";
        }
    });
});

$("#list-movie-list").on('click', function (e) {
    $('#list-movieform-list').css('pointer-events', 'all');
    $('#list-movieinfo-list').css('pointer-events', 'none');
    $('#list-movieform-list').tab('show');

    //reset seasonForm
    $('#movieForm').each(function () {
        this.reset();
    });
    // reset seriesForm
    $('#movieinfoForm').each(function () {
        this.reset();
    });
    $('.a-m-list').css('display','block');
    txtval.value = "";

    $('#season-right').css('display', 'none');
    $('#content-right').css('display', 'none');
    $('#episode-right').css('display', 'none');
    $('#series-right').css('display', 'none');
    $('#add-season-right').css('display', 'none');
    $('#add-episode-right').css('display', 'none');
    $('#add-content-right').css('display', 'none');
});


$("#list-added-movie-list").on('click', function (e) {
    $('#list-added-movieform-list').css('pointer-events', 'all');
    $('#list-added-movieinfo-list').css('pointer-events', 'none');
    $('#list-added-movieform-list').tab('show');

    //reset seasonForm
    $('#add-movieForm').each(function () {
        this.reset();
    });
    // reset seriesForm
    $('#add-movieinfoForm').each(function () {
        this.reset();
    });
    $('.a-m-list').css('display','none');
    txtval.value = "";

    $('#season-right').css('display', 'none');
    $('#content-right').css('display', 'none');
    $('#episode-right').css('display', 'none');
    $('#series-right').css('display', 'none');
    $('#add-season-right').css('display', 'none');
    $('#add-episode-right').css('display', 'none');
    $('#add-content-right').css('display', 'none');
});

// ajax call for posting movie form 

$("#movieForm").submit(function (e) {
    e.preventDefault(); //prevent default action

    // Extracting Form Data
    var movie_name = document.getElementById('movie_name').value;
    var movie_description = document.getElementById('movie__description').value;
    var language = document.getElementById('movie__language').value;
    var category = document.getElementById('movie__category').value;
    var subcategory = document.getElementById('movie__subcategory__choosen').value;
    var thumbnail_image = $('#movie__file')[0].files[0];

    // javascript data object
    var data = {
        'movie_name': movie_name,
        'movie_description': movie_description,
        'language': language,
        'category': category,
        'subcategory': subcategory,
    }

    // adding data to javascript form which is to be send over ajax request
    var formData = new FormData();
    formData.append('data', JSON.stringify(data));
    formData.append('file', thumbnail_image, thumbnail_image.name);
    $('#movie-submit').attr('disabled', true);
    $.ajax({
        type: 'POST',
        url: '',
        data: formData,
        dataType: 'json',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function (data) {
            $('#movie-submit').attr('disabled', false);
            // checking and handling error conditions
            if (data.is_series_exists != '') {
                alert(data.is_series_exists);
            } else if (data.is_language_selected != '') {
                alert(data.is_language_selected);
            } else if (data.is_category_selected != '') {
                alert(data.is_category_selected);
            } else if (data.is_subcategory_selected != '') {
                alert(data.is_subcategory_selected);
            } else if (data.is_thumbnail_too_large != '') {
                alert(data.is_thumbnail_too_large);
            } else if (data.is_thumbnail_mimetype_problem != '') {
                alert(data.is_thumbnail_mimetype_problem);
            } else if (data.is_successful != '') {

                // setting series_id for the series created
                document.getElementById('movie_id').innerHTML = data.movie_id;

                alert(data.is_successful);

                // restricting pointer events for other tabs
                $('#list-movieform-list').css('pointer-events', 'none');
                $('#list-movieinfo-list').css('pointer-events', 'all');
                $('#list-movieinfo-list').tab('show');
                $('#season-right').css('display', 'none');
                $('#content-right').css('display', 'none');
                $('#episode-right').css('display', 'none');
                $('#series-right').css('display', 'none');
                $('#add-season-right').css('display', 'none');
                $('#add-episode-right').css('display', 'none');
                $('#add-content-right').css('display', 'none');


            } else {
                alert('Some unexpected error has occured. Try again.');
            }
        }
    });
});


// submitting new movie form using ajax call
$("#movievideoForm").submit(function (e) {
    e.preventDefault(); //prevent default action

    // Extracting Form Data
    var movie_id = document.getElementById('movie_id').innerHTML;
    var movie_name = document.getElementById('movie__videoname').value;
    var movie_description = document.getElementById('movie__videodescription').value;
    // var episode_tags = document.getElementById('series__season__episodetags').value;
    var movie_tags = "";
    $('#m-selected-tags span').each(function () {
        movie_tags += $(this).attr("value");
        movie_tags += ",";
    });
    movie_tags = movie_tags.substring(0, movie_tags.length - 1);

    var movie_quality = document.getElementById('m-video_quality').value;
    var movie_release_date = document.getElementById('movie__videodate').value;
    var movie_linkorvideo = document.getElementById('m-linkorvideo').value;

    var movie_link = '';
    if (movie_linkorvideo == 'Link') {
        var movie_link = document.getElementById('movie-link').value;
    }

    // Files from episode form
    var thumbnail_image = $('#movie-file2')[0].files[0];
    var movie_video = $('#movie-video')[0].files[0];

    // javascript data object
    var data = {
        'movie_id': movie_id,
        'movie_name': movie_name,
        'movie_description': movie_description,
        'movie_tags': movie_tags,
        'movie_quality': movie_quality,
        'movie_release_date': movie_release_date,
        'movie_linkorvideo': movie_linkorvideo,
        'movie_link': movie_link,
    }

    // adding data to javascript form which is to be send over ajax request
    var formData = new FormData();
    formData.append('data', JSON.stringify(data));
    formData.append('file', thumbnail_image, thumbnail_image.name);
    formData.append('video', movie_video);

    $('#movie-submit').attr('disabled', true);

    $.ajax({
        type: 'POST',
        url: '',
        data: formData,
        dataType: 'json',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function (data) {
            $('#movie-submit').attr('disabled', false);
            // checking and handling error conditions
            if (data.is_series_season_exists != '') {
                alert(data.is_series_season_exists);
            } else if (data.is_episode_no_exists != '') {
                alert(data.is_episode_no_exists);
            } else if (data.is_quality_selected != '') {
                alert(data.is_quality_selected);
            } else if (data.is_release_date_future != '') {
                alert(data.is_release_date_future);
            } else if (data.is_thumbnail_too_large != '') {
                alert(data.is_thumbnail_too_large);
            } else if (data.is_thumbnail_mimetype_problem != '') {
                alert(data.is_thumbnail_mimetype_problem);
            } else if (data.is_video_mimetype_problem != '') {
                alert(data.is_video_mimetype_problem);
            } else if (data.is_successful != '') {
                $('.movie-oe-time').css('display','none');
                // appending the new episode to previously created episodes list
                // for (var key in data.season_episode_data) {
                //     var specialol = `'${data.season_episode_data[key][4]}'`;
                //     var htmlgen = '<div id="movie' + data.season_episode_data[key][6] +
                //         '" class="container my-5"><h4 class="my-4">Episode ' + data
                //         .season_episode_data[key][6] + '-' + data.season_episode_data[key][
                //             1
                //         ] +
                //         '</h4><div class="row"><div class="col-lg-8 col-md-8"><img id="episode' +
                //         data.season_episode_data[key][6] + 'thumbnail" src="' + data
                //         .season_episode_data[key][3] +
                //         '" alt="uploading" class="img-fluid"></div><div class="col-lg-4 col-md-4"><div class="content mx-5"><p class="text-muted">' +
                //         data.season_episode_data[key][2] + '</p><p class="text-muted">';

                //     for (var i = 0; i < data.season_episode_data[key][9].length; i++) {
                //         htmlgen += data.season_episode_data[key][9][i] + ' | ';
                //     }

                //     htmlgen += '</p><p class="text-muted">Status - ' + data
                //         .season_episode_data[key][8] +
                //         '</p><button type="button" class="btn btn-primary" onclick="play_video(' +
                //         data.season_episode_data[key][0] + ',' + specialol +
                //         ')" class="btn btn-primary btn-sm">Play video</button></div></div></div></div>';

                //     $('#uploaded_episodes').append(htmlgen);
                // }

                // // appending current episode to right navigation bar
                // $('#episodes-right').append('<li><a href="#episode' + episodecount +
                //     '">episode' + episodecount + '</a></li>');

                // // reset the form
                // $('#seasonepisodeForm').each(function () {
                //     this.reset();
                // });

                // // add season video form toggle
                // $('#seasonVideos').collapse('toggle');
                // // setting the episode number value
                // $('#series__season__episodeno').attr("value", episodecount + 1);

                // alert(data.is_successful);
            } else {
                alert('Some unexpected error has occured. Try again.');
            }
        }
    });
});