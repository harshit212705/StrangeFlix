//fetch room id
const room_id = JSON.parse(document.getElementById('room-id').textContent);
        //connect to respective room socket
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/room/'
            + room_id
            + '/'
        );
        //Checks applied on room connection
        chatSocket.onopen = function(e){
             setVideoState();
        }
        var hostTimeout;
        var notJoined = true;
        function setVideoState()
        {
            const message = "Join Request";
            chatSocket.send(JSON.stringify({
                'type' : 'join',
                'message': message
            }));
            $("#overlay").show();
            hostTimeout = setTimeout(function (){
                alert("Host has not joined the room");
                window.location.assign("/room");
            },5000);

        }
        var users = []
        //Update online user list
        function fillUsers()
        {
            document.querySelector('#user-log').innerHTML = '';
            users.forEach(element => {
                document.querySelector('#user-log').innerHTML += element+'<br>';
            });
        }
        //Receive message from Websocket
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if(data.type === 'chat_message')
            {
                document.querySelector('#chat-log').innerHTML += (data.user+' : '+data.message + '<br>');
            }
            if(data.type === 'play')
            {
                document.querySelector('#chat-log').innerHTML += (data.user+' : '+data.message + '<br>');
                togglePlay();
            }
            if(data.type === 'skip')
            {
                document.querySelector('#chat-log').innerHTML += (data.user+' : '+data.message + '<br>');
                skip(data.skipAmount);
            }
            if(data.type === 'upd')
            {
                document.querySelector('#chat-log').innerHTML += (data.user+' : '+data.message + '<br>');
                upd(data.updTime);
            }
            if(data.type === 'hostupd')
            {
                console.log(data.message);
                video.innerHTML = data.videoStatus;
                video.load();
                users = data.users;
                fillUsers();
                upd(data.currentTimeStatus)
                if (data.pausedStatus) {
                    video.pause();
                }
                else{
                    var pl = video.play();
                    if (pl != undefined) {
                        pl.then(_ => {})
                            .catch(error => {
                                video.pause();
                            });
                    }
                }
                if(notJoined)
                {
                    $("#overlay").hide();
                    clearTimeout(hostTimeout);
                    notJoined = false;
                }
            }
            if(data.type === 'add_user')
            {
                
                if(!users.find((s)=> s===data.user))
                {
                    users.push(data.user)
                }
                fillUsers()
            }
            if(data.type === 'remove_user')
            {
                if(user.sfind((s)=> s===data.user))
                {
                    const index = user.indexOf(data.user);
                    if (index > -1) {
                    users.splice(index, 1);
                    }
                }
                fillUsers()
            }
            if(data.type === 'close_room')
            {
                alert(data.message);
                window.close();
            }

        };

        //On when Socket is closed
        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        //Send chat message to the socket
        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'type' : 'chat_message',
                'message': message
            }));
            messageInputDom.value = '';
        };







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

//setting volume of video to be zero as to facilitate autoplay
video.volume = 0;
// progress-bar
function updHelper(e)
{
    const updTime = (e.offsetX / progress.offsetWidth) * video.duration;
    const message = "Time Updata";
    chatSocket.send(JSON.stringify({
        'type' : 'upd',
        'message': message,
        'updTime':updTime
    }));
    
}
function upd(updTime) {
    video.currentTime = updTime;
}
let mousedown = false;

// update when click event is fired
progress.addEventListener('click', updHelper);
progress.addEventListener('mousemove', (e) => mousedown && updHelper(e));
progress.addEventListener('mousedown', () => mousedown = true);
progress.addEventListener('mouseup', () => mousedown = false);


// play/pause
function togglePlayHelper()
{
    const message = "Play Pause";
    chatSocket.send(JSON.stringify({
        'type' : 'play',
        'message': message
    }));

}
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
playpause.addEventListener('click', togglePlayHelper);

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
video.addEventListener('click', togglePlayHelper);

// change the icon based on the event fired
video.addEventListener('play', updateButton);
video.addEventListener('pause', updateButton);

// skip 
function skipHelper()
{
    const message = "Skip";
    chatSocket.send(JSON.stringify({
        'type' : 'skip',
        'message': message,
        'skipAmount':this.dataset.skip 
    }));
}
function skip(skipAmount) {
    video.currentTime += parseFloat(skipAmount);
}

skipButtons.forEach(button => button.addEventListener('click', skipHelper));


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



// theatre mode

var theatre = document.querySelector(".theatre__button");
theatre.addEventListener('click', function (e) {
    var vp = document.querySelector("#video-player");
});







