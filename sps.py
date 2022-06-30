import cv2
import mediapipe as mp
import math
import time

timer = 3


def get_coords(landmarks):
    h, w, c = img.shape
    coords = []
    points = [0, 8, 12, 16, 20, 5, 9, 13, 17]
    for i in points:
        point = landmarks[i]
        cx, cy, cz = int(point.x * w), int(point.y * h), abs(int(point.z * w))
        coords.append([cx, cy, cz])
    return coords


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


# alle functies voor schaar
def get_schaar_coords(landmarks):
    h, w, c = img.shape
    schaar_coords = []
    points = [0, 5, 9, 13, 17, 8, 12, 16, 20]
    for i in points:
        point = landmarks[i]
        cx, cy, cz = int(point.x * w), int(point.y * h), abs(int(point.z * w))
        schaar_coords.append([cx, cy, cz])
    return schaar_coords


def afstand_tussen_punten(punt1, punt2):
    x, y, z = punt1[0], punt1[1], punt1[2]
    x2, y2, z2 = punt2[0], punt2[1], punt2[2]
    afstand_punt = math.sqrt(((x - x2)**2) + ((y - y2)**2) + ((z - z2)**2))

    return abs(afstand_punt)


def check_schaar(coords):
    afstanden = []
    for i in range(1, 5):
        afstand = afstand_tussen_punten(coords[i], coords[i + 4])
        afstanden.append(afstand)

    coef = 0.6
    if afstanden[2] < coef * afstanden[0] and afstanden[3] < coef * afstanden[0] \
            and afstanden[2] < coef * afstanden[1] and afstanden[3] < coef * afstanden[1]:
        cv2.putText(img, "Schaar", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        return True
    else:
        return False

# checken voor papier


def check_vingers(coords):
    vingers = []
    for i in range(1, 5):
        up = top_knok(coords[i], coords[i + 4], coords[0])
        vingers.append(up)
    return vingers

# Checken voor steen


def get_steen_coords(landmarks):
    h, w, c = img.shape
    steen_coords = []
    points = [0, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20]
    for i in points:
        point = landmarks[i]
        cx, cy, cz = int(point.x * w), int(point.y * h), abs(int(point.z * w))
        steen_coords.append([cx, cy, cz])
    return steen_coords


def check_steen(coords):
    afstanden = []
    cluster = []
    for i in [1, 4, 7, 10]:
        temp = []
        afstand1 = afstand_tussen_punten(coords[i], coords[0])
        afstand2 = afstand_tussen_punten(coords[i + 1], coords[0])
        afstand3 = afstand_tussen_punten(coords[i + 2], coords[0])
        temp.append(afstand1)
        temp.append(afstand2)
        temp.append(afstand3)
        klein = min(temp)
        groot = max(temp)
        afstanden.append(groot)
        afstanden.append(klein)

    for i in range(0, 8, 2):
        verschil = afstanden[i] - afstanden[i + 1]
        if verschil < 0.3 * afstand_tussen_punten(coords[0], coords[1]):
            cluster.append(True)
        else:
            cluster.append(False)

    if all(cluster) == True:
        cv2.putText(img, 'Steen', (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        return True
    else:
        return False


def check_move(move):
    result = ''
    if move[0] == True and move[1] == True and move[2] == False and move[3] == False:
        result = 'schaar'
    elif all(move) == True:
        result = 'papier'
    elif move[0] == False and move[1] == False and move[2] == False and move[3] == False:
        result = 'steen'
    else:
        result = 'ongeldig'
    cv2.putText(img, result, (10, 70),
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
        prev = time.time()

        while timer > 0:
            succes, img = cap.read()
            img = cv2.flip(img, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(timer),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            cv2.imshow('image', img)
            cv2.waitKey(125)
            cur = time.time()
            if cur-prev >= 1:
                prev = cur
                timer = timer-1

        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                landmarks = handlms.landmark
                coords = get_coords(landmarks)
                schaar_coords = get_schaar_coords(landmarks)
                steen_coords = get_steen_coords(landmarks)
                schaar = check_schaar(schaar_coords)
                if schaar == False:
                    steen = check_steen(steen_coords)
                    if steen == False:
                        move = check_vingers(coords)
                        check_move(move)

                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("image", img)

    cv2.destroyAllWindows()
