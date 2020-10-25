# # import pyrebase

# # config = {
# #     "apiKey": "AIzaSyDQKj9_KAG8-uMhWISn87AOHNS-fZuyBYg",
# #     "authDomain": "strangeflix-85ae0.firebaseapp.com",
# #     "databaseURL": "https://strangeflix-85ae0.firebaseio.com",
# #     "projectId": "strangeflix-85ae0",
# #     "storageBucket": "strangeflix-85ae0.appspot.com",
# #     "messagingSenderId": "21362748883",
# #     "appId": "1:21362748883:web:a585c9907c7362c7795326",
# #     "measurementId": "G-61Z61Y7JWN"
# # }

# # firebase = pyrebase.initialize_app(config)
# # storage = firebase.storage()

# # import urllib.request
# # url_link = "https://www.youtube.com/watch?v=3D9g4erlOVE"
# # urllib.request.urlretrieve(url_link, 'video_name.mp4') 

# # from pytube import YouTube
# # videourl = "https://www.youtube.com/watch?v=3D9g4erlOVE"
# # yt = YouTube(videourl)
# # yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
# # # if not os.path.exists(path):
# # #     os.makedirs(path)
# # yt.download('/home/harshit/Desktop/webster2020/', filename='youtube_video')

# # import tldextract
# # ext = tldextract.extract('https://hr-testcases-us-east-1.s3.amazonaws.com/16007/input02.txt?AWSAccessKeyId=AKIAR6O7GJNX5DNFO3PV&Expires=1602080980&Signature=BuwFY6Z9vMkHbKgUkyp34ieOWpA%3D&response-content-type=text%2Fplain')
# # print(ext.domain)


# # import youtube_dl
# # import os

# # import ffmpeg
# # vid = ffmpeg.probe('/home/harshit/Desktop/webster2020/song.mp4')
# # print(vid)


# # GOOD CODE

# # import moviepy.editor as mp
# # duration =  mp.VideoFileClip('/home/harshit/Desktop/webster2020/meta').duration
# # print(int(duration))


# # import filetype

# # kind = filetype.guess('/home/harshit/Desktop/webster2020/meta')
# # if kind is None:
# #     print('Cannot guess file type!')

# # print('File extension: %s' % kind.extension)
# # print('File MIME type: %s' % kind.mime)

# # GOOD CODE

# # ydl_opts = {'outtmpl': '/home/harshit/Desktop/webster2020/m.txt', 'ignoreerrors': True}
# # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# #     try:
# #         dictMeta = ydl.extract_info("https://hr-testcases-us-east-1.s3.amazonaws.com/22937/input00.txt?AWSAccessKeyId=AKIAR6O7GJNX5DNFO3PV&Expires=1602314535&Signature=bn8GwIgarRB4j1ypmkV4CSa7If0%3D&response-content-type=text%2Fplain", download=True)
# #         print(dictMeta)
# #         # dictMeta['formats'][0]['ext'] - extension
# #     except Exception as e:
# #         print('File protected')
# #         print(e)


# # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     # try:
#     # obj = ydl.download(['https://www.hotstar.com/in/sports/cricket/indian-premier-league/mumbai-indians-vs-rajasthan-royals-m701670/match-clips/bumrahs-420-crushes-rrs-soul/1260043466'])
#     # except Exception as e:
#     #     print(e)
#     # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     #     dictMeta = ydl.extract_info(
#     #         "https://www.youtube.com/watch?v=3D9g4erlOVA", download=True)
#     #     print(dictMeta)

#         # for unavailable video or protected video dictmeta = None
#         # duration = dictMeta['duration']

# # ydl_opts = {
# #     'format': 'bestaudio/best',
# #     'outtmpl': 'tmp/%(id)s.%(ext)s',
# #     'noplaylist': True,
# #     'quiet': True,
# #     'prefer_ffmpeg': True,
# #     'logger': MyLogger(),
# #     'audioformat': 'wav',
# #     'forceduration':True
# # }
# # sID = "t99ULJjCsaM"
# # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# #     dictMeta = ydl.extract_info(
# #         "https://www.youtube.com/watch?v={sID}".format(sID=sID),
# #         download=True)



# # import requests 
# # file_url = "https://hr-testcases-us-east-1.s3.amazonaws.com/22937/input00.txt?AWSAccessKeyId=AKIAR6O7GJNX5DNFO3PV&Expires=1602314535&Signature=bn8GwIgarRB4j1ypmkV4CSa7If0%3D&response-content-type=text%2Fplain"
# # r = requests.get(file_url, stream = True) 
# # with open("aws.txt","wb") as f: 
# #     for chunk in r.iter_content(chunk_size=1024): 

# #          # writing one chunk at a time to pdf file 
# #          if chunk: 
# #              f.write(chunk) 

