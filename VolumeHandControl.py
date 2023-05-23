import cv2
import numpy as np
import HandTracking as ht
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    def get_minimum_volume(self):
        return self.volume.GetVolumeRange()[0]

    def get_maximum_volume(self):
        return self.volume.GetVolumeRange()[1]

    def set_volume(self, vol):
        self.volume.SetMasterVolumeLevel(vol, None)


def main():
    width, height = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    detector = ht.HandDetector()
    controller = VolumeControl()

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

            min_vol, max_vol = controller.get_minimum_volume(), controller.get_maximum_volume()

            vol = np.interp(cur_len, [50,300], [min_vol,max_vol])
            controller.set_volume(vol)
        cv2.imshow('VolumeControl', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()