import numpy as np
import os
import cv2
import sys
import glob
import re

from config.settings import BASE_DIR

def shot_segmentation(video_path): # 요약할 비디오 파일 경로
    ouput_file = BASE_DIR +'\\dobby\\summ\\data\\'+'shot_segmentation.txt'
    command = 'ffprobe -show_frames -of compact=p=0 -f lavfi "movie=' + video_path + ',select=gt(scene\,.4)" > ' + ouput_file
    # command = 'ffprobe -show_frames -of compact=p=0 -f lavfi "movie='.\\Cosmus_Laundromat.mp4',select=gt(scene\,.4)" > C:\Users\User\test.txt'
    os.system(command)
    with open(ouput_file) as f: 
        content = f.readlines()
    shotIdx = [0]
    cap = cv2.VideoCapture(video_path)
    frames_per_second = int(cap.get(cv2.CAP_PROP_FPS))
    i = 0
    for line in content:
        shotIdx.append(np.int(np.round(float(line.split(sep="pts_time=")[1].split(sep="|pkt_dts")[0]) * frames_per_second)))
        i = i + 1
    # Impose a minimum (Lmin) and maximum (Lmax) shot length:
    Lmin = 25
    Lmax = 200
    total_num_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    C = np.subtract(np.append(shotIdx[1:], total_num_of_frames), shotIdx)
    # Consolidate a short shot with the following shot:
    C_without_short_shots = []
    for i in range(len(C) - 1):
        if C[i] >= Lmin:
            C_without_short_shots.append(C[i])
        else:
            C[i+1] = C[i+1] + C[i]
    if C[-1] >= Lmin:
        C_without_short_shots.append(C[-1])
    else:
        C_without_short_shots[-1] += C[-1]
    # Break long shot into smaller parts:
    final_C = []
    for i in range(len(C_without_short_shots)):
        if C_without_short_shots[i] <= Lmax:
            final_C.append(C_without_short_shots[i])
        else:
            devide_factor = np.int((C_without_short_shots[i] // Lmax) + 1)
            length_of_each_part = C_without_short_shots[i] // devide_factor
            for j in range(devide_factor - 1):
                final_C.append(length_of_each_part)
            final_C.append(C_without_short_shots[i] - (devide_factor - 1)*length_of_each_part)
    
    return np.save('./dobby/summ/data/shots_durations.npy', final_C)


def DeleteAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Remove all tmp files'
    else:
        return 'no dir'
        

def save_img(video_pth,txt_pth):
    # 이전 사용 파일 삭제
    DeleteAllFile('./dobby/summ/tmp/')
    
    cap = cv2.VideoCapture(video_pth)
    duration = np.load(txt_pth) 
    if not cap.isOpened() :
        sys.exit()
    cnt = 0
    while True:
        ret,frame = cap.read()
        if not ret: 
            break
        cv2.imwrite('./dobby/summ/tmp/{}.jpg'.format(cnt), frame) # 이미지가 여기서 저장됩니다!! 여기서 경로를 주면 됩니다!
        print('----------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',cnt)
        for i in range(duration[cnt]-1):
            ret,frame = cap.read()
            if not ret: 
                break

            cv2.imshow('frame',frame)

            if cv2.waitKey(1)== 27:
                break
        cnt += 1

def extract_features(image_dir_name):
    images = [cv2.imread(file) for file in sorted(glob.glob(os.path.join(image_dir_name, "*.jpg")), key=stringSplitByNumbers)]
    BINS_NUMBER_PER_CHANNEL = 32
    features = np.zeros((images.__len__(), BINS_NUMBER_PER_CHANNEL * 3), dtype=float)
    for i in range(len(images)):
        if i % 50 == 0:
            print("Finished extracting features for %d frames" %i)
        r_values = images[i][:,:,0].flatten()
        g_values= images[i][:, :, 1].flatten()
        b_values = images[i][:, :, 2].flatten()

        r_hist, _ = np.histogram(r_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_r_hist = r_hist / np.sum(r_hist)
        g_hist, _ = np.histogram(g_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_g_hist = g_hist / np.sum(g_hist)
        b_hist, _ = np.histogram(b_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_b_hist = b_hist / np.sum(b_hist)

        features[i,:] = np.concatenate((normalized_r_hist, normalized_g_hist, normalized_b_hist))
    print(features.shape,"-----------------")
    return np.save('./dobby/summ/data/shots_features.npy', features)

def stringSplitByNumbers(x):
    r = re.compile('(\d+)')
    l = r.split(x)
    return [int(y) if y.isdigit() else y for y in l]


################################## 실행되는 코드 #####################################

# video_path = # 요약할 영상 경로
# txt_pth = # shot_duration.npy가 저장된 경로
# image_dir_name = # 썸네일 이미지가 저장된 경로

# shot_segmentation(video_path) # shot_duration.npy저장하는 함수 -> return 에 저장될 경로 같이 주시면 됩니다!
# save_img(video_path,txt_pth) # 이미지 저장하는 함수 # 나중에 썸네일 이미지를 여기서 추출합니다 
# extract_features(image_dir_name) #최종적으로 feature를 추출하는 함수! 위에서 저장된 이미지 경로를 주시면 됩니다!