# # path_on_cloud = "videos/youtube.mp4"
# # path_local = "youtube.mp4"
# # obj = storage.child(path_on_cloud).put(path_local)
# # print(obj)
# # storage.child(path_on_cloud).download(path_local)
# # c66211e8-13bc-42cd-9db9-08349ba7dc1c --- webster.pdf
# # f29df98c-1d8d-47f1-b329-f8816d6b295c --- song.mp4
# # 7043cb4a-87ab-449d-bb99-4cdc19e59cb7 --- testcase

# # url = storage.child(path_on_cloud).get_url('')
# # print(url)




# import re
# import os
# from wsgiref.util import FileWrapper
# from django.http import StreamingHttpResponse
# import mimetypes

 
# def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
#     with open(file_name, "rb") as f:
#         f.seek(offset, os.SEEK_SET)
#         remaining = length
#         while True:
#             bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
#             data = f.read(bytes_length)
#             if not data:
#                 break
#             if remaining:
#                 remaining -= len(data)
#             yield data

# from django.views.decorators.http import condition

# # @condition(etag_func=None)
# def stream_video(path):
#     path = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F1ae247bf-5049-409b-8e58-2453ebcb583e.mp4?alt=media&token=d345d5ca-7c94-4c0b-a3b1-6ea77b968164'
#     """ responds to the video file as """
#     range_header = request.META.get('HTTP_RANGE', '').strip()
#     range_header = 'bytes=0-50'
#     range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
#     range_match = range_re.match(range_header)
#     print(range_match)
#     # size = os.path.getsize(path)
#     content_type, encoding = mimetypes.guess_type(path)
#     content_type = content_type or 'application/octet-stream'
#     if range_match:
#         first_byte, last_byte = range_match.groups()
#         first_byte = int(first_byte) if first_byte else 0
#         last_byte = first_byte + 1024 * 1024 * 8 # 8M per piece, the maximum volume of the response body
#         # if last_byte >= size:
#         #     last_byte = size - 1
#         # print(type(first_byte))
#         # print(type(last_byte))
#         length = last_byte - first_byte + 1
#         resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
#         resp['Content-Length'] = str(length)
#         resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, 0)
#     else:
#         # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
#         resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
#         resp['Content-Length'] = str(size)
#     resp['Accept-Ranges'] = 'bytes'
#     print(resp)
#     # for obj in resp:
#     #     print(obj)
#     # return resp


# # stream_video('https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F1ae247bf-5049-409b-8e58-2453ebcb583e.mp4?alt=media&token=d345d5ca-7c94-4c0b-a3b1-6ea77b968164')


# var formData = new FormData();

#             $.ajax({
#                 type: 'POST',
#                 url: '{% url "stream_video" %}',
#                 data: formData,
#                 dataType: 'json',
#                 enctype: 'multipart/form-data',
#                 processData: false,
#                 contentType: false,
#                 success: function (data) {
#                     // console.log(data.resp);
#                     var byteCharacters = atob(data.resp);
#                     var byteNumbers = new Array(byteCharacters.length);
#                     for (let i = 0; i < byteCharacters.length; i++) {
#                         byteNumbers[i] = byteCharacters.charCodeAt(i);
#                     }
#                     var video = document.querySelector('video');
#                     // Show loading animation.
#                     var playPromise = video.play();

#                     if (playPromise !== undefined) {
#                     playPromise.then(_ => {
#                         // Automatic playback started!
#                         // Show playing UI.
#                     })
#                     .catch(error => {
#                         // Auto-play was prevented
#                         // Show paused UI.
#                     });
#                     }
#                     var blobArray = [];
#                     blobArray.push(new Blob([new Uint8Array(byteNumbers)],{'type':'video/mp4'}));
#                     var currentTime = video.currentTime;
#                     var blob = new Blob(blobArray,{'type':'video/mp4'});
#                     video.src = window.URL.createObjectURL(blob);
#                     video.currentTime = currentTime;
#                     $('.progress__filled').css('flex', '0');
#                     $('#video-in-modal').modal('show');
#                     video.play();
#                 }
#             });



# # import re
# # import os
# # from wsgiref.util import FileWrapper
# # from django.http import StreamingHttpResponse
# # import mimetypes

 
# # def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
# #     with open(file_name, "rb") as f:
# #         f.seek(offset, os.SEEK_SET)
# #         remaining = length
# #         while True:
# #             bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
# #             data = f.read(bytes_length)
# #             if not data:
# #                 break
# #             if remaining:
# #                 remaining -= len(data)
# #             yield data


