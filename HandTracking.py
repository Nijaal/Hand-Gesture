import cv2
import mediapipe as mp
import time


class HandDetector:

    def __init__(self, mode =False, max_hands =2, detection_con =0.5, track_con =0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.max_hands, model_complexity=1,
                                         min_detection_confidence=self.detection_con,
                                         min_tracking_confidence=self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        # image processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # hand detection and tracking
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw: self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, handNo=0, draw=True):
        lmList = []
        # image processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # image shape
        h, w, c = img.shape

        # hand detection and tracking
        if self.results.multi_hand_landmarks and handNo < len(self.results.multi_hand_landmarks):
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw: cv2.circle(img, (cx, cy), 10, (0,255,00), cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture(0)

    detector = HandDetector()
    prev_time = cur_time = 0
    while cap.read()[0]:
        success, img = cap.read()
        img = detector.find_hands(img)
        # detector.find_position(img)

        # fps
        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time
        cv2.putText(img, str(int(fps)), (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
