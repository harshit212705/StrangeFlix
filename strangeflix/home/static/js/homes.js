$('document').on('resize', function (e) {
   var adjust = $('.player-wrapper').css('height');
   var hd = $('.ser-hd').css('height');
   adjust = parseInt(adjust) - parseInt(hd);
   $('.vid-cont').css('height', adjust);
});
var adjust = $('.player-wrapper').css('height');
var hd = $('.ser-hd').css('height');
adjust = parseInt(adjust) - parseInt(hd);
$('.vid-cont').css('height', adjust);

// theatre mode 

$('.theatre__button').on('click', function (e) {
   var chk = $('.theatre__button').attr('class');
   if (chk == 'theatre__button') {
      $('.playlist-container').css('display', 'none');
      $('.c-visible-t-mode').css('display', 'block');
      $('.player-wrapper').attr('class', 'col-xl-12 col-lg-12 col-md-12 player-wrapper');
      $('.theatre__button').attr('class', 'theatre__button hellooo');
      $('.video-body').css('padding', '0% 13%');
   } else {
      $('.playlist-container').css('display', 'block');
      $('.c-visible-t-mode').css('display', 'none');
      $('.player-wrapper').attr('class', 'col-xl-9 col-lg-8 col-md-7 player-wrapper');
      $('.theatre__button').attr('class', 'theatre__button');
      $('.video-body').css('padding', '0% 9%');
   }
});



// function to toggle Login modal
$('#signup').on('click', function () {
   $('#loginModal').modal('toggle')
});
$('#login').on('click', function () {
   $('#signupModal').modal('toggle')
});



// class to manage next and prevs of buttons

class DoublyLinkedList {
   constructor() {
      this.head = null;
      this.tail = null;
      this.length = 0;
   }
   insert(data, position = this.length) {
      let node = new this.Node(data);
      // List is currently empty
      if (this.head === null) {
         this.head = node;
         this.tail = node;
         this.length++;
         return this.head;
      }
      // Insertion at head
      if (position == 0) {
         node.prev = null;
         node.next = this.head;
         this.head.prev = node;
         this.head = node;
         return this.head;
      }
      let iter = 1;
      let currNode = this.head;
      while (currNode.next != null && iter < position) {
         currNode = currNode.next;
         iter++;
      }
      // Make new node point to next node in list
      node.next = currNode.next;
      // Make next node's previous point to new
      if (currNode.next != null) {
         currNode.next.prev = node;
      }
      // Make our node point to previous node
      node.prev = currNode;

      // Make previous node's next point to new node
      currNode.next = node;

      // check if inserted element was at the tail, if yes then make tail point to it
      if (this.tail.next != null) {
         this.tail = this.tail.next;
      }
      this.length++;
      return node;
   }
   remove(data, position = 0) {
      if (this.length === 0) {
         console.log("List is already empty");
         return;
      }
      this.length--;
      let currNode = this.head;
      if (position <= 0) {
         this.head = this.head.next;
         this.head.prev = null;
      } else if (position >= this.length - 1) {
         this.tail = this.tail.prev;
         this.tail.next = null;
      } else {
         let iter = 0;
         while (iter < position) {
            currNode = currNode.next;
            iter++;
         }
         currNode.next = currNode.next.next;
         currNode.next.prev = currNode;
      }
      return currNode;
   }
   display() {
      let currNode = this.head;
      while (currNode != null) {
         console.log(currNode.data + " <-> ");
         currNode = currNode.next;
      }
   }
}

DoublyLinkedList.prototype.Node = class {
   constructor(data) {
      this.data = data;
      this.next = null;
      this.prev = null;
   }
};

var playerVid = new DoublyLinkedList();

// when clicked on prev or next button get the next value in the linked list ad run it on the player
window.addEventListener('load',function(e){
  $('#pl-vid').children('li').each(function(){
     $(this).children('a').each(function(){
        playerVid.insert(this);
     });
  })
  let currNode=playerVid.head;
  while(currNode!=null){
   console.log(currNode.data);
   currNode=currNode.next;
  }
})


// load video when clicked on a video


// search by name and tag

$('#sear-by-nam').on('click', function (e) {
   $('#sear').attr('placeholder', 'search by name');
})

$('#sear-by-tag').on('click', function (e) {
   $('#sear').attr('placeholder', 'search by tag');
})



// movie rating

var movielistItem = [];
var movierating = 0;
$('.movierating-val').each(function (e) {
   movielistItem.push(this);
   $(this).on('click', function (e) {
      for (var ind in movielistItem) {
         $(movielistItem[ind]).css('color', 'white');
      }
      var val = $($(this)).attr('value');
      val = parseInt(val);
      movierating = val;
      for (var ind in movielistItem) {
         $(movielistItem[ind]).css('color', 'red');
         if (ind == val - 1) {
            break;
         }
      }
   })
})



// movie rating

var serieslistItem = [];
var seriesrating = 0;
$('.seriesrating-val').each(function (e) {
   serieslistItem.push(this);
   $(this).on('click', function (e) {
      for (var ind in serieslistItem) {
         $(serieslistItem[ind]).css('color', 'white');
      }
      var val = $($(this)).attr('value');
      val = parseInt(val);
      seriesrating = val;
      for (var ind in serieslistItem) {
         $(serieslistItem[ind]).css('color', 'red');
         if (ind == val - 1) {
            break;
         }
      }
   })
})



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


