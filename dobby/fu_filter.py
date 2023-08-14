from config.settings import MEDIA_ROOT, STATIC_ROOT
from dobby.clova import ClovaSpeechClient
import moviepy.editor as mp
import re

def filter_srt(txt_pth, video_pth):
    res = ClovaSpeechClient().req_upload(file=video_pth, completion='sync')
    dt = res.json()
    test = dt['segments']
    # 파일 저장되는 경로 -> 변경 해줘야함
    with open(txt_pth, 'a') as f:
        for i in range(len(test)):
            f.write(str(test[i]['start']//1000))
            f.write("-")
            f.write(str(test[i]['end']//1000))
            f.write(str(test[i]['text']))
            f.write("\n")



def filter_audio(start, end, video_pth):
    end = str(int(end) + 1)
    audios = []
    audio = mp.AudioFileClip(video_pth)
    filter_audio = mp.AudioFileClip(STATIC_ROOT+'\\filter.mp3')

    if len(start) < 2:
       start = '0' + start
       print(start)
    start_audio = audio.subclip("00:00:00","00:00:{}".format(start))

    audios.append(start_audio)

    filter = filter_audio.subclip("00:00:00","00:00:06")

    audios.append(filter)

    end_audio = audio.subclip("00:00:{}".format(end),"00:00:13") # 하드코딩

    audios.append(end_audio)

    audioClips = mp.concatenate_audioclips([audio for audio in audios])
    audioClips.write_audiofile(MEDIA_ROOT+"\\"+"filter_audio.mp3")

def total_filter(txt_pth, video_pth):
  with open(txt_pth,encoding='cp949') as f:
      while True:
          line = f.readline()
          if not line :
              break
          if "새끼" in line:
              time = re.findall('\d+', line)
              
              start = time[0]
              end = time[1]

              filter_audio(start,end,video_pth)



def combine_audio2(audio_pth,video_pth,file_name):

  videoclip = mp.VideoFileClip(video_pth) 
  audioclip = mp.AudioFileClip(audio_pth) 


  videoclip = videoclip.set_audio(audioclip) 
  videoclip.write_videofile(MEDIA_ROOT+"/filter/"+file_name, codec='libx264', audio_codec='aac')