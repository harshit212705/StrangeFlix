// choosing subcategory in NEW MOVIE FORM in ADD CONTENT SECTION
var mentsel = document.querySelectorAll("#chkbxo");
var mtxtval = document.querySelector("#movie__subcategory__choosen");
var mchkb = document.querySelector("#savecho");
mchkb.addEventListener('click', function (e) {
    mtxtval.value = "";
    mentsel.forEach(element => {
        if (element.checked) {
            mtxtval.value += element.value + ",";
        }
    });
    if (mtxtval.value.length > 0) {
        mtxtval.value = mtxtval.value.substring(0, mtxtval.value.length - 1);
    }
});



// reset everything on clicking on MOVIES in ADD CONTENT SECTION IN LEFT NAVIGATION BAR
$("#list-movie-list").on('click', function (e) {

    // restricting pointer events for other tabs
    $('#list-movieform-list').css('pointer-events', 'all');
	$('#list-movieinfo-list').css('pointer-events', 'none');
	$('#list-movieform-list').tab('show');

	// reset seriesForm
	$('#movieForm').each(function () {
		this.reset();
	});

	//reset episodeForm
	$('#movievideoForm').each(function () {
		this.reset();
	});

	// reset free content form
	$('#moviefreecontentForm').each(function () {
		this.reset();
	});

	// Emptying previous movies details content
	$('#m-uploaded-free-contents').empty();
    $('#uploaded_movie').empty();

    // $('.a-m-list').css('display','block');

    // setting default empty value for category and subcategory
    txtval.value = "";

	set_navigation_bars_display('none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none');

});


// once moved to UPLOADED MOVIES SECTION IN ADDED CONTENT in MOVIES remove pointer events to ADD MOVIE CONTENT SECTION
$("#list-added-movieform-list").on('click', function (e) {
    $('#list-added-movieform-list').css('pointer-events', 'all');
    $('#list-added-movieinfo-list').css('pointer-events', 'none');
    $('#list-added-movieform-list').tab('show');

    //reset free movie content form
    $('#add-moviefreecontentForm').each(function () {
        this.reset();
    });

    // reset movie video form
    $('#add-movievideoForm').each(function () {
        this.reset();
    });

	set_navigation_bars_display('none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'block', 'none', 'none');
});



// handling ADD TAG in ADD MOVIE VIDEO SECTION of MOVIES IN ADD CONTENT SECTION
var maddTag = document.querySelector("#m-add-tag");
var mtagText = document.querySelector("#m-tag-text");
var mshowTags = document.querySelector("#m-selected-tags");
var mselectedTags = document.querySelectorAll("#m-tag-toggler");
maddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = mtagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="m-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	mshowTags.append(span);
	mselectedTags = document.querySelectorAll("#m-tag-toggler");
	mselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});



// handling ADD TAG in ADD FREE CONTENT SECTION of MOVIES IN ADD CONTENT SECTION
var cmaddTag = document.querySelector("#cm-add-tag");
var cmtagText = document.querySelector("#cm-tag-text");
var cmshowTags = document.querySelector("#cm-selected-tags");
var cmselectedTags = document.querySelectorAll("#cm-tag-toggler");
cmaddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = cmtagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="cm-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	cmshowTags.append(span);
	cmselectedTags = document.querySelectorAll("#cm-tag-toggler");
	cmselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});



// handling ADD TAG in ADD EPISODE SECTION of MOVIES IN ADDED CONTENT SECTION
var maddaddTag = document.querySelector("#m-add-add-tag");
var maddtagText = document.querySelector("#m-add-tag-text");
var maddshowTags = document.querySelector("#m-add-selected-tags");
var maddselectedTags = document.querySelectorAll("#m-add-tag-toggler");
maddaddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = maddtagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="m-add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	maddshowTags.append(span);
	maddselectedTags = document.querySelectorAll("#m-add-tag-toggler");
	maddselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});