// progress-bar

function movie_upd(e) {
   const movie_updTime = (e.offsetX / movie_progress.offsetWidth) * movie_video.duration;
   movie_video.currentTime = movie_updTime;
}

// play/pause

function movie_togglePlay() {
   if (movie_video.paused || movie_video.ended) {
      var movie_pl = movie_video.play();
      if (movie_pl != undefined) {
         movie_pl.then(_ => {})
               .catch(error => {
                  movie_video.pause();
               });
      }
   } else {
      movie_video.pause();
   }
}

function movie_updateButton() {
   var movie_icon = document.getElementById("movie-play-icon");
   var movie_title = document.querySelector(".player__button");
   if (this.paused) {
      movie_icon.setAttribute("class", "fas fa-play");
      movie_title.setAttribute("title", "play");
   } else {
      movie_icon.setAttribute("class", "fas fa-pause");
      movie_title.setAttribute("title", "pause");
   }
}

// skip 

function movie_skip() {
   movie_video.currentTime += parseFloat(this.dataset.skip);
}

function movie_handleRangeUpdate() {
   var movie_vol = document.querySelector("#movie-vol-ico");
   var movie_titl = document.querySelector(".volume__button");
   if (this.name == "volume") {
      if (this.value == 0) {
         movie_vol.setAttribute("class", "fas fa-volume-mute");
         movie_titl.setAttribute("title", "unmute");
      } else {
         movie_vol.setAttribute("class", "fas fa-volume-up");
         movie_titl.setAttribute("title", "mute");
         movie_prev = this.value;
      }
   }
   movie_video[this.name] = this.value;
}

// handle progress and timer on time update event

function movie_handleProgress() {
   const movie_percent = (movie_video.currentTime / movie_video.duration) * 100;
   movie_progressBar.style.flexBasis = `${movie_percent}%`;
   var movie_current = document.getElementById("movie-current");
   var movie_timeDuration = document.getElementById("movie-duration");
   // curr mins spend
   var movie_currmins = Math.floor(movie_video.currentTime / 60);

   // curr secs spend
   var movie_currsecs = Math.floor(movie_video.currentTime - movie_currmins * 60);

   // total mins
   var movie_durmins = movie_video.currentTime==0?0:Math.floor(movie_video.duration / 60);

   //total secs
   var movie_dursecs = movie_video.currentTime==0?0:Math.floor(movie_video.duration - movie_durmins * 60);

   if (movie_currsecs < 10) {
      movie_currsecs = "0" + movie_currsecs;
   }
   if (movie_dursecs < 10) {
      movie_dursecs = "0" + movie_dursecs;
   }
   if (movie_currmins < 10) {
      movie_currmins = "0" + movie_currmins;
   }
   if (movie_durmins < 10) {
      movie_durmins = "0" + movie_durmins;
   }
   movie_current.innerHTML = movie_currmins + ":" + movie_currsecs + " / ";
   movie_timeDuration.innerHTML = movie_durmins + ":" + movie_dursecs;
}

var movie_player, movie_video, movie_progress, movie_progressBar, movie_playpause, movie_skipButtons, movie_ranges;
var movie_mousedown, movie_prev, movie_voloff, movie_fulls, movie_pip, movie_total_duration;
var movie_playback, movie_quality, movie_dis, movie_plbk, movie_qual, movie_seli;
// var movie_packet_start_time = 0, movie_maxtime_fetched = 0, movie_nextpacket_url = '', movie_fetcherror = '';
// var movie_previous_time_watched = 0;



