import cv2
import sys
from dobby.clova import ClovaSpeechClient
import numpy as np
import moviepy.editor as mp
from PIL import ImageFont,Image,ImageDraw

from config.settings import MEDIA_ROOT, STATIC_ROOT

def subtitle_fps(txt_pth, video_pth):
    res = ClovaSpeechClient().req_upload(file=video_pth, completion='sync')
    dt = res.json()
    cap1 = cv2.VideoCapture(video_pth)
    fps2 = cap1.get(cv2.CAP_PROP_FPS) +2
    fps2 = round(fps2)
    test = dt['segments']
    cnt = 0
    start_point = 0
    # 파일 저장되는 경로 -> 변경 해줘야함
    with open(txt_pth, 'a') as f:
        for i in range(len(test)):
            if i == 0 and (test[i]['start']//1000) != 0:
                cnt = (test[i]['start']//1000)* fps2
                for j in range(cnt):
                    f.write(str(" "))
                    f.write("\n")
            if i != 0 and i< len(test)-1 and (test[i]['end']//1000)+1 != (test[i+1]['start']//1000):
                cnt = ((test[i+1]['start']//1000) - (test[i]['end']//1000))* fps2
                for j in range(cnt):
                    f.write(str(" "))
                    f.write("\n")
            cnt = ((test[i]['end']//1000) - (test[i]['start']//1000))* fps2
            for j in range(cnt):
                f.write(str(test[i]['text']))
                f.write("\n")
                start_point += 1



def subtitle_generator(txt_pth,video_pth,fontnum,font_col_num,font_bg_num):

  cap1 = cv2.VideoCapture(video_pth)
  file = open(txt_pth, "r")

  w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
  h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

  fps2 = cap1.get(cv2.CAP_PROP_FPS)
  fps2 = round(fps2)
  fourcc = cv2.VideoWriter_fourcc(*"mp4v")
  delay2 = round(1000/fps2)

  out = cv2.VideoWriter(MEDIA_ROOT+"/"+"no_voice.mp4",fourcc,fps2,(w,h))



  fps1 = cap1.get(cv2.CAP_PROP_FPS)
#   delay2 = round(1000/fps1)


  if not cap1.isOpened() :
      print("video open failed")
      sys.exit()

  fontnum = fontnum
  font_col_num = font_col_num
  font_bg_num = font_bg_num

  if fontnum == 1:
      fontpath = STATIC_ROOT+'\\HiMelody-Regular.ttf'
  elif fontnum == 2:
      fontpath = STATIC_ROOT+'\\EastSeaDokdo-Regular.ttf'
  elif fontnum == 3:
      fontpath = STATIC_ROOT+'\\PoorStory-Regular.ttf'

#   폰트컬러 흰,검,빨 순
  if font_col_num == 1:
      fontcolor = (255,255,255)
  elif font_col_num == 2:
      fontcolor = (0,0,0)
  elif font_col_num == 3:
      fontcolor = (255,0,0)
  
#   배경색 검,회,흰 순
  if font_bg_num == 1:
      bgcolor = (0,0,0,50)
  elif font_bg_num == 2:
      bgcolor = (128,128,128,50)
  elif font_bg_num == 3:
      bgcolor = (255,255,255,50)

  while True:
      ret,frame = cap1.read()
      if not ret: 
          break
      org=(0,h - 80)

      font = ImageFont.truetype(fontpath,32)
      text = file.readline()
      text_size =font.getsize(text)  
      if text_size[0] > w:
          text = text.split()
          n = len(text) //2
          text = text[:n] + ['\n'] + text[n:]
          text = ' '.join(text)

      
      y0, dy = (h - 80), text_size[1]

      for i, line in enumerate(text.split('\n')):
        y = y0 + i*dy
       
        if line :
            img = Image.fromarray(frame)
            draw = ImageDraw.Draw(img, 'RGBA')
            draw.rectangle((0,y,text_size[0],y+text_size[1]),fill=bgcolor)
            frame = np.array(img)
        img = Image.fromarray(frame)
        draw2 = ImageDraw.Draw(img)
        draw2.text((0, y),line,font = font,fill = fontcolor)
        frame = np.array(img)

          

      out.write(frame)


def combine_audio(video_pth, file_name):
    videoclip = mp.VideoFileClip(MEDIA_ROOT+"/"+"no_voice.mp4") # 자막이 들어간 동영상 위치
    audioclip = mp.AudioFileClip(video_pth) # 원본 동영상 위치

    videoclip = videoclip.set_audio(audioclip)  

    videoclip.write_videofile(MEDIA_ROOT+"/subtitle/"+file_name,codec='libx264',audio_codec='aac')