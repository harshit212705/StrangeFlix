$(window).on('load', function() {

    // setting carousel arrows display
    if ($('#search_results .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#search_results').children('#search_results .carousel-control-prev').hide();
    }
    if ($('#search_results .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#search_results').children('#search_results .carousel-control-next').hide();
    }

    if ($('#recommended_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#recommended_series').children('#recommended_series .carousel-control-prev').hide();
    }
    if ($('#recommended_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#recommended_series').children('#recommended_series .carousel-control-next').hide();
    }

    if ($('#recommended_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#recommended_movies').children('#recommended_movies .carousel-control-prev').hide();
    }
    if ($('#recommended_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#recommended_movies').children('#recommended_movies .carousel-control-next').hide();
    }

    if ($('#recent_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#recent_series').children('#recent_series .carousel-control-prev').hide();
    }
    if ($('#recent_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#recent_series').children('#recent_series .carousel-control-next').hide();
    }

    if ($('#recent_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#recent_movies').children('#recent_movies .carousel-control-prev').hide();
    }
    if ($('#recent_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#recent_movies').children('#recent_movies .carousel-control-next').hide();
    }

    if ($('#popular_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#popular_series').children('#popular_series .carousel-control-prev').hide();
    }
    if ($('#popular_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#popular_series').children('#popular_series .carousel-control-next').hide();
    }

    if ($('#popular_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $('#popular_movies').children('#popular_movies .carousel-control-prev').hide();
    }
    if ($('#popular_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $('#popular_movies').children('#popular_movies .carousel-control-next').hide();
    }

});

// carousel
$('#search_results').on('slid.bs.carousel', '', function () {
    //ajax here to load the series and movies
    var $this = $(this);
    $this.children('#search_results .carousel-control-prev').show();
    $this.children('#search_results .carousel-control-next').show();
    if ($('#search_results .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#search_results .carousel-control-prev').hide();
    } else if ($('#search_results .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#search_results .carousel-control-next').hide();
    }
});

$('#recommended_series').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#recommended_series .carousel-control-prev').show();
    $this.children('#recommended_series .carousel-control-next').show();
    if ($('#recommended_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#recommended_series .carousel-control-prev').hide();
    } else if ($('#recommended_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#recommended_series .carousel-control-next').hide();
    }
});

$('#recommended_movies').on('slid.bs.carousel', '', function () {
    //ajax here to load the series and movies
    var $this = $(this);
    $this.children('#recommended_movies .carousel-control-prev').show();
    $this.children('#recommended_movies .carousel-control-next').show();
    if ($('#recommended_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#recommended_movies .carousel-control-prev').hide();
    } else if ($('#recommended_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#recommended_movies .carousel-control-next').hide();
    }
});

$('#recent_series').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#recent_series .carousel-control-prev').show();
    $this.children('#recent_series .carousel-control-next').show();
    if ($('#recent_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#recent_series .carousel-control-prev').hide();
    } else if ($('#recent_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#recent_series .carousel-control-next').hide();
    }
});

$('#recent_movies').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#recent_movies .carousel-control-prev').show();
    $this.children('#recent_movies .carousel-control-next').show();
    if ($('#recent_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#recent_movies .carousel-control-prev').hide();
    } else if ($('#recent_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#recent_movies .carousel-control-next').hide();
    }
});

$('#popular_series').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#popular_series .carousel-control-prev').show();
    $this.children('#popular_series .carousel-control-next').show();
    if ($('#popular_series .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#popular_series .carousel-control-prev').hide();
    } else if ($('#popular_series .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#popular_series .carousel-control-next').hide();
    }
});

$('#popular_movies').on('slid.bs.carousel', '', function () {
    var $this = $(this);
    $this.children('#popular_movies .carousel-control-prev').show();
    $this.children('#popular_movies .carousel-control-next').show();
    if ($('#popular_movies .carousel-inner .carousel-item:first').hasClass('active')) {
        $this.children('#popular_movies .carousel-control-prev').hide();
    } else if ($('#popular_movies .carousel-inner .carousel-item:last').hasClass('active')) {
        $this.children('#popular_movies .carousel-control-next').hide();
    }
});