var v = document.querySelectorAll(".special");
v.forEach(element => {
	element.addEventListener('click', function () {
		element.setAttribute("class", "special");
	});
});



// custom-select
// series-category
var selected = document.querySelector('#series-category');
var entsel = document.querySelectorAll("#chkbx");
var sprtslct = document.querySelector("#sports-subcategory");
var showent = document.querySelector(".ws-entmnt");
var showsports = document.querySelector(".ws-sports");
var showtxt = document.querySelector(".ws-txt");
var txtval = document.querySelector("#subcategory__choosen");
var chkb = document.querySelector("#savech");
selected.addEventListener('change', function (e) {
	var content = selected.options[selected.selectedIndex].value;
	if (content == "Sports") {
		showent.style.display = "none";
		showsports.style.display = "block";
		txtval.value = "";
		showtxt.style.display = "block";
		sprtslct.addEventListener('change', function (e) {
			var sportsub = sprtslct.options[sprtslct.selectedIndex].value;
			if (sportsub != "Subcategory")
				txtval.value = sportsub;
			else
				txtval.value = "";
		});
	} else if (content == "Entertainment") {
		showsports.style.display = "none";
		txtval.value = "";
		showtxt.style.display = "block";
		showent.style.display = "block";
		chkb.addEventListener('click', function (e) {
			txtval.value = "";
			entsel.forEach(element => {
				if (element.checked) {
					txtval.value += element.value + ",";
				}
			});
			if (txtval.value.length > 0) {
				txtval.value = txtval.value.substring(0, txtval.value.length - 1);
			}
		});

	} else {
		showent.style.display = "none";
		showsports.style.display = "none";
		txtval.value = "";
		showtxt.style.display = "none";
	}
});



// submitting series form using ajax call
// $("#seriesForm").submit(function (e) {
// 	e.preventDefault(); //prevent default action 
// 	var post_url = $(this).attr("action"); //get form action url
// 	var form_data = $(this).serialize(); //Encode form elements for submission
// 	$('#list-seriesform-list').css('pointer-events', 'none');
// 	$('#list-seriesinfo-list').css('pointer-events', 'all');
// 	$('#list-seriesinfo-list').tab('show');
// 	// $.post( post_url, form_data, function( response ) {
// 	// //   $("#server-results").html( response ); // data from server
// 	// });
// });

// submitting season form using ajax call
// $('#seasonForm').submit(function (e) {
// 	e.preventDefault();
// 	var post_url = $(this).attr("action");
// 	var form_data = $(this).serialize();  
//  $('#list-seasoninfo-list').css('pointer-events', 'all');
//  $('#list-seasoninfo-list').tab('show');
// 	console.log(form_data);
// 	// $.post( post_url, form_data, function( response ) {
// 	// //   $("#server-results").html( response ); // data from server(recieved dat should have parent id="season+{{seasonno}}" and have a button which will take it to next page)
// 	// });

// 	// if successfully posted then
// 	var seasoncount = $('#season-right li').length;
// 	seasoncount++;
// 	var htmlgen='<div id="season'+seasoncount+'"><h4>Season'+seasoncount+'</h4></div>';
// 	$('#season-right').append('<li><a href="#season' + seasoncount + '">season' + seasoncount + '</a></li>');
// 	$('#apnd').append(htmlgen);
// 	// reset the form
// 	$('#seasonForm').each(function(){
// 		this.reset();
// 	});
// 	$('#collapseExample').collapse('toggle');
// 	$('#seasonvalue').attr("value",seasoncount+1);
// });


// reset everything on click on series in add-content section

$("#list-series-list").on('click', function (e) {
	$('#list-seriesform-list').css('pointer-events', 'all');
	$('#list-seriesinfo-list').css('pointer-events', 'none');
	$('#list-seasoninfo-list').css('pointer-events', 'none');
	$('#list-seriesform-list').tab('show');

	//reset seasonForm
	$('#seasonForm').each(function () {
		this.reset();
	});
	// reset seriesForm
	$('#seriesForm').each(function () {
		this.reset();
	});
	//reset episodeForm
	$('#seasonepisodeForm').each(function () {
		this.reset();
	});
	// reset free content form
	$('#freecontentForm').each(function () {
		this.reset();
	});

	$('#uploaded_episodes').empty();
	$('#episodes-right').empty();
	$('#season-right').empty();
	$('#apnd').empty();
	showent.style.display = "none";
	showsports.style.display = "none";
	txtval.value = "";
	showtxt.style.display = "none";

	$('#season-right').css('display', 'none');
	$('#content-right').css('display', 'none');
	$('#episode-right').css('display', 'none');
	$('#series-right').css('display', 'none');
	$('#add-season-right').css('display', 'none');
	$('#add-episode-right').css('display', 'none');
	$('#add-content-right').css('display', 'none');
});

// reset everything on click on series in added-content section
$("#list-added-series-list").on('click', function (e) {
	$('#list-added-seriesform-list').css('pointer-events', 'all');
	$('#list-added-seriesinfo-list').css('pointer-events', 'none');
	$('#list-added-seasoninfo-list').css('pointer-events', 'none');
	$('#list-added-seriesform-list').tab('show');

	// change the ids of the forms or div tag in added section
	//reset seasonForm
	$('#add-seasonForm').each(function () {
		this.reset();
	});
	// reset seriesForm
	$('#add-seriesForm').each(function () {
		this.reset();
	});
	//reset episodeForm
	$('#add-episodeForm').each(function () {
		this.reset();
	});

	$('#uploaded_episodes').empty();
	$('#episodes-right').empty();
	$('#season-right').empty();
	$('#apnd').empty();
	$('#season-right').css('display', 'none');
	$('#episode-right').css('display', 'none');
	$('#content-right').css('display', 'none');
	$('#series-right').css('display', 'block');
	$('#add-season-right').css('display', 'none');
	$('#add-episode-right').css('display', 'none');
	$('#add-content-right').css('display', 'none');
});


