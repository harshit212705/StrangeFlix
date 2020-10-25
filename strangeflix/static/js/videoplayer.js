// player
const player = document.querySelector('.player');

// video
const video = player.querySelector('.viewer');

// progress
const progress = player.querySelector('.progress');

// progress__filled
const progressBar = player.querySelector('.progress__filled');

// toggle play/pause
const playpause = player.querySelector('.toggle');

// skipButtons
const skipButtons = player.querySelectorAll('[data-skip]');

// ranges for volume and speed
const ranges = player.querySelectorAll('.player__slider');


// progress-bar

function upd(e) {
    const updTime = (e.offsetX / progress.offsetWidth) * video.duration;
    video.currentTime = updTime;
}
let mousedown = false;

// update when click event is fired
progress.addEventListener('click', upd);
progress.addEventListener('mousemove', (e) => mousedown && upd(e));
progress.addEventListener('mousedown', () => mousedown = true);
progress.addEventListener('mouseup', () => mousedown = false);


// play/pause

function togglePlay() {
    if (video.paused || video.ended) {
        var pl = video.play();
        if (pl != undefined) {
            pl.then(_ => {})
                .catch(error => {
                    video.pause();
                });
        }
    } else {
        video.pause();
    }
}
playpause.addEventListener('click', togglePlay);

function updateButton() {
    var icon = document.getElementById("play-icon");
    var title = document.querySelector(".player__button");
    if (this.paused) {
        icon.setAttribute("class", "fas fa-play");
        title.setAttribute("title", "play");
    } else {
        icon.setAttribute("class", "fas fa-pause");
        title.setAttribute("title", "pause");
    }
}

// toggle when click event is fired on the video
video.addEventListener('click', togglePlay);

// change the icon based on the event fired
video.addEventListener('play', updateButton);
video.addEventListener('pause', updateButton);

// skip 

function skip() {
    video.currentTime += parseFloat(this.dataset.skip);
}

skipButtons.forEach(button => button.addEventListener('click', skip));


// volume and speed
var prev = video.volume;

function handleRangeUpdate() {
    var vol = document.querySelector("#vol-ico");
    var titl = document.querySelector(".volume__button");
    if (this.name == "volume") {
        if (this.value == 0) {
            vol.setAttribute("class", "fas fa-volume-mute");
            titl.setAttribute("title", "unmute");
        } else {
            vol.setAttribute("class", "fas fa-volume-up");
            titl.setAttribute("title", "mute");
            prev = this.value;
        }
    }
    video[this.name] = this.value;
}

ranges.forEach(range => range.addEventListener('change', handleRangeUpdate));
ranges.forEach(range => range.addEventListener('mousemove', handleRangeUpdate));
var voloff = document.querySelector("#volume");
voloff.addEventListener('click', function (e) {
    var vol = document.querySelector("#vol-ico");
    var inputRange = document.querySelector("#vol-ran");
    var titl = document.querySelector(".volume__button");
    if (video.volume == 0) {
        vol.setAttribute("class", "fas fa-volume-up");
        titl.setAttribute("title", "mute");
        inputRange.value = prev;
        video.volume = prev;
    } else {
        prev = video.volume;
        video.volume = 0;
        inputRange.value = "0";
        vol.setAttribute("class", "fas fa-volume-mute");
        titl.setAttribute("title", "unmute");
    }
});

// handle progress and timer on time update event

function handleProgress() {
    const percent = (video.currentTime / video.duration) * 100;
    progressBar.style.flexBasis = `${percent}%`;
    var current = document.getElementById("current");
    var timeDuration = document.getElementById("duration");
    // curr mins spend
    var currmins = Math.floor(video.currentTime / 60);

    // curr secs spend
    var currsecs = Math.floor(video.currentTime - currmins * 60);

    // total mins 
    var durmins = video.currentTime==0?0:Math.floor(video.duration / 60);

    //total secs
    var dursecs = video.currentTime==0?0:Math.floor(video.duration - durmins * 60);

    if (currsecs < 10) {
        currsecs = "0" + currsecs;
    }
    if (dursecs < 10) {
        dursecs = "0" + dursecs;
    }
    if (currmins < 10) {
        currmins = "0" + currmins;
    }
    if (durmins < 10) {
        durmins = "0" + durmins;
    }
    current.innerHTML = currmins + ":" + currsecs + " / ";
    timeDuration.innerHTML = durmins + ":" + dursecs;
}
video.addEventListener('timeupdate', handleProgress);

// fullscreen 
var fulls = document.getElementById("fs");
fulls.addEventListener("click", async function (event) {
    try {
        // if already in full screen then exit
        if (document.fullscreen) {
            await document.exitFullscreen();
            document.getElementById("fs-ico").setAttribute("class", "fas fa-expand");
            fulls.setAttribute("title", "fullscreen(f)");
        }
        // if not fullscreen then request for fullscreen mode
        else {
            await player.requestFullscreen();
            document.getElementById("fs-ico").setAttribute("class", "fas fa-compress");
            fulls.setAttribute("title", "exit fullscreen(f)");
        }
    } catch (error) {
        console.log(error);
    }
});

// picutre-in-picture 

var pip = document.getElementById("pip");
pip.addEventListener("click", async function (event) {
    pip.disabled = true;
    try {
        if (video !== document.pictureInPictureElement) {
            await video.requestPictureInPicture();
            pip.disabled = false;
        }
        // If already playing exit mide
        else {
            await document.exitPictureInPicture();
            pip.disabled = false;
        }
    } catch (error) {
        console.log(error);
    } finally {
        pip.disabled = false; // enable toggle at last
    }
});


// setting dropdown
var playback = document.querySelector(".playbacki");
var quality = document.querySelector(".quali");
var dis = document.querySelectorAll(".dis");
var plbk = document.querySelectorAll(".playback");
var qual = document.querySelectorAll(".qual");
var seli = document.querySelector(".dropdown-menu");
playback.addEventListener('click', function (e) {
    e.stopPropagation();
    dis.forEach(element => {
        element.style.display = "none";
    });
    qual.forEach(element => {
        element.style.display = "none";
    });
    plbk.forEach(element => {
        element.style.display = "block";
    });
    plbk.forEach(element => {
        element.addEventListener('click', function () {
            video.playbackRate = element.innerHTML;
            qual.forEach(element => {
                element.style.display = "none";
            });
            plbk.forEach(element => {
                element.style.display = "none";
            });
            dis.forEach(element => {
                element.style.display = "block";
            });
        });
    });
});
quality.addEventListener('click', function (e) {
    e.stopPropagation();
    qual.forEach(element => {
        element.style.display = "block";
    });
    plbk.forEach(element => {
        element.style.display = "none";
    });
    dis.forEach(element => {
        element.style.display = "none";
    });
    qual.forEach(element => {
        element.addEventListener('click', function () {
            qual.forEach(element => {
                element.style.display = "none";
            });
            plbk.forEach(element => {
                element.style.display = "none";
            });
            dis.forEach(element => {
                element.style.display = "block";
            });
        });
    });
})