// special class for left navigation bar items
var v = document.querySelectorAll(".special");
v.forEach(element => {
	element.addEventListener('click', function () {
		element.setAttribute("class", "special");
	});
});



// choosing category and subcategory in NEW SERIES FORM in ADD CONTENT SECTION
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


function set_navigation_bars_display(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12) {

	// IN ADD CONTENT SERIES SECTION
	$('#season-right').css('display', d1);
	$('#episodes-right').css('display', d2);
	$('#content-right').css('display', d3);

	// IN ADDED CONTENT SERIES SECTION
	$('#series-right').css('display', d4);
	$('#add-season-right').css('display', d5);
	$('#add-episodes-right').css('display', d6);
	$('#add-content-right').css('display', d7);

	// IN ADD CONTENT MOVIES SECTION
	$('#movie-video-right').css('display', d8);
	$('#movie-free-content-right').css('display', d9);

	// IN ADDED CONTENT MOVIES SECTION
	$('#add-movie-right').css('display', d10);
	$('#add-movie-video-right').css('display', d11);
	$('#add-movie-free-content-right').css('display', d12);

}


// reset everything on clicking on SERIES in ADD CONTENT SECTION IN LEFT NAVIGATION BAR
$("#list-series-list").on('click', function (e) {

	// restricting pointer events for other tabs
	$('#list-seriesform-list').css('pointer-events', 'all');
	$('#list-seriesinfo-list').css('pointer-events', 'none');
	$('#list-seasoninfo-list').css('pointer-events', 'none');
	$('#list-seriesform-list').tab('show');

	// reset seriesForm
	$('#seriesForm').each(function () {
		this.reset();
	});

	//reset seasonForm
	$('#seasonForm').each(function () {
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

	// Emptying previous series details content
	$('#apnd').empty(); // For already uploaded seasons
	$('#uploaded-free-contents').empty();
	$('#uploaded_episodes').empty();

	// setting default empty value for category and subcategory
	showent.style.display = "none";
	showsports.style.display = "none";
	txtval.value = "";
	showtxt.style.display = "none";

	set_navigation_bars_display('none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none');
});



// once moved to ADD SEASON SECTION IN ADD CONTENT remove pointer events to ADD EPISODES SECTION
$('#list-seriesinfo-list').on('click', function (e) {
	$('#list-seasoninfo-list').css('pointer-events', 'none');

	set_navigation_bars_display('block', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none');

});

// once moved to ADD SEASON SECTION IN ADDED CONTENT remove pointer events to ADD EPISODES SECTION
$('#list-added-seriesinfo-list').on('click', function (e) {
	$('#list-added-seasoninfo-list').css('pointer-events', 'none');

	set_navigation_bars_display('none', 'none', 'none', 'none', 'block', 'none', 'none', 'none', 'none', 'none', 'none', 'none');

});

// once moved to UPLOADED SERIES SECTION IN ADDED CONTENT remove pointer events to ADD SEASON and ADD EPISODES SECTION
$('#list-added-seriesform-list').on('click', function (e) {
	$('#list-added-seriesinfo-list').css('pointer-events', 'none');
	$('#list-added-seasoninfo-list').css('pointer-events', 'none');

	set_navigation_bars_display('none', 'none', 'none', 'block', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none');

});


// initial ADD SEASON FORM setup in SERIES IN ADDED SECTION
$('#list-added-seriesinfo-list').on('show.bs.tab', function (e) {
	var addCountEle = $('#add-season-right li').length;
	$('#add-seasonvalue').attr("value", addCountEle + 1);
});


// initial ADD EPISODE FORM setup in SERIES IN ADDED SECTION
$('#list-added-seasoninfo-list').on('show.bs.tab', function (e) {
	var addCountEle = $('#add-episodes-right li').length;
	$('#add__series__season__episodeno').attr("value", addCountEle + 1);
});


// handling ADD TAG in ADD EPISODES SECTION of SERIES IN ADD CONTENT SECTION
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



// handling ADD TAG in ADD FREE CONTENT SECTION of SERIES IN ADD CONTENT SECTION
var caddTag = document.querySelector("#c-add-tag");
var ctagText = document.querySelector("#c-tag-text");
var cshowTags = document.querySelector("#c-selected-tags");
var cselectedTags = document.querySelectorAll("#c-tag-toggler");
caddTag.addEventListener('click', function (e) {
	var span = document.createElement('span');
	var textValue = ctagText.value;
	span.setAttribute("value", textValue);
	span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
	span.style.border = "2px solid blue";
	span.style.borderRadius = "50%";
	span.innerHTML = textValue + '<a id="c-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
	cshowTags.append(span);
	cselectedTags = document.querySelectorAll("#c-tag-toggler");
	cselectedTags.forEach(element => {
		element.addEventListener('click', function (e) {
			var obj = element.parentNode;
			obj.remove();
		});
	});
});



// handling ADD TAG in ADD EPISODE SECTION of SERIES IN ADDED CONTENT SECTION
function add_tag_in_added(){
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
}

add_tag_in_added();


// handling ADD TAG in ADD FREE CONTENT SECTION of SERIES IN ADDED CONTENT SECTION
function add_tag_c_added(){
	var eaddAddTag = document.querySelector("#e-add-add-tag");
	var eaddTagText = document.querySelector("#e-add-tag-text");
	var eaddShowTags = document.querySelector("#e-add-selected-tags");
	var eaddSelectedTags = document.querySelectorAll("#e-add-tag-toggler");
	eaddAddTag.addEventListener('click', function (e) {
		var span = document.createElement('span');
		var textValue = eaddTagText.value;
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
}

add_tag_c_added();


// handling ADD TAG in ADD EPISODE SECTION of SERIES IN ADDED CONTENT SECTION FOR REJECTED VIDEOS
function edit_add_tag_in_added(){
	var addAddTag = document.querySelector("#edit-content-modal #add-add-tag");
	var addTagText = document.querySelector("#edit-content-modal #add-tag-text");
	var addShowTags = document.querySelector("#edit-content-modal #add-selected-tags");
	var addSelectedTags = document.querySelectorAll("#edit-modal-add-tag-toggler");
	addAddTag.addEventListener('click', function (e) {
		var span = document.createElement('span');
		var textValue = addTagText.value;
		span.setAttribute("value", textValue);
		span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
		span.style.border = "2px solid blue";
		span.style.borderRadius = "50%";
		span.innerHTML = textValue + '<a id="edit-modal-add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
		addShowTags.append(span);
		addSelectedTags = document.querySelectorAll("#edit-modal-add-tag-toggler");
		addSelectedTags.forEach(element => {
			element.addEventListener('click', function (e) {
				var obj = element.parentNode;
				obj.remove();
			});
		});
	});
}


// handling ADD TAG in ADD FREE CONTENT SECTION of SERIES IN ADDED CONTENT SECTION FOR REJECTED VIDEOS
function edit_add_tag_c_added(){
	var eaddAddTag = document.querySelector("#edit-content-modal #e-add-add-tag");
	var eaddTagText = document.querySelector("#edit-content-modal #e-add-tag-text");
	var eaddShowTags = document.querySelector("#edit-content-modal #e-add-selected-tags");
	var eaddSelectedTags = document.querySelectorAll("#edit-modal-e-add-tag-toggler");
	eaddAddTag.addEventListener('click', function (e) {
		var span = document.createElement('span');
		var textValue = eaddTagText.value;
		span.setAttribute("value", textValue);
		span.setAttribute("class", "text-center px-2 py-2 bg-primary text-white");
		span.style.border = "2px solid blue";
		span.style.borderRadius = "50%";
		span.innerHTML = textValue + '<a id="edit-modal-e-add-tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
		eaddShowTags.append(span);
		eaddSelectedTags = document.querySelectorAll("#edit-modal-e-add-tag-toggler");
		eaddSelectedTags.forEach(element => {
			element.addEventListener('click', function (e) {
				var obj = element.parentNode;
				obj.remove();
			});
		});
	});
}


// handling selection between video or link in ADD EPISODE SECTION of SERIES IN ADD CONTENT SECTION
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



// handling selection between video or link in ADD FREE CONTENT SECTION of SERIES IN ADD CONTENT SECTION
var free_cont_linkorvideo = document.querySelector('#contentlinkorvideo');
var free_cont_episodeVideo = document.querySelector('#content-video');
var free_cont_episodeLink = document.querySelector('#content-link');
free_cont_linkorvideo.addEventListener('change', function (e) {
	var cont = free_cont_linkorvideo.options[free_cont_linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		free_cont_episodeVideo.style.display = "block";
		free_cont_episodeLink.value = "";
		free_cont_episodeLink.style.display = "none";
	} else {
		free_cont_episodeVideo.style.display = "none";
		free_cont_episodeLink.style.display = "block";
		free_cont_episodeVideo.value = "";
	}
});



// handling selection between video or link in ADD EPISODE SECTION of SERIES IN ADDED CONTENT SECTION
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


// handling selection between video or link in ADD FREE CONTENT SECTION of SERIES IN ADDED CONTENT SECTION
var free_cont_add__linkorvideo = document.querySelector('#add__contentlinkorvideo');
var free_cont_add__episodeVideo = document.querySelector('#add__content-video');
var free_cont_add__episodeLink = document.querySelector('#add__content-link');
free_cont_add__linkorvideo.addEventListener('change', function (e) {
	var cont = free_cont_add__linkorvideo.options[free_cont_add__linkorvideo.selectedIndex].value;
	if (cont != "Link") {
		free_cont_add__episodeVideo.style.display = "block";
		free_cont_add__episodeLink.value = "";
		free_cont_add__episodeLink.style.display = "none";
	} else {
		free_cont_add__episodeVideo.style.display = "none";
		free_cont_add__episodeLink.style.display = "block";
		free_cont_add__episodeVideo.value = "";
	}
});



// // once moved back to added movies tab in added content section then restricting its direct movement to next tab
// $('#list-added-movieform-list').on('click', function (e) {
// 	$('#list-added-movieinfo-list').css('pointer-events', 'none');
// 	$('#add-movie-right').css('display', 'block');
// 	$('#season-right').css('display', 'none');
// 	$('#content-right').css('display', 'none');
// 	$('#episodes-right').css('display', 'none');
// 	$('#series-right').css('display', 'none');
// 	$('#add-season-right').css('display', 'none');
// 	$('#add-episodes-right').css('display', 'none');
// 	$('#add-content-right').css('display', 'none');
// });


// call it when created a new episodeform

function callit() {
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
		span.innerHTML = textValue +
			'<a id="tag-toggler" type="button"><i class="fas fa-times mx-1"></i></a>';
		showTags.append(span);
		selectedTags = document.querySelectorAll("#tag-toggler");
		selectedTags.forEach(element => {
			element.addEventListener('click', function (e) {
				var obj = element.parentNode;
				obj.remove();
			});
		});
	});
}