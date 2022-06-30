"""hand checking
"""

import cv2
import mediapipe as mp
import time
import math


cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(max_num_hands=1)
mpdraw = mp.solutions.drawing_utils

current_time = 0
past_time = 0

max_distance = 100
# get distance between two points


def get_distance(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))


def finger_closed(ids):
    if ids + 1 not in loc_per_id:
        return False
    return get_distance(*loc_per_id[ids], *loc_per_id[ids+1]) < 80


while True:
    loc_per_id = {}
    succes, img = cap.read()

    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)

    if results.multi_hand_landmarks:
        loc_per_id = {}
        for handlms in results.multi_hand_landmarks:
            for idx, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                loc_per_id[idx] = [cx, cy]
                if idx % 4 == 0 and idx != 0 and idx != 20:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
            mpdraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)

    current_time = time.time()
    fps = 1 / (current_time - past_time)
    past_time = current_time

    closed = [finger_closed(id) for id in range(4, 20, 4)]
    if closed.count(True) == 4:
        cv2.putText(img, "Steen", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    elif closed.count(True) <= 1:
        cv2.putText(img, "Papier", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        # if 5 in loc_per_id and 8 in loc_per_id:
        #     max_distance = get_distance(*loc_per_id[5], *loc_per_id[8])/2
    elif closed.count(True) == 2:
        cv2.putText(img, "Schaar", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow("image", img)

img.release()

cv2.destroyAllWindows()