// handling ADD TAG in ADD FREE CONTENT SECTION of MOVIES IN ADDED CONTENT SECTION
var cmaddaddTag = document.querySelector("#cm-add-add-tag");
var cmaddtagText = document.querySelector("#cm-add-tag-text");
var cmaddshowTags = document.querySelector("#cm-add-selected-tags");
var cmaddselectedTags = document.querySelectorAll("#cm-add-tag-toggler");
cmaddaddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = cmaddtagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="cm-add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	cmaddshowTags.append(span);
	cmaddselectedTags = document.querySelectorAll("#cm-add-tag-toggler");
	cmaddselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});


// handling selection between video or link in ADD EPISODE SECTION of MOVIES IN ADD CONTENT SECTION
var mlinkorvideo = document.querySelector('#m-linkorvideo');
var mepisodeVideo = document.querySelector('#movie-video');
var mepisodeLink = document.querySelector('#movie-link');
mlinkorvideo.addEventListener('change', function (e) {
	var cont = mlinkorvideo.options[mlinkorvideo.selectedIndex].value;
	if (cont != "Link") {
		mepisodeVideo.style.display = "block";
		mepisodeLink.value = "";
		mepisodeLink.style.display = "none";
	} else {
		mepisodeVideo.style.display = "none";
		mepisodeLink.style.display = "block";
		mepisodeVideo.value = "";
	}
});



// handling selection between video or link in ADD FREE CONTENT SECTION of MOVIES IN ADD CONTENT SECTION
var mfree_cont_linkorvideo = document.querySelector('#moviecontentlinkorvideo');
var mfree_cont_episodeVideo = document.querySelector('#movie-content-video');
var mfree_cont_episodeLink = document.querySelector('#movie-content-link');
mfree_cont_linkorvideo.addEventListener('change', function (e) {
	var cont = mfree_cont_linkorvideo.options[mfree_cont_linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		mfree_cont_episodeVideo.style.display = "block";
		mfree_cont_episodeLink.value = "";
		mfree_cont_episodeLink.style.display = "none";
	} else {
		mfree_cont_episodeVideo.style.display = "none";
		mfree_cont_episodeLink.style.display = "block";
		mfree_cont_episodeVideo.value = "";
	}
});



// handling selection between video or link in ADD EPISODE SECTION of MOVIES IN ADDED CONTENT SECTION
var madd__linkorvideo = document.querySelector('#m-add-linkorvideo');
var madd__episodeVideo = document.querySelector('#movie-add-video');
var madd__episodeLink = document.querySelector('#movie-add-link');
madd__linkorvideo.addEventListener('change', function (e) {
	var cont = madd__linkorvideo.options[madd__linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		madd__episodeVideo.style.display = "block";
		madd__episodeLink.value = "";
		madd__episodeLink.style.display = "none";
	} else {
		madd__episodeVideo.style.display = "none";
		madd__episodeLink.style.display = "block";
		madd__episodeVideo.value = "";
	}
});


// handling selection between video or link in ADD FREE CONTENT SECTION of MOVIES IN ADDED CONTENT SECTION
var mfree_cont_add__linkorvideo = document.querySelector('#movieaddcontentlinkorvideo');
var mfree_cont_add__episodeVideo = document.querySelector('#movie-add-content-video');
var mfree_cont_add__episodeLink = document.querySelector('#movie-add-content-link');
mfree_cont_add__linkorvideo.addEventListener('change', function (e) {
	var cont = mfree_cont_add__linkorvideo.options[mfree_cont_add__linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		mfree_cont_add__episodeVideo.style.display = "block";
		mfree_cont_add__episodeLink.value = "";
		mfree_cont_add__episodeLink.style.display = "none";
	} else {
		mfree_cont_add__episodeVideo.style.display = "none";
		mfree_cont_add__episodeLink.style.display = "block";
		mfree_cont_add__episodeVideo.value = "";
	}
});


// ajax call for posting movie form 

// $("#movieForm").submit(function (e) {
//     e.preventDefault(); //prevent default action

