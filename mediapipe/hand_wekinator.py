import mediapipe as mp
import cv2
import math

from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

mp_hands = mp.solutions.hands

mp_draw = mp.solutions.drawing_utils

def list_keypoints(landmarks):

    keypoint_list = []
    wrist = landmarks[0]

    for landmark in landmarks: 

        keypoint_list.append(math.fabs(landmark.x - wrist.x))
        keypoint_list.append(math.fabs(landmark.y - wrist.y))


    print(keypoint_list)

    return keypoint_list

def detection_context(dev_id = 0):

    cap = cv2.VideoCapture(dev_id)
    with mp_hands.Hands(max_num_hands = 1) as hands:
        while cap.isOpened():

            success, image = cap.read()

            if not success: 

                print("Ignoring empty camera frame")

                continue

            # To imporve performance, can mark the image as not writeable to pass by reference
            image.flags.writeable = False

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = hands.process(image)

            image.flags.writeable = True

            if results.multi_hand_landmarks:

                hand_index = 0

                for hand_landmarks in results.multi_hand_landmarks:

                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    keypoint_list = list_keypoints(hand_landmarks.landmark)

                    osc_process()
                    osc_msg = oscbuildparse.OSCMessage("/wek/inputs", None, keypoint_list)
                    osc_send(osc_msg, "localhost")

                    hand_index += 1

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.flip(image, 1)
            cv2.imshow('frame', image)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        osc_terminate()

if __name__ == '__main__':

    osc_startup()
    osc_udp_client("127.0.0.1", 9000, "localhost")
    detection_context()