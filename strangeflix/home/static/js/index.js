// carousel arrow display in each section 
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

// function to set contents 
function set_content_display(d1, d2, d3, d4, d5, d6, d7, d8) {

	$('#video_with_comments').css('display', d1);

	// IN SELECTED SERIES SECTION
	$('#selected_season_description').css('display', d2);
	$('#selected_season_freecontent').css('display', d3);
	$('#selected_season_episodes').css('display', d4);
    $('#selected_series_description').css('display', d5);
    $('#selected_series_season').css('display', d6);

	// IN SELECTED MOVIE SECTION
	$('#selected_movie_description').css('display', d7);
    $('#selected_movie_freecontent').css('display', d8);

}


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


function bind_control_arrow_movie_freecontent() {
    $('#movie_freecontent-controls').on('slid.bs.carousel', '', function () {
        var $this = $(this);
        $this.children('#movie_freecontent-controls .carousel-control-prev').show();
        $this.children('#movie_freecontent-controls .carousel-control-next').show();
        if ($('#movie_freecontent-controls .carousel-inner .carousel-item:first').hasClass('active')) {
            $this.children('#movie_freecontent-controls .carousel-control-prev').hide();
        } else if ($('#movie_freecontent-controls .carousel-inner .carousel-item:last').hasClass('active')) {
            $this.children('#movie_freecontent-controls .carousel-control-next').hide();
        }
    });
}

function bind_control_arrow_series_season() {
    $('#series_season-controls').on('slid.bs.carousel', '', function () {
        var $this = $(this);
        $this.children('#series_season-controls .carousel-control-prev').show();
        $this.children('#series_season-controls .carousel-control-next').show();
        if ($('#series_season-controls .carousel-inner .carousel-item:first').hasClass('active')) {
            $this.children('#series_season-controls .carousel-control-prev').hide();
        } else if ($('#series_season-controls .carousel-inner .carousel-item:last').hasClass('active')) {
            $this.children('#series_season-controls .carousel-control-next').hide();
        }
    });
}

function bind_control_arrow_series_season_freecontent() {
    $('#series_season_freecontent-controls').on('slid.bs.carousel', '', function () {
        var $this = $(this);
        $this.children('#series_season_freecontent-controls .carousel-control-prev').show();
        $this.children('#series_season_freecontent-controls .carousel-control-next').show();
        if ($('#series_season_freecontent-controls .carousel-inner .carousel-item:first').hasClass('active')) {
            $this.children('#series_season_freecontent-controls .carousel-control-prev').hide();
        } else if ($('#series_season_freecontent-controls .carousel-inner .carousel-item:last').hasClass('active')) {
            $this.children('#series_season_freecontent-controls .carousel-control-next').hide();
        }
    });
}

function bind_control_arrow_series_season_episodes() {
    $('#series_season_episodes-controls').on('slid.bs.carousel', '', function () {
        var $this = $(this);
        $this.children('#series_season_episodes-controls .carousel-control-prev').show();
        $this.children('#series_season_episodes-controls .carousel-control-next').show();
        if ($('#series_season_episodes-controls .carousel-inner .carousel-item:first').hasClass('active')) {
            $this.children('#series_season_episodes-controls .carousel-control-prev').hide();
        } else if ($('#series_season_episodes-controls .carousel-inner .carousel-item:last').hasClass('active')) {
            $this.children('#series_season_episodes-controls .carousel-control-next').hide();
        }
    });
}

function bind_control_arrow_search_results_subcategory() {
    $('#search_results_subcategory-controls').on('slid.bs.carousel', '', function () {
        var $this = $(this);
        $this.children('#search_results_subcategory-controls .carousel-control-prev').show();
        $this.children('#search_results_subcategory-controls .carousel-control-next').show();
        if ($('#search_results_subcategory-controls .carousel-inner .carousel-item:first').hasClass('active')) {
            $this.children('#search_results_subcategory-controls .carousel-control-prev').hide();
        } else if ($('#search_results_subcategory-controls .carousel-inner .carousel-item:last').hasClass('active')) {
            $this.children('#search_results_subcategory-controls .carousel-control-next').hide();
        }
    });
}