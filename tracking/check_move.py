import cv2
import mediapipe as mp
import math


def get_coords(landmarks, img):
    h, w, c = img.shape
    coords = []
    points = [0, 8, 12, 16, 20, 5, 9, 13, 17]
    for i in points:
        point = landmarks[i]
        cx, cy, cz = int(point.x * w), int(point.y * h), abs(int(point.z * w))
        coords.append([cx, cy, cz])
    return coords


def get_schaar_coords(landmarks):
    h, w, c = img.shape
    schaar_coords = []
    points = [0, 6, 10, 14, 18, 5, 9, 13, 17]
    for i in points:
        point = landmarks[i]
        cx, cy, cz = int(point.x * w), int(point.y * h), abs(int(point.z * w))
        schaar_coords.append([cx, cy, cz])
    return schaar_coords


def top_knok(top, knok, palm):
    x, y, z = top[0], top[1], top[2]
    x2, y2, z2 = knok[0], knok[1], knok[2]
    a, b, c = palm[0], palm[1], palm[2]
    afstand_top_palm = math.sqrt(((x - a)**2) + ((y - b)**2) + ((z - c)**2))
    afstand_knok_palm = math.sqrt(
        ((x2 - a)**2) + ((y2 - b)**2) + ((z2 - c)**2))
    if afstand_top_palm > afstand_knok_palm:
        return True
    else:
        return False


def afstand_tussen_punten(punt1, punt2):
    x, y, z = punt1[0], punt1[1], punt1[2]
    x2, y2, z2 = punt2[0], punt2[1], punt2[2]
    afstand_punt = math.sqrt(((x - x2)**2) + ((y - y2)**2) + ((z - z2)**2))

    return abs(afstand_punt)


def check_schaar(coords, img):
    afstanden = []
    for i in range(1, 5):
        afstand = top_knok(coords[i], coords[i + 4], coords[0])
        afstanden.append(afstand)

    coef = 0.4
    if afstanden[2] < coef * afstanden[0] and afstanden[3] < coef * afstanden[0] \
            and afstanden[2] < coef * afstanden[1] and afstanden[3] < coef * afstanden[1]:
        cv2.putText(img, "Schaar", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        return 1
    else:
        return 0


def check_vingers(coords):
    vingers = []
    for i in range(1, 5):
        up = top_knok(coords[i], coords[i + 4], coords[0])
        vingers.append(up)
    return vingers


def check_move(move, img):
    if move[0] == True and move[1] == True and move[2] == False and move[3] == False:
        print('schaar')
        cv2.putText(img, "schaar", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    elif all(move) == True:
        cv2.putText(img, "papier", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    elif all(move) == False:
        cv2.putText(img, "steen", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    else:
        cv2.putText(img, "ongeldig", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    current_time = 0
    past_time = 0
    while True:
        succes, img = cap.read()
        img = cv2.flip(img, 1)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                landmarks = handlms.landmark
                points = get_coords(landmarks)
                val = check_schaar(points, img)
                if val == 0:
                    move = check_vingers(points)
                    check_move(move, img)

                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("image", img)

    cv2.destroyAllWindows()