//     // Extracting Form Data
//     var movie_name = document.getElementById('movie_name').value;
//     var movie_description = document.getElementById('movie__description').value;
//     var language = document.getElementById('movie__language').value;
//     var category = document.getElementById('movie__category').value;
//     var subcategory = document.getElementById('movie__subcategory__choosen').value;
//     var thumbnail_image = $('#movie__file')[0].files[0];

//     // javascript data object
//     var data = {
//         'movie_name': movie_name,
//         'movie_description': movie_description,
//         'language': language,
//         'category': category,
//         'subcategory': subcategory,
//     }

//     // adding data to javascript form which is to be send over ajax request
//     var formData = new FormData();
//     formData.append('data', JSON.stringify(data));
//     formData.append('file', thumbnail_image, thumbnail_image.name);
//     $('#movie-submit').attr('disabled', true);
//     $.ajax({
//         type: 'POST',
//         url: '',
//         data: formData,
//         dataType: 'json',
//         enctype: 'multipart/form-data',
//         processData: false,
//         contentType: false,
//         success: function (data) {
//             $('#movie-submit').attr('disabled', false);
//             // checking and handling error conditions
//             if (data.is_series_exists != '') {
//                 alert(data.is_series_exists);
//             } else if (data.is_language_selected != '') {
//                 alert(data.is_language_selected);
//             } else if (data.is_category_selected != '') {
//                 alert(data.is_category_selected);
//             } else if (data.is_subcategory_selected != '') {
//                 alert(data.is_subcategory_selected);
//             } else if (data.is_thumbnail_too_large != '') {
//                 alert(data.is_thumbnail_too_large);
//             } else if (data.is_thumbnail_mimetype_problem != '') {
//                 alert(data.is_thumbnail_mimetype_problem);
//             } else if (data.is_successful != '') {

//                 // setting series_id for the series created
//                 document.getElementById('movie_id').innerHTML = data.movie_id;

//                 alert(data.is_successful);

//                 // restricting pointer events for other tabs
//                 $('#list-movieform-list').css('pointer-events', 'none');
//                 $('#list-movieinfo-list').css('pointer-events', 'all');
//                 $('#list-movieinfo-list').tab('show');
//                 $('#season-right').css('display', 'none');
//                 $('#content-right').css('display', 'none');
//                 $('#episodes-right').css('display', 'none');
//                 $('#series-right').css('display', 'none');
//                 $('#add-season-right').css('display', 'none');
//                 $('#add-episodes-right').css('display', 'none');
//                 $('#add-content-right').css('display', 'none');


//             } else {
//                 alert('Some unexpected error has occured. Try again.');
//             }
//         }
//     });
// });


// submitting new movie form using ajax call
// $("#movievideoForm").submit(function (e) {
//     e.preventDefault(); //prevent default action

//     // Extracting Form Data
//     var movie_id = document.getElementById('movie_id').innerHTML;
//     var movie_name = document.getElementById('movie__videoname').value;
//     var movie_description = document.getElementById('movie__videodescription').value;
//     // var episode_tags = document.getElementById('series__season__episodetags').value;
//     var movie_tags = "";
//     $('#m-selected-tags span').each(function () {
//         movie_tags += $(this).attr("value");
//         movie_tags += ",";
//     });
//     movie_tags = movie_tags.substring(0, movie_tags.length - 1);

//     var movie_quality = document.getElementById('m-video_quality').value;
//     var movie_release_date = document.getElementById('movie__videodate').value;
//     var movie_linkorvideo = document.getElementById('m-linkorvideo').value;

//     var movie_link = '';
//     if (movie_linkorvideo == 'Link') {
//         var movie_link = document.getElementById('movie-link').value;
//     }

//     // Files from episode form
//     var thumbnail_image = $('#movie-file2')[0].files[0];
//     var movie_video = $('#movie-video')[0].files[0];

