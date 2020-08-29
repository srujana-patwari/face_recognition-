from pytube import YouTube

video_list = ['https://www.youtube.com/watch?v=wtQ_tBSrgVM','https://www.youtube.com/watch?v=rKmWRELlXAc']

for i in video_list:
    yt = YouTube(i)
    try:
        dw = yt.streams.first()
        dw.download('D:/')
        print('Downloaded',i)
    except:
        print('Download Failed For',i)

#or in two lines we can write as
#import pytube
#pytube.YouTube('https://www.youtube.com/watch?v=wtQ_tBSrgVM').streams.first().download('D:/')

#we can download playlist as
import pytube

pytube.Playlist('https://www.youtube.com/watch?v=nIiQRza3Q-s').streams.first().download('D:/')



