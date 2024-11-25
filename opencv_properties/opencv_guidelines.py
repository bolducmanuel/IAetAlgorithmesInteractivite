import cv2


## pour ouvrir une caméra
cap = cv2.VideoCapture(0) #normalement, la webcam

#cap = cv2.VideoCapture(1) # une deuxième caméra USB connectée à l'ordi

cap = cv2.VideoCapture('/home/metalab_legion/Videos/blobtracking_demo/30fps_Bruno_with_light.avi')



while cap.isOpened():

    success, frame = cap.read()

    if not success: 
        print("ignoring empty camera frame.")

        continue

    ## METHODE DE SOUSTRACTION D'ARRIERE PLAN ##
    
    # if has_background_img:

    #     temp_background_img = frame
    #     frame = cv2.subtract(frame, background_img)
    #     background_img = temp_background_img

    # if not has_background_img:

    #     background_img = frame  
    #     has_background_img = True 

    ## METHODE DE SOUSTRACTION D'ARRIERE PLAN ##


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

    #cv2.waitKey(33) pour rajouter un délai sur l'exécution de la boucle while

cap.release()
cv2.destroyAllWindows()