# from django.views.decorators.http import condition
# import base64
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# @csrf_exempt
# # @condition(etag_func=None)
# def stream_video(request):
#     # path = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F1ae247bf-5049-409b-8e58-2453ebcb583e.mp4?alt=media&token=d345d5ca-7c94-4c0b-a3b1-6ea77b968164'
#     path = '/home/harshit/Desktop/webster2020/out1.mp4'
#     """ responds to the video file as """
#     # range_header = request.META.get('HTTP_RANGE', '').strip()
#     # range_header = 'bytes=0-50'
#     # range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
#     # range_match = range_re.match(range_header)
#     # # print(range_match)
#     # size = os.path.getsize(path)
#     # content_type, encoding = mimetypes.guess_type(path)
#     # content_type = content_type or 'application/octet-stream'
#     # if range_match:
#     #     first_byte, last_byte = range_match.groups()
#     #     first_byte = int(first_byte) if first_byte else 0
#     #     last_byte = first_byte + 1024 # 8M per piece, the maximum volume of the response body
#     #     if last_byte >= size:
#     #         last_byte = size - 1
#     #     # print(type(first_byte))
#     #     # print(type(last_byte))
#     #     length = last_byte - first_byte + 1
#     #     resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
#     #     resp['Content-Length'] = str(length)
#     #     resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
#     # else:
#     #     # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
#     #     resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
#     #     resp['Content-Length'] = str(size)
#     # resp['Accept-Ranges'] = 'bytes'
#     # # print(resp)
#     # for key, val in resp.items():
#     #     print(key)
#     #     print(val)
#     # e = ''
#     # for e in resp: 
#     #     print(e.decode())
#     # print(resp.streaming_content)
#     start_time = 60
#     end_time = 80
#     ffmpeg_extract_subclip("/home/harshit/Desktop/webster2020/song.mp4", start_time, end_time, targetname="/home/harshit/Desktop/webster2020/out1.mp4")
#     with open(path, "rb") as videoFile:
#         text = base64.b64encode(videoFile.read()).decode('utf-8')
#         # print(text)
#     context = {
#         'resp': text
#     }
#     return JsonResponse(context)



#             var formData = new FormData();

#             $.ajax({
#                 type: 'POST',
#                 url: '{% url "stream_video" %}',
#                 data: formData,
#                 dataType: 'json',
#                 enctype: 'multipart/form-data',
#                 processData: false,
#                 contentType: false,
#                 success: function (data) {
#                     // console.log(data.resp);
#                     var byteCharacters = atob(data.resp);
#                     var byteNumbers = new Array(byteCharacters.length);
#                     for (let i = 0; i < byteCharacters.length; i++) {
#                         byteNumbers[i] = byteCharacters.charCodeAt(i);
#                     }
#                     var video = document.querySelector('video');
#                     // Show loading animation.
#                     var playPromise = video.play();

#                     if (playPromise !== undefined) {
#                     playPromise.then(_ => {
#                         // Automatic playback started!
#                         // Show playing UI.
#                     })
#                     .catch(error => {
#                         // Auto-play was prevented
#                         // Show paused UI.
#                     });
#                     }
#                     var blobArray = [];
#                     blobArray.push(new Blob([new Uint8Array(byteNumbers)],{'type':'video/mp4'}));
#                     var currentTime = video.currentTime;
#                     var blob = new Blob(blobArray,{'type':'video/mp4'});
#                     video.src = window.URL.createObjectURL(blob);
#                     video.currentTime = currentTime;
#                     $('.progress__filled').css('flex', '0');
#                     $('#video-in-modal').modal('show');
#                     video.play();
#                 }
#             });


#             var formData = new FormData();

#             $.ajax({
#                 type: 'POST',
#                 url: '{% url "stream_video" %}',
#                 data: formData,
#                 dataType: 'json',
#                 enctype: 'multipart/form-data',
#                 processData: false,
#                 contentType: false,
#                 success: function (data) {
#                     console.log(data.resp);
#                     var byteCharacters = atob(data.resp);
#                     var byteNumbers = new Array(byteCharacters.length);
#                     for (let i = 0; i < byteCharacters.length; i++) {
#                         byteNumbers[i] = byteCharacters.charCodeAt(i);
#                     }
#                     var video = document.querySelector('movie_video_player');
#                     // Show loading animation.
#                     var playPromise = video.play();

#                     if (playPromise !== undefined) {
#                     playPromise.then(_ => {
#                         // Automatic playback started!
#                         // Show playing UI.
#                     })
#                     .catch(error => {
#                         // Auto-play was prevented
#                         // Show paused UI.
#                     });
#                     }
#                     var blobArray = [];
#                     blobArray.push(new Blob([new Uint8Array(byteNumbers)],{'type':'video/mp4'}));
#                     var currentTime = video.currentTime;
#                     var blob = new Blob(blobArray,{'type':'video/mp4'});
#                     video.src = window.URL.createObjectURL(blob);
#                     video.currentTime = currentTime;
#                     $('.progress__filled').css('flex', '0');
#                     // $('#video-in-modal').modal('show');
#                     video.play();
#                 }
#             });


