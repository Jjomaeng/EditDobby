import datetime
from glob import glob
import json

import os

from django.shortcuts import redirect, render
from django.http import HttpResponse
import urllib.parse

from matplotlib.image import thumbnail
from config import settings
from config.settings import BASE_DIR, MEDIA_ROOT
from dobby.fu_filter import combine_audio2, filter_srt, total_filter
from dobby.subtitle import combine_audio, subtitle_fps, subtitle_generator
from dobby.summ.demo import demo, demo_title
from dobby.summ.feature_extract import extract_features, save_img, shot_segmentation
from dobby.summ.thumbnail_rcmmnd import rcmd_th
from dobby.imgcap.img_cap import rcmmnd_title, translate_text

from main.models import Member
from .models import File

# Create your views here.
def edit(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    if request.method == "POST":
        upload_file = request.FILES.get('e_file')
        name = upload_file.name 
        request.session['file_name'] = name
        with open(MEDIA_ROOT+'/'+name, 'wb') as file: 
            for chunk in upload_file.chunks():
                file.write(chunk)

    else:
        return render(request, "dobby/edit.html")
    
    # return render(request, "dobby/fun.html", {"upload_file": upload_file})
    return redirect("/dobby/fun/")


def result(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    

    return render(request, 'dobby/result.html')



def download(request):

    # 다운로드 문제 - db에서 경로로 비교하여 파일탐색 따라서 같은파일이 2번 들어오면 오류 발생
    #              - 같은파일이 존재할 시 구분해서 저장할 필요 있음
    if request.method == 'POST':
        fn = request.POST["filename"]
        filename = File.objects.get(file_root = fn)
        filepath = str(settings.BASE_DIR) + ('%s' % filename.file_root)
        fn = urllib.parse.quote(fn.encode('utf-8'))
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % fn
    return response




def fun(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")

    global fontnum
    global font_col_num
    global font_bg_num
    # return render(request,"dobby/fun.html")
    if request.method == "GET":
      
        return render(request,"dobby/fun.html")
        
    elif 'create' in request.POST:
        txt_pth = MEDIA_ROOT + "\\"+ "subtitle.txt"
        video_pth = MEDIA_ROOT + "\\" + request.session['file_name']
    
        font =  request.POST['font']
        if font == "font1":
            fontnum = 1

        elif font == "font2":
            fontnum = 2

        elif font == "font3":
            fontnum = 3

        fontcolor =  request.POST['fontcolor']
        if fontcolor == "font-color1":
            font_col_num = 1

        elif fontcolor == "font-color2":
            font_col_num = 2

        elif fontcolor == "font-color3":
            font_col_num = 3


        font_bg_num = 0
        bgcolor =  request.POST['bgcolor']
        if bgcolor == "bg-color1":
            font_bg_num = 1

        elif bgcolor == "bg-color2":
            font_bg_num = 2

        elif bgcolor == "bg-color3":
            font_bg_num = 3
        
        subtitle_fps(txt_pth,video_pth)
        subtitle_generator(txt_pth,video_pth,fontnum,font_col_num,font_bg_num)
        combine_audio(video_pth, request.session['file_name'])
        
        
        file_path = str(settings.BASE_DIR) + ('/media/%s' % request.session['file_name'])
        rmv1 = str(settings.BASE_DIR) + ('/media/%s' % 'no_voice.mp4')
        rmv2 = str(settings.BASE_DIR) + ('/media/%s' % 'subtitle.txt')
        os.remove(file_path)
        os.remove(rmv1)
        os.remove(rmv2)
        
        now = datetime.datetime.now()
        
        file = File(
            file_name = request.session['file_name'],
            member_id = Member.objects.get(member_id=request.session.get('s_id')),
            file_root = "\\media\\subtitle\\" + request.session['file_name'],
            file_date = now,
        )
        file.save()
        context={
            'file':file
        }
    
    elif 'filter' in request.POST:
        txt_pth = MEDIA_ROOT + "\\"+ "result.txt"  # 필터링 음성추출파일 
        video_pth = MEDIA_ROOT + "\\" + request.session['file_name']
 
        
        filter_srt(txt_pth,video_pth)
        total_filter(txt_pth,video_pth)
        
        audio_pth =  MEDIA_ROOT + "\\" + "filter_audio.mp3"
        combine_audio2(audio_pth,video_pth,request.session['file_name'])
        
        now = datetime.datetime.now()
        
        file = File(
            file_name = request.session['file_name'],
            member_id = Member.objects.get(member_id=request.session.get('s_id')),
            file_root = "\\media\\filter\\" + request.session['file_name'],
            file_date = now,
        )
        file.save()
        context={
            'file':file
        }
    
    elif 'shorts' in request.POST: 
        video_name = request.session['file_name']
        video_root = "\\media\\summary\\" + request.session['file_name']
        duration = "./dobby/summ/data/"+"shots_durations.npy"
        rate = request.POST.get("ratio")
        
        tmp = "./media/"+video_name
        img_dir = "./dobby/summ/tmp/"
        
        # 테스트코드
        # video_name = "20220504_120048.mp4"
        # video_root = "\\media\\summary\\" + "20220504_120048.mp4"
        # duration = "./dobby/summ/data/"+"shots_durations.npy"
        # rate = request.POST.get("ratio")
        
        # tmp = "./media/"+video_name
        # img_dir = "./dobby/summ/tmp/"
        
        
        # 20220504_120048.mp4
        
        
        shot_segmentation(tmp)
        save_img(tmp, duration)
        extract_features(img_dir)
        
        
        print(rate)
        demo(video_name, rate)
        
        now = datetime.datetime.now()
        
        file = File(
            file_name = request.session['file_name'],
            member_id = Member.objects.get(member_id=request.session.get('s_id')),
            file_root = "\\media\\summary\\" + request.session['file_name'],
            file_date = now,
        )
        file.save()
        context={
            'file':file
        }
        
    
    elif 'title' in request.POST:
        video_name = request.session['file_name']
        duration = "./dobby/summ/data/"+"shots_durations.npy"
        
        tmp = "./media/"+video_name
        img_dir = BASE_DIR + "\\dobby\\summ\\tmp\\"
        
        shot_segmentation(tmp)
        save_img(tmp, duration)
        extract_features(img_dir)
        
        representative_points = demo_title(video_name, 0.5)
        imgs = rcmd_th(representative_points, img_dir)
        
        
        context={
            'imgs':imgs
        }
        
        # return render(request, 'dobby/result_thumb_title.html', context)
        return redirect("/dobby/result_thumb/")

    
    
    
    

    return render(request, 'dobby/result.html', context)



def result_thumb(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    if request.method == 'POST':
        img_path = request.POST['thumbnail']
        img='.'+img_path[21:]
        img_file = img_path
        print('******'+img)
        
        
        
        
        key_list =translate_text(rcmmnd_title(img))
        context={
            'img':img,
            'key_list':key_list,
            'img_file':img_file
        }
        return render(request,'dobby/title_select.html', context)
    
    
    
    img_files = []
    k=0
    for file in sorted(glob(MEDIA_ROOT + "\\thumbnail\\"+ "*.jpg")):
        img_files.append(file)
        print(img_files[k])
        print(k,'###$#$#$$')
        k=k+1
        
    context={
        'imgs':img_files,
    }
    
    contJson = json.dumps(context)

    return render(request, 'dobby/result_thumb_title.html', {'contJson':contJson})


def title_select(request):
    
    return render(request, 'dobby/title_select.html')
   