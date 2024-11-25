import cv2

# Create a SimpleBlobDetector parameters object
params = cv2.SimpleBlobDetector_Params()

# Modify the parameters as needed
params.minThreshold = 10
params.maxThreshold = 50
params.filterByArea = True
params.minArea = 60
params.filterByColor = True
params.blobColor = 255
params.minDistBetweenBlobs = 80
params.filterByCircularity = False
params.filterByInertia = False
params.filterByConvexity = False


# Create a SimpleBlobDetector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


# Open a video capture object
cap = cv2.VideoCapture('/home/metalab_legion/Videos/blobtracking_demo/30fps_Bruno_with_light.avi')  # Replace 'your_video_file.avi' with your video file path

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()


#initialize keypoints
keypoints = ([[]])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
   
    keypoints = detector.detect(frame)

    # Draw the keypoints on the frame
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, outImage=None, color=(0, 0, 255),
                                             flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



    cv2.imshow('frame', frame_with_keypoints)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
