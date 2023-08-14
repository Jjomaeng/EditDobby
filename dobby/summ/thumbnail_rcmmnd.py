import glob
import os
import cv2
import re

from config.settings import MEDIA_ROOT



def rcmd_th(representative_points,img_pth):
    print(representative_points)
    # img_files = [cv2.imread(file) for file in sorted(glob.glob(img_pth), key=stringSplitByNumbers)]
    img_files = []
    k = 0
    for file in sorted(glob.glob(img_pth+'*.jpg'), key=stringSplitByNumbers):
        img_files.append(cv2.imread(file))
        print(k,' image')
        k = k+1 
    

    print(len(img_files))
    DeleteAllFile(MEDIA_ROOT + "\\thumbnail\\")
    for i in representative_points :
        img = img_files[i]
        
        if img is None :
            print("Image load failed")
            break
        # cv2.imshow('img',img)
        # cv2.waitKey()
        cv2.imwrite(MEDIA_ROOT + "\\thumbnail\\" + "{}.jpg".format(i), img) # 이미지 저장
    return img_files


def stringSplitByNumbers(x):
    r = re.compile('(\d+)')
    l = r.split(x)
    return [int(y) if y.isdigit() else y for y in l]


def DeleteAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Remove all tmp files'
    else:
        return 'no dir'


######



######

# img_pth = ".//img//*.jpg" # 썸네일 이미지가 저장된 위치
# representative_points =  [ 37, 104, 311, 321] # demo.py 파일 돌렸을 때 출력되는 선택된 shot

# rcmd_th(representative_points,img_pth)