# import base64
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# # @csrf_exempt
# # def stream_video(request):
#     # # path = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F1ae247bf-5049-409b-8e58-2453ebcb583e.mp4?alt=media&token=d345d5ca-7c94-4c0b-a3b1-6ea77b968164'
#     # path = '/home/harshit/Desktop/webster2020/out2.mp4'
#     # start_time = 250
#     # end_time = 270
#     # ffmpeg_extract_subclip("https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fab783e7c-1bfb-4992-89e3-fa1fcd708936.mp4?alt=media&token=69b4c009-4bf3-4ef7-ad68-faafc91fcd4c", start_time, end_time, targetname="/home/harshit/Desktop/webster2020/out2.mp4")
#     # with open(path, "rb") as videoFile:
#     #     text = base64.b64encode(videoFile.read()).decode('utf-8')
#     #     # print(text)
#     # context = {
#     #     'resp': text
#     # }
# #     return JsonResponse(context)





# playerhtml = <div class="player" id="video-player"><!-- video-head  --><div class="video-head"></div><!-- video-body  --><div class="video-body"><video class="player__video viewer" id="movie_video_player" preload="metadata"><source id="insert-movie-video" src="" type="video/mp4"></video></div><!-- video-footer  --><div class="video-footer"><div class="player__controls" id="plact"><!-- progress-bar  --><div class="progress"><div class="progress__filled"></div></div><!-- play/pause  --><button class="player__button toggle" data-toggle="tooltip" title="pause"><i id="play-icon"class="fas fa-play"></i></button> <!-- skip 10s backword --><button data-skip="-10" class="backword__button" data-toggle="tooltip" title="Skip -10s">« 10s</button><!-- skip 10s forward --><button data-skip="10" class="forward__button" data-toggle="tooltip" title="Skip 10s">10s »</button><!-- volume  --><button class="volume__button" data-toggle="tooltip" title="mute" id="volume"><i id="vol-ico" class="fas fa-volume-up"></i></button><input type="range" name="volume" id="vol-ran" class="player__slider" min="0" max="1" step="0.05" value="1"><!-- video timer  --><button id="progressTime" class="timer__button"><span id="current">00:00 / </span><span id="duration">00:00</span></button><!-- playbackrate  --><!-- <input type="range" name="playbackRate" class="player__slider" min="0.5" max="2" step="0.1" value="1"> --><div class="fullscreen"><!-- setting  --><!-- <button id="setting" class="setting__button" data-toggle="tooltip" title="setting"><span class="px-4"><i id="setting-ico" class="fas fa-cog"></i></span></button> --><div class="btn-group dropup"><button id="setting" class="setting__button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="px-4"><i id="setting-ico" class="fas fa-cog"></i></span></button><div class="dropdown-menu"><a href="#" class="dropdown-item playbacki dis">Playback speed</a><a href="#" class="dropdown-item quali dis">Video Quality</a><a href="#" class="dropdown-item shortcuts dis">Keyboard shortcuts</a><a href="#" class="dropdown-item playback">0.25</a><a href="#" class="dropdown-item playback">0.5</a><a href="#" class="dropdown-item playback">1</a><a href="#" class="dropdown-item playback">1.25</a><a href="#" class="dropdown-item playback">1.5</a><a href="#" class="dropdown-item playback">1.75</a><a href="#" class="dropdown-item playback">2</a><a href="#" class="dropdown-item qual">Auto</a><a href="#" class="dropdown-item qual">480p</a><a href="#" class="dropdown-item qual">720p</a><a href="#" class="dropdown-item qual">1080p</a></div></div><!-- picture-in-picture  --><button id="pip" class="pip__button" data-toggle="tooltip" title="picture-in-picture"><span class="px-4"><i id="pip-ico" class="fas fa-window-maximize"></i></span></button><!-- theatre view  --><button class="theatre__button" data-toggle="tooltip" title="theatre mode"><span class="px-4"><i id="th-ico" class="fas fa-mobile-alt"></i></span></button><!-- fullscreen  --><button id="fs" class="fs__button" data-toggle="tooltip" title="fullscreen(f)"><span class="px-4"><i id="fs-ico" class="fas fa-expand"></i></span></button></div></div></div></div>

import requests

# resume_header = {'Range':'bytes=100-300000'}
url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F0b3aaf33-f04d-4949-aafc-f147571b2a6e.mp4?alt=media&token=0c45781c-001f-48f4-a7cd-ed0f569f5c1d'
# r = requests.get(url, stream=True, headers=resume_header)
# with open('filename.mp4','wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#         f.write(chunk)


r = requests.get(url, stream=True)
# r.raise_for_status()
with open("/home/harshit/Desktop/webster2020/check.mp4", 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)



