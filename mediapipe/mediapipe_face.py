import mediapipe as mp 
import cv2

mp_face = mp.solutions.face_detection

mp_draw = mp.solutions.drawing_utils


def detection_context(dev_id=0):

    cap = cv2.VideoCapture(dev_id)
    with mp_face.FaceDetection() as faces:
        while cap.isOpened():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = faces.process(image)

            if results.detections:

                for i, detection in enumerate(results.detections):
                    mp_draw.draw_detection(image, detection)
                #mp_draw.draw_landmarks(image, results.detections, mp_pose.POSE_CONNECTIONS)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.flip(image, 1)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    detection_context()
