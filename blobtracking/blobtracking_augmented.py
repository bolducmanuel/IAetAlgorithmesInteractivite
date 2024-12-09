import cv2
import math

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

nice_notes = {
    -1 : 0,
    0 : 130.813,
    1 : 164.814,
    2 : 195.998,
    3: 246.942
}

def is_in_zone(keypoints, zone_centers = [[250,250],[500, 250], [500,500],[250, 500]], zone_rad = [50, 50, 50, 50]):

    detected_zone = -1
    
    for keypoint in keypoints:

        position = keypoint.pt

        for index in range(len(zone_rad)):

            if math.dist(position, zone_centers[index]) < zone_rad[index]:

                detected_zone = index
                break
    
        if detected_zone != -1:
            break

    # for range purposes
    detected_zone = (detected_zone + 1.0)/4.0

    return detected_zone 

def proximity_calc(keypoints, distance_prev):

    distance = 0. 

    for keypoint1 in keypoints:

        position1 = keypoint1.pt

        for keypoint2 in keypoints: 

            position2 = keypoint2.pt

            distance += math.dist(position1, position2)

    distance_prev = distance_prev[-1:] + distance_prev[:-1]

    distance_prev[0] = distance

    distance_smooth = math.fsum(distance_prev)/len(distance_prev)

    return distance_smooth, distance_prev







# Create a SimpleBlobDetector parameters object
params = cv2.SimpleBlobDetector_Params()

# Modify the parameters as needed
params.minThreshold = 10
params.maxThreshold = 100
params.filterByArea = True
params.minArea = 5
params.filterByColor = True
params.blobColor = 255
params.minDistBetweenBlobs = 20
params.filterByCircularity = False
params.filterByInertia = False
params.filterByConvexity = False


# Create a SimpleBlobDetector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

def detection_context():
    # Open a video capture object
    cap = cv2.VideoCapture('/home/metalab_legion/Videos/blobtracking_demo/circle_uncompressed.mp4')  # Replace 'your_video_file.avi' with your video file path

    if not cap.isOpened():
        print("Error: Could not open video file")
        exit()


    #initialize keypoints
    keypoints = ([[]])

    has_background_img = False

    frame_count = 0

    # to change the smoothing behavior of the function proximity_calc, add 0s to the list!
    distance_prev = [0]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        

        ## SOUSTRACTION DYNAMIQUE ##
        # if has_background_img:

        #     temp_background_img = frame
        #     frame = cv2.subtract(frame, background_img)
        #     background_img = temp_background_img

        # if not has_background_img:

        #     background_img = frame  
        #     has_background_img = True 

        ## SOUSTRACTION INITIALE ##
        if frame_count == 0:
            background_image = frame
            frame_count += 1

        frame = cv2.subtract(frame, background_image)
    
        keypoints = detector.detect(frame)

        #detected_zone function call
        #detected_zone = is_in_zone(keypoints)
        #print(zone)

        #total distance function call

        total_dist, distance_prev = proximity_calc(keypoints, distance_prev)

        osc_process()
        osc_msg = oscbuildparse.OSCMessage("/zone", None, [total_dist] )
        osc_send(osc_msg, "localhost")


        

        # Draw the keypoints on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, outImage=None, color=(0, 0, 255),
                                                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for id, keypoint in enumerate(keypoints):
            cv2.putText(
                frame_with_keypoints,
                str(id),
                (int(keypoint.pt[0]), int(keypoint.pt[1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                5,
                cv2.LINE_AA
            )


        # Display the frame with keypoints
        #cv2.imshow('Frame with Keypoints', frame_with_keypoints)
        cv2.imshow('frame', frame_with_keypoints)

        #cv2.imshow('frame with background removed', mask)
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.waitKey(25)
    # Release the video capture object and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    osc_terminate()

if __name__ == '__main__':

    osc_startup()
    osc_udp_client("127.0.0.1", 9000, "localhost")
    detection_context()
