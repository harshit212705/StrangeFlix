// toggling on left sidebar
$('.special').each(function(){
    $(this).on('click',function(e){
        $(this).attr("class","special");
    })
})

// setting right navigation bars display options
function set_navigation_bars(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14) {

    // IN PENDING CONTENT SERIES SECTION
    $('#series-right').css('display', d1);
    $('#season-right').css('display', d2);
    $('#content-right').css('display', d3);
	$('#episodes-right').css('display', d4);

	// IN VERIFIED CONTENT SERIES SECTION
	$('#verified-series-right').css('display', d5);
    $('#verified-season-right').css('display', d6);
    $('#verified-content-right').css('display', d7);
	$('#verified-episodes-right').css('display', d8);

	// IN PENDING CONTENT MOVIES SECTION
	$('#movies-right').css('display', d9);
    $('#movies-content-right').css('display', d10);
    $('#movies-video-right').css('display', d11);

	// IN VERIFIED CONTENT MOVIES SECTION
	$('#verified-movies-right').css('display', d12);
    $('#verified-movies-content-right').css('display', d13);
    $('#verified-movies-video-right').css('display', d14);

}

// get user once clicked on list-users-left
$('#list-users-list').on('click',function(e){
    $('#list-usertable-list').tab('show');
    $('#list-changeuser-list').css('pointer-events', 'none');
    $('#insert-users').empty();
    set_navigation_bars('none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none',
                'none', 'none', 'none');
 })

$('#list-series-list').on('click', function (e) {
    $('#list-seriesform-list').css('pointer-events', 'all');
    $('#list-seriesinfo-list').css('pointer-events', 'none');
    $('#list-seasoninfo-list').css('pointer-events', 'none');
    $('#list-seriesform-list').tab('show');

    get_series();

});

$('#list-movie-list').on('click', function (e) {
    $('#list-movieform-list').css('pointer-events', 'all');
    $('#list-movieinfo-list').css('pointer-events', 'none');
    $('#list-movieform-list').tab('show');

    get_movies();

});

$('#list-added-series-list').on('click', function (e) {
    $('#list-added-seriesform-list').css('pointer-events', 'all');
    $('#list-added-seriesinfo-list').css('pointer-events', 'none');
    $('#list-added-seasoninfo-list').css('pointer-events', 'none');
    $('#list-added-seriesform-list').tab('show');

    get_added_series();

});

$('#list-added-movie-list').on('click', function (e) {
    $('#list-added-movieform-list').css('pointer-events', 'all');
    $('#list-added-movieinfo-list').css('pointer-events', 'none');
    $('#list-added-movieform-list').tab('show');

    get_added_movies();

});


// comment full show
$('.show-mr-button').on('click',function(e){
// console.log($('.show-mr-button').text().trim());
if($('.show-mr-button').text().trim()=='show'){
    $('.d-cent').css('display','block');
    $('.show-mr-button').text('hide');
}
else
{
    $('.d-cent').css('display','-webkit-box');
    $('.show-mr-button').text('show');
}
})