function initialize_movie_player() {
   // console.log('initialized');
   // player
   movie_player = document.querySelector('.player');

   // video
   movie_video = movie_player.querySelector('.viewer');

   // progress
   movie_progress = movie_player.querySelector('.progress');

   // progress__filled
   movie_progressBar = movie_player.querySelector('.progress__filled');

   // toggle play/pause
   movie_playpause = movie_player.querySelector('.toggle');

   // skipButtons
   movie_skipButtons = movie_player.querySelectorAll('[data-skip]');

   // ranges for volume and speed
   movie_ranges = movie_player.querySelectorAll('.player__slider');

   movie_mousedown = false;

   // update when click event is fired
   movie_progress.addEventListener('click', movie_upd);
   movie_progress.addEventListener('mousemove', (e) => movie_mousedown && movie_upd(e));
   movie_progress.addEventListener('mousedown', () => movie_mousedown = true);
   movie_progress.addEventListener('mouseup', () => movie_mousedown = false);

   movie_playpause.addEventListener('click', movie_togglePlay);


   // toggle when click event is fired on the video
   movie_video.addEventListener('click', movie_togglePlay);

   // change the icon based on the event fired
   movie_video.addEventListener('play', movie_updateButton);
   movie_video.addEventListener('pause', movie_updateButton);

   movie_skipButtons.forEach(movie_button => movie_button.addEventListener('click', movie_skip));

   // volume and speed
   movie_prev = movie_video.volume;

   movie_ranges.forEach(movie_range => movie_range.addEventListener('change', movie_handleRangeUpdate));
   movie_ranges.forEach(movie_range => movie_range.addEventListener('mousemove', movie_handleRangeUpdate));
   movie_voloff = document.querySelector("#movie-volume");
   movie_voloff.addEventListener('click', function (e) {
      var movie_vol = document.querySelector("#movie-vol-ico");
      var movie_inputRange = document.querySelector("#movie-vol-ran");
      var movie_titl = document.querySelector(".volume__button");
      if (movie_video.volume == 0) {
         movie_vol.setAttribute("class", "fas fa-volume-up");
         movie_titl.setAttribute("title", "mute");
         movie_inputRange.value = movie_prev;
         movie_video.volume = movie_prev;
      } else {
         movie_prev = movie_video.volume;
         movie_video.volume = 0;
         movie_inputRange.value = "0";
         movie_vol.setAttribute("class", "fas fa-volume-mute");
         movie_titl.setAttribute("title", "unmute");
      }
   });

   movie_video.addEventListener('timeupdate', movie_handleProgress);

   // fullscreen 
   movie_fulls = document.getElementById("movie-fs");
   movie_fulls.addEventListener("click", async function (event) {
      try {
         // if already in full screen then exit
         if (document.fullscreen) {
               await document.exitFullscreen();
               document.getElementById("movie-fs-ico").setAttribute("class", "fas fa-expand");
               movie_fulls.setAttribute("title", "fullscreen(f)");
         }
         // if not fullscreen then request for fullscreen mode
         else {
               await movie_player.requestFullscreen();
               document.getElementById("movie-fs-ico").setAttribute("class", "fas fa-compress");
               movie_fulls.setAttribute("title", "exit fullscreen(f)");
         }
      } catch (error) {
         console.log(error);
      }
   });

   // picutre-in-picture 

   movie_pip = document.getElementById("movie-pip");
   movie_pip.addEventListener("click", async function (event) {
      movie_pip.disabled = true;
      try {
         if (movie_video !== document.pictureInPictureElement) {
               await movie_video.requestPictureInPicture();
               movie_pip.disabled = false;
         }
         // If already playing exit mide
         else {
               await document.exitPictureInPicture();
               movie_pip.disabled = false;
         }
      } catch (error) {
         console.log(error);
      } finally {
         movie_pip.disabled = false; // enable toggle at last
      }
   });


   // setting dropdown
   movie_playback = document.querySelector(".playbacki");
   movie_quality = document.querySelector(".quali");
   movie_dis = document.querySelectorAll(".dis");
   movie_plbk = document.querySelectorAll(".playback");
   movie_qual = document.querySelectorAll(".qual");
   movie_seli = document.querySelector(".dropdown-menu");
   movie_playback.addEventListener('click', function (e) {
      e.stopPropagation();
      movie_dis.forEach(element => {
         element.style.display = "none";
      });
      movie_qual.forEach(element => {
         element.style.display = "none";
      });
      movie_plbk.forEach(element => {
         element.style.display = "block";
      });
      movie_plbk.forEach(element => {
         element.addEventListener('click', function () {
            movie_video.playbackRate = element.innerHTML;
               movie_qual.forEach(element => {
                  element.style.display = "none";
               });
               movie_plbk.forEach(element => {
                  element.style.display = "none";
               });
               movie_dis.forEach(element => {
                  element.style.display = "block";
               });
         });
      });
   });
   movie_quality.addEventListener('click', function (e) {
      e.stopPropagation();
      movie_qual.forEach(element => {
         element.style.display = "block";
      });
      movie_plbk.forEach(element => {
         element.style.display = "none";
      });
      movie_dis.forEach(element => {
         element.style.display = "none";
      });
      movie_qual.forEach(element => {
         element.addEventListener('click', function () {
               movie_qual.forEach(element => {
                  element.style.display = "none";
               });
               movie_plbk.forEach(element => {
                  element.style.display = "none";
               });
               movie_dis.forEach(element => {
                  element.style.display = "block";
               });
         });
      });
   })

   // $("#movie-video").bind("drop", function() {
   //    console.log('ended');
   // });

   // theatre mode 

   $('.theatre__button').on('click', function (e) {
      var movie_chk = $('.theatre__button').attr('class');
      if (movie_chk == 'theatre__button') {
         $('.playlist-container').css('display', 'none');
         $('.c-visible-t-mode').css('display', 'block');
         $('.player-wrapper').attr('class', 'col-xl-12 col-lg-12 col-md-12 player-wrapper');
         $('.theatre__button').attr('class', 'theatre__button hellooo');
         $('.video-body').css('padding', '0% 13%');
      } else {
         $('.playlist-container').css('display', 'block');
         $('.c-visible-t-mode').css('display', 'none');
         $('.player-wrapper').attr('class', 'col-xl-9 col-lg-8 col-md-7 player-wrapper');
         $('.theatre__button').attr('class', 'theatre__button');
         $('.video-body').css('padding', '0% 9%');
      }
   });


}
