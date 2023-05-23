import cv2
import numpy as np

import HandTracking as ht
import math

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = ht.HandDetector()

prev_len, ratio = 0, 0

while cap.read()[0]:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList =  detector.find_position(img,draw=False)
    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

        cur_len = math.hypot(x2-x1,y2-y1)
        if prev_len: ratio = cur_len/prev_len
        prev_len = cur_len

        min_vol, max_vol = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]

        # if ratio and ratio>1.2:
        #     new_vol = volume.GetMasterVolumeLevel() + ((max_vol - min_vol) * ratio)
        #     if new_vol>max_vol: new_vol=max_vol
        #     volume.SetMasterVolumeLevel(new_vol,None)
        # elif ratio and ratio<0.8:
        #     new_vol = volume.GetMasterVolumeLevel() - ((max_vol - min_vol) * ratio)
        #     if new_vol < min_vol: new_vol = min_vol
        #     volume.SetMasterVolumeLevel(new_vol,None)

        vol = np.interp(cur_len, [50,300], [min_vol,max_vol])
        volume.SetMasterVolumeLevel(vol, None)

        # print(volume.SetMasterVolumeLevel(-20.0, None))
    # cv2.imshow('VolumeControl', img)
    cv2.waitKey(1)