// once moved to add season remove pointer-events for add section
$('#list-seriesinfo-list').on('click', function (e) {
	$('#list-seasoninfo-list').css('pointer-events', 'none');
	$('#season-right').css('display', 'block');
	$('#content-right').css('display', 'none');
	$('#episode-right').css('display', 'none');
	$('#series-right').css('display', 'none');
	$('#add-season-right').css('display', 'none');
	$('#add-episode-right').css('display', 'none');
	$('#add-content-right').css('display', 'none');
})

// once moved to add season remove pointer-events for add section
$('#list-added-seriesinfo-list').on('click', function (e) {
	$('#list-added-seasoninfo-list').css('pointer-events', 'none');
	$('#season-right').css('display', 'none');
	$('#content-right').css('display', 'none');
	$('#episode-right').css('display', 'none');
	$('#series-right').css('display', 'none');
	$('#add-season-right').css('display', 'block');
	$('#add-episode-right').css('display', 'none');
	$('#add-content-right').css('display', 'none');
})

// once moved to add season remove pointer-events for add section
$('#list-added-seriesform-list').on('click', function (e) {
	$('#list-added-seriesinfo-list').css('pointer-events', 'none');
	$('#list-added-seasoninfo-list').css('pointer-events', 'none');
	$('#season-right').css('display', 'none');
	$('#content-right').css('display', 'none');
	$('#episode-right').css('display', 'none');
	$('#series-right').css('display', 'block');
	$('#add-season-right').css('display', 'none');
	$('#add-episode-right').css('display', 'none');
	$('#add-content-right').css('display', 'none');
})

// initial season form-setups for added section
$('#list-added-seriesinfo-list').on('show.bs.tab', function (e) {
	var addCountEle = $('#add-season-right li').length;
	$('#add-seasonvalue').attr("value", addCountEle + 1);
});

// initial episode form-setups for added section
$('#list-added-seasoninfo-list').on('show.bs.tab', function (e) {
	var addCountEle = $('#add-episode-right li').length;
	$('#add__series__season__episodeno').attr("value", addCountEle + 1);
});



// handling tags for episode add section

var addTag = document.querySelector("#add-tag");
var tagText = document.querySelector("#tag-text");
var showTags = document.querySelector("#selected-tags");
var selectedTags = document.querySelectorAll("#tag-toggler");
addTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = tagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	showTags.append(span);
	selectedTags = document.querySelectorAll("#tag-toggler");
	selectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});


// handling tags for content add section

var caddTag = document.querySelector("#c-add-tag");
var ctagText = document.querySelector("#c-tag-text");
var cshowTags = document.querySelector("#c-selected-tags");
var cselectedTags = document.querySelectorAll("#c-tag-toggler");
caddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = tagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	cshowTags.append(span);
	cselectedTags = document.querySelectorAll("#c-tag-toggler");
	cselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});

// handling tags for content added section

var addAddTag = document.querySelector("#add-add-tag");
var addTagText = document.querySelector("#add-tag-text");
var addShowTags = document.querySelector("#add-selected-tags");
var addSelectedTags = document.querySelectorAll("#add-tag-toggler");
addAddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = addTagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	addShowTags.append(span);
	addSelectedTags = document.querySelectorAll("#add-tag-toggler");
	addSelectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});

// handling tags for episode added section

var eaddAddTag = document.querySelector("#e-add-add-tag");
var eaddTagText = document.querySelector("#e-add-tag-text");
var eaddShowTags = document.querySelector("#e-add-selected-tags");
var eaddSelectedTags = document.querySelectorAll("#e-add-tag-toggler");
eaddAddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = addTagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="e-add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	eaddShowTags.append(span);
	eaddSelectedTags = document.querySelectorAll("#e-add-tag-toggler");
	eaddSelectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});


var linkorvideo = document.querySelector('#linkorvideo');
var episodeVideo = document.querySelector('#episode-video');
var episodeLink = document.querySelector('#episode-link');
linkorvideo.addEventListener('change', function (e) {
	var cont = linkorvideo.options[linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		episodeVideo.style.display = "block";
		episodeLink.value = "";
		episodeLink.style.display = "none";
	} else {
		episodeVideo.style.display = "none";
		episodeLink.style.display = "block";
		episodeVideo.value = "";
	}
});

var add__linkorvideo = document.querySelector('#add__linkorvideo');
var add__episodeVideo = document.querySelector('#add__episode-video');
var add__episodeLink = document.querySelector('#add__episode-link');
add__linkorvideo.addEventListener('change', function (e) {
	var cont = add__linkorvideo.options[add__linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		add__episodeVideo.style.display = "block";
		add__episodeLink.value = "";
		add__episodeLink.style.display = "none";
	} else {
		add__episodeVideo.style.display = "none";
		add__episodeLink.style.display = "block";
		add__episodeVideo.value = "";
	}
});