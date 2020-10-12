// toggling on left sidebar
$('.special').each(function(){
    $(this).on('click',function(e){
        $(this).attr("class","special");
    })
})

// initial restrictions
$("#list-series-list").on('click', function (e) {
    $('#list-seriesform-list').css('pointer-events', 'all');
    $('#list-seriesinfo-list').css('pointer-events', 'none');
    $('#list-seasoninfo-list').css('pointer-events', 'none');
    $('#list-seriesform-list').tab('show');

	$('#uploaded_episodes').empty();
	$('#episodes-right').empty();
	$('#season-right').empty();
	$('#apnd').empty();
});
// reset everything on click on series in added-content section
$("#list-added-series-list").on('click', function (e) {
    $('#list-added-seriesform-list').css('pointer-events', 'all');
    $('#list-added-seriesinfo-list').css('pointer-events', 'none');
    $('#list-added-seasoninfo-list').css('pointer-events', 'none');
    $('#list-added-seriesform-list').tab('show');
});


$('#reject-sect').on('show.bs.collapse',function(e){
    console.log('hii');
    $('#verify-sect').collapse('hide');
})

$('#verify-sect').on('show.bs.collapse',function(e){
    $('#reject-sect').collapse('hide');
})


