// function to toggle Login modal
document.getElementById("signup").addEventListener('click',function(event){
          $("#loginModal").modal("toggle");
});
//function to toggle register modal
document.getElementById("login").addEventListener('click',function(event){
    $("#signupModal").modal("toggle");
});



// carousel
$('#movie-controls').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#movie-controls .carousel-control-prev').show();
    $this.children('#movie-controls .carousel-control-next').show();
    if ($('#movie-controls .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#movie-controls .carousel-control-prev').hide();
    } else if ($('#movie-controls .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#movie-controls .carousel-control-next').hide();
    }
});
$('#series-controls').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#series-controls .carousel-control-prev').show();
    $this.children('#series-controls .carousel-control-next').show();
    if ($('#series-controls .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#series-controls .carousel-control-prev').hide();
    } else if ($('#series-controls .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#series-controls .carousel-control-next').hide();
    }
});
$('#free-video-controls').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('.carousel-control-prev').show();
    $this.children('.carousel-control-next').show();
    if ($('.carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('.carousel-control-prev').hide();
    } else if ($('.carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('.carousel-control-next').hide();
    }
});

