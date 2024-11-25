import cv2
import math

def is_in_zone(position, zone_centers = [[20,25],[250, 540], [500,300],[90, 400]], zone_rad = [25, 45, 90, 100]):

    for index, zone in enumerate(zone_centers):

        if math.dist(position, zone) < zone_rad[index]:

            print("I'm in zone", index, "!")

# Create a SimpleBlobDetector parameters object
params = cv2.SimpleBlobDetector_Params()

# Modify the parameters as needed
params.minThreshold = 10
params.maxThreshold = 50
params.filterByArea = True
params.minArea = 10
params.filterByColor = True
params.blobColor = 255
params.minDistBetweenBlobs = 80
params.filterByCircularity = False
params.filterByInertia = False
params.filterByConvexity = False


# Create a SimpleBlobDetector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


# Open a video capture object
cap = cv2.VideoCapture('/home/metalab_legion/Videos/blobtracking_demo/Bruno_with_light.mp4')  # Replace 'your_video_file.avi' with your video file path

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()


#initialize keypoints
keypoints = ([[]])

has_background_img = False


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if has_background_img:

        temp_background_img = frame
        frame = cv2.subtract(frame, background_img)
        background_img = temp_background_img

    if not has_background_img:

        background_img = frame  
        has_background_img = True 

    
   
    keypoints = detector.detect(frame)

    for keypoint in keypoints:
        is_in_zone(keypoint.pt)

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

    cv2.waitKey(33)
# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