//     // javascript data object
//     var data = {
//         'movie_id': movie_id,
//         'movie_name': movie_name,
//         'movie_description': movie_description,
//         'movie_tags': movie_tags,
//         'movie_quality': movie_quality,
//         'movie_release_date': movie_release_date,
//         'movie_linkorvideo': movie_linkorvideo,
//         'movie_link': movie_link,
//     }

//     // adding data to javascript form which is to be send over ajax request
//     var formData = new FormData();
//     formData.append('data', JSON.stringify(data));
//     formData.append('file', thumbnail_image, thumbnail_image.name);
//     formData.append('video', movie_video);

//     $('#movie-submit').attr('disabled', true);

//     $.ajax({
//         type: 'POST',
//         url: '',
//         data: formData,
//         dataType: 'json',
//         enctype: 'multipart/form-data',
//         processData: false,
//         contentType: false,
//         success: function (data) {
//             $('#movie-submit').attr('disabled', false);
//             // checking and handling error conditions
//             if (data.is_series_season_exists != '') {
//                 alert(data.is_series_season_exists);
//             } else if (data.is_episode_no_exists != '') {
//                 alert(data.is_episode_no_exists);
//             } else if (data.is_quality_selected != '') {
//                 alert(data.is_quality_selected);
//             } else if (data.is_release_date_future != '') {
//                 alert(data.is_release_date_future);
//             } else if (data.is_thumbnail_too_large != '') {
//                 alert(data.is_thumbnail_too_large);
//             } else if (data.is_thumbnail_mimetype_problem != '') {
//                 alert(data.is_thumbnail_mimetype_problem);
//             } else if (data.is_video_mimetype_problem != '') {
//                 alert(data.is_video_mimetype_problem);
//             } else if (data.is_successful != '') {
//                 $('.movie-oe-time').css('display','none');
//                 // appending the new episode to previously created episodes list
//                 // for (var key in data.season_episode_data) {
//                 //     var specialol = `'${data.season_episode_data[key][4]}'`;
//                 //     var htmlgen = '<div id="movie' + data.season_episode_data[key][6] +
//                 //         '" class="container my-5"><h4 class="my-4">Episode ' + data
//                 //         .season_episode_data[key][6] + '-' + data.season_episode_data[key][
//                 //             1
//                 //         ] +
//                 //         '</h4><div class="row"><div class="col-lg-8 col-md-8"><img id="episode' +
//                 //         data.season_episode_data[key][6] + 'thumbnail" src="' + data
//                 //         .season_episode_data[key][3] +
//                 //         '" alt="uploading" class="img-fluid"></div><div class="col-lg-4 col-md-4"><div class="content mx-5"><p class="text-muted">' +
//                 //         data.season_episode_data[key][2] + '</p><p class="text-muted">';

//                 //     for (var i = 0; i < data.season_episode_data[key][9].length; i++) {
//                 //         htmlgen += data.season_episode_data[key][9][i] + ' | ';
//                 //     }

//                 //     htmlgen += '</p><p class="text-muted">Status - ' + data
//                 //         .season_episode_data[key][8] +
//                 //         '</p><button type="button" class="btn btn-primary" onclick="play_video(' +
//                 //         data.season_episode_data[key][0] + ',' + specialol +
//                 //         ')" class="btn btn-primary btn-sm">Play video</button></div></div></div></div>';

//                 //     $('#uploaded_episodes').append(htmlgen);
//                 // }

//                 // // appending current episode to right navigation bar
//                 // $('#episodes-right').append('<li><a href="#episode' + episodecount +
//                 //     '">episode' + episodecount + '</a></li>');

//                 // // reset the form
//                 // $('#seasonepisodeForm').each(function () {
//                 //     this.reset();
//                 // });

//                 // // add season video form toggle
//                 // $('#seasonVideos').collapse('toggle');
//                 // // setting the episode number value
//                 // $('#series__season__episodeno').attr("value", episodecount + 1);

//                 // alert(data.is_successful);
//             } else {
//                 alert('Some unexpected error has occured. Try again.');
//             }
//         }
//     });
// });