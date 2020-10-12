######################################################3
# from django.conf import settings
# import pyrebase

# config = {
#     "apiKey": settings.FIREBASE_API_KEY,
#     "authDomain": settings.FIREBASE_AUTH_DOMAIN,
#     "databaseURL": settings.FIREBASE_DATABASE_URL,
#     "projectId": settings.FIREBASE_PROJECT_ID,
#     "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
#     "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
#     "appId": settings.FIREBASE_APP_ID,
#     "measurementId": settings.FIREBASE_MEASUREMENT_ID
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# path_on_cloud = "videos/bell_bottom_teaser.mp4"
# path_local = "/home/harshit/Desktop/webster2020/youtube_video.mp4"
# obj = storage.child(path_on_cloud).put(path_local)
# print(obj)
#############FINAL CODE FOR FIREBASE UPLOADS####################


# import urllib.request
# url_link = "https://www.youtube.com/watch?v=3D9g4erlOVE"
# urllib.request.urlretrieve(url_link, 'video_name.mp4') 

# from pytube import YouTube
# videourl = "https://www.youtube.com/watch?v=3D9g4erlOVE"
# yt = YouTube(videourl)
# yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
# # if not os.path.exists(path):
# #     os.makedirs(path)
# yt.download('/home/harshit/Desktop/webster2020/', filename='youtube_video')

# import tldextract
# ext = tldextract.extract('https://hr-testcases-us-east-1.s3.amazonaws.com/16007/input02.txt?AWSAccessKeyId=AKIAR6O7GJNX5DNFO3PV&Expires=1602080980&Signature=BuwFY6Z9vMkHbKgUkyp34ieOWpA%3D&response-content-type=text%2Fplain')
# print(ext.domain)


# import youtube_dl
# import os

# ydl_opts = {'outtmpl': '/home/harshit/Desktop/webster2020/metavideo', 'ignoreerrors': True}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # try:
    # obj = ydl.download(['https://www.hotstar.com/in/sports/cricket/indian-premier-league/mumbai-indians-vs-rajasthan-royals-m701670/match-clips/bumrahs-420-crushes-rrs-soul/1260043466'])
    # except Exception as e:
    #     print(e)
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     try:
    #         dictMeta = ydl.extract_info("https://www.youtube.com/watch?v=3D9g4erlOVA", download=True)
    #         print(dictMeta)
    #     except Exception as e:
    #         print('File protected')
    #         print(e)

        # for unavailable video or protected video dictmeta = None
        # duration = dictMeta['duration']

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': 'tmp/%(id)s.%(ext)s',
#     'noplaylist': True,
#     'quiet': True,
#     'prefer_ffmpeg': True,
#     'logger': MyLogger(),
#     'audioformat': 'wav',
#     'forceduration':True
# }
# sID = "t99ULJjCsaM"
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     dictMeta = ydl.extract_info(
#         "https://www.youtube.com/watch?v={sID}".format(sID=sID),
#         download=True)



# import requests 
# file_url = "https://www.youtube.com/watch?v=3D9g4erlOVE.mp4"
# r = requests.get(file_url, stream = True) 
# with open("youtube.mp4","wb") as f: 
#     for chunk in r.iter_content(chunk_size=1024): 

#          # writing one chunk at a time to pdf file 
#          if chunk: 
#              f.write(chunk) 

# path_on_cloud = "videos/youtube.mp4"
# path_local = "youtube.mp4"
# obj = storage.child(path_on_cloud).put(path_local)
# print(obj)
# storage.child(path_on_cloud).download(path_local)
# c66211e8-13bc-42cd-9db9-08349ba7dc1c --- webster.pdf
# f29df98c-1d8d-47f1-b329-f8816d6b295c --- song.mp4
# 7043cb4a-87ab-449d-bb99-4cdc19e59cb7 --- testcase

# url = storage.child(path_on_cloud).get_url('')
# print(url)