@condition(etag_func=None)
def stream_video(request, video_obj):
    print(request.META)
    if video_obj.video_type == 1:
        video_details = FreeSeriesVideos.objects.filter(video_id=video_obj).first()
        if video_details is None:
            video_details = FreeMovieVideo.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 2:
        video_details = SeriesVideos.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 3:
        video_details = MovieVideo.objects.filter(video_id=video_obj).first()

    # getting firebase url for uploaded video file
    path_on_cloud = 'videos/' + video_details.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[video_details.extension]
    # firebase_video_url = storage.child(path_on_cloud).get_url(video_details.firebase_token)
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fab783e7c-1bfb-4992-89e3-fa1fcd708936.mp4?alt=media&token=69b4c009-4bf3-4ef7-ad68-faafc91fcd4c'
    firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F0b3aaf33-f04d-4949-aafc-f147571b2a6e.mp4?alt=media&token=0c45781c-001f-48f4-a7cd-ed0f569f5c1d'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F05628f4f-11b2-4bb0-bc93-76bb13fa3221.mp4?alt=media&token=47726f97-1404-40bf-bdf9-75b389c8f836'
    # firebase_video_url = '/home/harshit/Desktop/webster2020/song.mp4'
    """ responds to the video file as """
    # base_url = "https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F05628f4f-11b2-4bb0-bc93-76bb13fa3221.mp4"
    # import requests
    # res = requests.get(base_url).body()
    # print(res)
    print('video')
    # req = urllib.request.Request(firebase_video_url, headers=request.META)
    # rr = 'bytes=' + str(first_byte) + '-' + str(first_byte + 503500)
    # # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36')
    # req.add_header('Range', rr) # <=== range header
    # res = urllib.request.urlopen(req)
    # import requests
    # r = requests.get(firebase_video_url, request.META)
    # print(r.headers)
    # print(r.status_code)
    # a = res.read()
    # return a
    # path = '/home/harshit/Desktop/webster2020/sample_video.mp4'
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = 574823
    # size = 3151886
    # size = 16508537
    if range_match:
        print("range perfect")
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        # req = urllib.request.Request(firebase_video_url)
        # rr = 'bytes=' + str(first_byte) + '-' + str(first_byte + 503500)
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36')
        # req.add_header('Range', rr) # <=== range header
        # res = urllib.request.urlopen(req)

        # extension = str(firebase_video_url).split('?')[0][-3:]
        # unique_video_name = str(uuid.uuid4())
        # print(unique_video_name)
        # video_fragment_save_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + extension

        # with open(video_fragment_save_path, 'wb') as f:
        #     f.write(res.read())

        # content_type, encoding = mimetypes.guess_type(path)
        # content_type = content_type or 'application/octet-stream'
        content_type = 'video/mp4'
        # print(content_type)
        # print(encoding)
        resp = StreamingHttpResponse(response_iter(firebase_video_url, request), status=206, content_type=content_type)
        # resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        print('ggod')
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        print('response sent')
        # return redirect(firebase_video_url)
        # os.remove(video_fragment_save_path)
    else:
        print("range not fine")
        extension = str(firebase_video_url).split('?')[0][-3:]
        unique_video_name = str(uuid.uuid4())
        video_fragment_save_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + 'flv'

        req = urllib.request.Request(firebase_video_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0')
        # req.add_header('Range', range_header) # <=== range header
        res = urllib.request.urlopen(req)

        with open(video_fragment_save_path, 'wb') as f:
            f.write(res.read())

        content_type, encoding = mimetypes.guess_type(video_fragment_save_path)
        content_type = content_type or 'application/octet-stream'
        # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        resp = StreamingHttpResponse(FileWrapper(open(video_fragment_save_path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
        # os.remove(video_fragment_save_path)
    resp['accept-ranges'] = 'bytes'
    print('go')
    return resp




 // // function to keep fetching next packet for movie video
        // window.setInterval(function(){
        //     // call your function here
        //     var video = document.getElementById('movie-video');
        //     if (video != null && !video.paused) {
        //         if ((movie_maxtime_fetched - movie_previous_time_watched - Math.ceil(video.currentTime)) == 9) {
        //             console.log('fetching');
        //             var movie_id = document.getElementById('selected_movie_id').innerHTML;
        //             var data = {
        //                 'movie_id': movie_id,
        //                 'start_time':  movie_maxtime_fetched,
        //             }

        //             // adding data to javascript form which is to be send over ajax request
        //             var formData = new FormData();
        //             formData.append('data', JSON.stringify(data));

        //             $.ajax({
        //                 type: 'POST',
        //                 url: '',
        //                 data: formData,
        //                 dataType: 'json',
        //                 enctype: 'multipart/form-data',
        //                 processData: false,
        //                 contentType: false,
        //                 success: function (data) {
        //                     // checking and handling error conditions
        //                     if (data.is_movie_exists != '') {
        //                         movie_fetcherror = data.is_movie_exists;
        //                     } else if (data.is_user_subscribed != '') {
        //                         movie_fetcherror = data.is_user_subscribed;
        //                     } else if (data.is_successful != '') {
        //                         console.log('fetched');
        //                         var byteCharacters = atob(data.stream);
        //                         var byteNumbers = new Array(byteCharacters.length);
        //                         for (let i = 0; i < byteCharacters.length; i++) {
        //                             byteNumbers[i] = byteCharacters.charCodeAt(i);
        //                         }

        //                         // // Show loading animation.
        //                         // var playPromise = video.play();

        //                         // if (playPromise !== undefined) {
        //                         //     playPromise.then(_ => {
        //                         //         // Automatic playback started!
        //                         //         // Show playing UI.
        //                         //     })
        //                         //     .catch(error => {
        //                         //         // Auto-play was prevented
        //                         //         // Show paused UI.
        //                         //     });
        //                         // }
        //                         // movie_total_duration = data.movie_duration
        //                         var blobArray = [];
        //                         blobArray.push(new Blob([new Uint8Array(byteNumbers)],{'type':'video/mp4'}));
        //                         // var currentTime = video.currentTime;
        //                         var blob = new Blob(blobArray,{'type':'video/mp4'});
        //                         movie_nextpacket_url = window.URL.createObjectURL(blob);
        //                         // video.currentTime = currentTime;
        //                         // movie_previous_time_watched = 0;     // if using history add history time
        //                         movie_packet_start_time = movie_maxtime_fetched;
        //                         movie_maxtime_fetched = Math.min(movie_maxtime_fetched + 10, movie_total_duration);

        //                         // $('.progress__filled').css('flex', '0');
        //                         // video.play();

        //                     } else {
        //                         alert('Some unexpected error has occured. Try again.');
        //                     }
        //                 }
        //             });
        //         }
        //     }
        // }, 1000);


        // // function to set new packet to video tag
        // window.setInterval(function(){
        //     // call your function here
        //     var video = document.getElementById('movie-video');
        //     if (video != null) {
        //         if (movie_packet_start_time == (movie_previous_time_watched + Math.ceil(video.currentTime))) {
        //             if (movie_fetcherror != '') {
        //                 alert(movie_fetcherror);
        //             }
        //             else{
        //                 if (movie_nextpacket_url != '') {
        //                     console.log('setting');
        //                     video.src = movie_nextpacket_url;
        //                     movie_nextpacket_url = '';
        //                     movie_previous_time_watched = movie_packet_start_time;
        //                     video.play();
        //                     console.log('done');
        //                 }
        //             }
        //         }
        //     }
        // }, 1000);







<div id="video_with_comments" style="display: none;">
        <!-- video running section  -->
        <div class="runner-section container-fluid">
            <div class="row">
                <!-- video-player  -->
                <div class="col-xl-9 col-lg-8 col-md-7 player-wrapper">
                    <!-- if paid  -->
                    <div class="player" id="video-player">

                        <!-- video-head  -->
                        <div class="video-head">
                            <div class="text-white">
                                <h3 class="font-weight-bold">heading</h4>
                            </div>
                        </div>
                        <!-- video-body  -->
                        <div class="video-body">
                            <video class="player__video viewer" id="video" preload="metadata">
                                <source
                                    src=""
                                    id="insert-vid" type="video/mp4">
                            </video>
                        </div>
                        <!-- video-footer  -->
                        <div class="video-footer">
                            <div class="player__controls" id="plact">
                                <!-- progress-bar  -->
                                <div class="progress">
                                    <div class="progress__filled"></div>
                                </div>


                                <!-- play/pause  -->
                                <button class="player__button toggle" data-toggle="tooltip" title="pause"><i id="play-icon"
                                        class="fas fa-play"></i></button>

                                <!-- skip 10s backword -->
                                <button data-skip="-10" class="backword__button" data-toggle="tooltip" title="Skip -10s">«
                                    10s</button>

                                <!-- skip 10s forward -->
                                <button data-skip="10" class="forward__button" data-toggle="tooltip" title="Skip 10s">10s
                                    »</button>

                                <!-- volume  -->
                                <button class="volume__button" data-toggle="tooltip" title="mute" id="volume"><i id="vol-ico"
                                        class="fas fa-volume-up"></i></button>
                                <input type="range" name="volume" id="vol-ran" class="player__slider" min="0" max="1"
                                    step="0.05" value="1">

                                <!-- video timer  -->
                                <button id="progressTime" class="timer__button">
                                    <span id="current">00:00 / </span>
                                    <span id="duration">00:00</span>
                                </button>
                                <!-- playbackrate  -->
                                <!-- <input type="range" name="playbackRate" class="player__slider" min="0.5" max="2" step="0.1" value="1"> -->

                                <div class="fullscreen">
                                    <!-- setting  -->
                                    <!-- <button id="setting" class="setting__button" data-toggle="tooltip" title="setting"><span
                                            class="px-4"><i id="setting-ico" class="fas fa-cog"></i></span></button> -->

                                    <button type="button" class="prev-button mr-3">
                                        <i class="fas fa-step-backward"></i>
                                    </button>
                                    <button type="button" class="next-button">
                                        <i class="fas fa-step-forward"></i>
                                    </button>
                                    <div class="btn-group dropup">
                                        <button id="setting" class="setting__button" data-toggle="dropdown" aria-haspopup="true"
                                            aria-expanded="false"><span class="px-4"><i id="setting-ico"
                                                    class="fas fa-cog"></i></span></button>
                                        <div class="dropdown-menu plbcrt">
                                            <a href="#" class="dropdown-item playbacki dis">Playback speed</a>
                                            <a href="#" class="dropdown-item quali dis">Video Quality</a>
                                            <a href="#" class="dropdown-item shortcuts dis">Keyboard shortcuts</a>
                                            <a href="#" class="dropdown-item playback">0.25</a>
                                            <a href="#" class="dropdown-item playback">0.5</a>
                                            <a href="#" class="dropdown-item playback">1</a>
                                            <a href="#" class="dropdown-item playback">1.25</a>
                                            <a href="#" class="dropdown-item playback">1.5</a>
                                            <a href="#" class="dropdown-item playback">1.75</a>
                                            <a href="#" class="dropdown-item playback">2</a>
                                            <a href="#" class="dropdown-item qual">Auto</a>
                                            <a href="#" class="dropdown-item qual">480p</a>
                                            <a href="#" class="dropdown-item qual">720p</a>
                                            <a href="#" class="dropdown-item qual">1080p</a>
                                        </div>
                                    </div>
                                    <!-- picture-in-picture  -->
                                    <button id="pip" class="pip__button" data-toggle="tooltip" title="picture-in-picture"><span
                                            class="px-4"><i id="pip-ico" class="fas fa-window-maximize"></i></span></button>
                                    <!-- theatre view  -->
                                    <button class="theatre__button" data-toggle="tooltip" title="theatre mode"><span
                                            class="px-4"><i id="th-ico" class="fas fa-arrows-alt-v"></i></span></button>
                                    <!-- fullscreen  -->
                                    <button id="fs" class="fs__button" data-toggle="tooltip" title="fullscreen"><span
                                            class="px-4"><i id="fs-ico" class="fas fa-expand"></i></span></button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- else this  -->
                    <!-- pay cost per video  -->
                    <!-- <div class="text-center text-muted text-white">
                        pay $(number) to watch this video 
                        <button class="btn btn-primary btn-sm" type="button">Pay</button>
                    </div> -->

                </div>

                <!-- sidebar content  -->
                <div class="col-xl-3 col-lg-4 col-md-5 playlist-container" style="background: white;color: black;">
                    <div class="card comment">
                        <div class="card-header">
                            <h4>comments</h4>
                        </div>
                        <div class="card-body">
                            <ul id="vid-comments">
                                <li>
                                    <div class="row media">
                                        <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2">
                                            <!-- user-profile  -->
                                            <img src="/img/img1.png" alt="" class="img-fluid">
                                        </div>
                                        <!-- video-desccription  -->
                                        <div class="col-xl-10 col-lg-10 col-md-10 col-sm-10">
                                            <div class="media-body px-1">
                                                <span class="font-weight-bold">
                                                    S1 E1 - date
                                                </span>
                                                <div class="d-cent text-justify">
                                                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                                                    Distinctio doloribus explicabo enim quae tenetur omnis, optio
                                                    dolorem et. Eaque similique obcaecati laborum blanditiis
                                                    officiis veniam maxime veritatis alias inventore voluptates!
                                                </div>
                                                <button type="button" class="flg-comm-button px-2" data-toggle="modal"
                                                data-target="#flagCommentCenter">
                                                        <i class="fas fa-flag"></i>
                                                </button>
                                                <button type="button" class="show-mr-button">
                                                        show
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="whole-sect">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-xl-9 col-lg-6 col-md-7">
                        <!-- description flag section  -->
                        <div class="container-fluid descript-sect my-4">
                            <div class="row">
                                <div class="col-xl-8 col-lg-8 col-md-8">
                                    <div class="vid-desc text-left pb-3">
                                        <div class="vid-hd py-1" id="video_description_1">
                                            Series name || Season name || Episode name || SNo.ENo || Date
                                        </div>
                                        <div class="vid-cat py-1" id="video_description_2">
                                            Categories || Language || Subcategories || tags
                                        </div>
                                        <div class="vid-des py-1" id="video_description_3">
                                            Description of videos
                                        </div>
                                    </div>
                                </div>
                                <div class="col-xl-4 col-lg-6 col-md-4 pb-3">
                                    <div class="flg-sect d-flex flex-row-reverse align-items-end">
                                        <button type="button" class="add-to-fav mx-3" data-toggle="tooltip"
                                            data-placement="bottom" title="Add to favourites">
                                            <span class="ico-cont bg-danger text-center py-2 px-2">
                                                <span class="py-3">
                                                    <i class="fas fa-plus"></i>
                                                </span>
                                            </span>
                                            <p class="add-to-fav-title py-3">Favourites</p>
                                        </button>
                                        <button type="button" class="vid-flag mx-3" data-toggle="modal"
                                            data-target="#flagCenter">
                                            <span class="ico-cont bg-danger text-center py-2 px-2">
                                                <span class="py-3">
                                                    <i class="fas fa-flag"></i>
                                                </span>
                                            </span>
                                            <p class="add-to-flag py-3">Flag</p>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>










import requests
def response_iter(url, first_byte):
    ran = 'bytes=' + str(first_byte) + '-'
    headers = {'Range': ran}
    r = requests.get(url, headers=headers, stream=True)
    # r.raise_for_status()
    # with open("/home/harshit/Desktop/webster2020/check.mp4", 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
            # print(chunk)
            yield chunk


# def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
#     with open(file_name, "rb") as f:
#         f.seek(offset, os.SEEK_SET)
#         remaining = length
#         while True:
#             bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
#             data = f.read(bytes_length)
#             if not data:
#                 break
#             if remaining:
#                 remaining -= len(data)
#             # print(data)
#             yield data


from django.views.decorators.http import condition

@condition(etag_func=None)
def stream_video(request, video_obj):
    # print(request.META)
    if video_obj.video_type == 1:
        video_details = FreeSeriesVideos.objects.filter(video_id=video_obj).first()
        if video_details is None:
            video_details = FreeMovieVideo.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 2:
        video_details = SeriesVideos.objects.filter(video_id=video_obj).first()
    elif video_obj.video_type == 3:
        video_details = MovieVideo.objects.filter(video_id=video_obj).first()

    # getting firebase url for uploaded video file
    path_on_cloud = 'videos/' + video_details.firebase_save_name + '.' + VIDEO_EXTENSION_REVERSE[video_details.extension]
    firebase_video_url = storage.child(path_on_cloud).get_url(video_details.firebase_token)
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fab783e7c-1bfb-4992-89e3-fa1fcd708936.mp4?alt=media&token=69b4c009-4bf3-4ef7-ad68-faafc91fcd4c'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F0b3aaf33-f04d-4949-aafc-f147571b2a6e.mp4?alt=media&token=0c45781c-001f-48f4-a7cd-ed0f569f5c1d'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2F05628f4f-11b2-4bb0-bc93-76bb13fa3221.mp4?alt=media&token=47726f97-1404-40bf-bdf9-75b389c8f836'
    # firebase_video_url = 'https://firebasestorage.googleapis.com/v0/b/strangeflix-85ae0.appspot.com/o/videos%2Fa5674582-2005-4f44-a9b0-abc25016a246.mp4?alt=media&token=d74a389b-ce2a-478f-9c16-4d68fd95c9d8'
    # firebase_video_url = '/home/harshit/Desktop/webster2020/song.mp4'
    # path = '/home/harshit/Desktop/webster2020/sample_video.mp4'

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    base_url = str(firebase_video_url).split('?')[0]
    video_details = requests.get(base_url).text
    details_dict = eval(video_details)
    size = int(details_dict['size'])

    if range_match:
        print("range perfect")
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        content_type = 'video/mp4'
        resp = StreamingHttpResponse(response_iter(firebase_video_url, first_byte), status=206, content_type=content_type)
        # resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        # print('response sent')
        # os.remove(video_fragment_save_path)
    else:
        return render(request, 'templates/404.html')
        # print("range not fine")
        # extension = str(firebase_video_url).split('?')[0][-3:]
        # unique_video_name = str(uuid.uuid4())
        # video_fragment_save_path = VIDEO_BASE_FILEPATH + '/' + unique_video_name + '.' + 'flv'

        # req = urllib.request.Request(firebase_video_url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0')
        # # req.add_header('Range', range_header) # <=== range header
        # res = urllib.request.urlopen(req)

        # with open(video_fragment_save_path, 'wb') as f:
        #     f.write(res.read())

        # content_type, encoding = mimetypes.guess_type(video_fragment_save_path)
        # content_type = content_type or 'application/octet-stream'
        # # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        # resp = StreamingHttpResponse(FileWrapper(open(video_fragment_save_path, 'rb')), content_type=content_type)
        # resp['Content-Length'] = str(size)
        # # os.remove(video_fragment_save_path)
    resp['accept-ranges'] = 'bytes'
    print('go')
    return resp



def fetch_video(request, video_id):
    video_obj = Videos.objects.filter(video_id=video_id).first()
    if video_obj:
        if video_obj.video_type == 1:
            return stream_video(request, video_obj)
        else:
            if request.user.is_authenticated:
                # checking logged in user subscription plan details
                subscribe = Subscriptions.objects.filter(user=request.user, end_date__gt=datetime.now(tz=timezone.utc)).order_by('-end_date').first()
                if subscribe:
                    return stream_video(request, video_obj)
                else:
                    return render(request, 'templates/404.html')
            else:
                return render(request, 'templates/404.html')
    else:
        return render(request, 'templates/404.html')
