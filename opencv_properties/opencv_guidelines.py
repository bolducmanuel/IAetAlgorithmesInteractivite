import cv2


## pour ouvrir une caméra
cap = cv2.VideoCapture(0) #normalement, la webcam

#cap = cv2.VideoCapture(1) # une deuxième caméra USB connectée à l'ordi

cap = cv2.VideoCapture('/home/metalab_legion/Videos/blobtracking_demo/test_video.mp4')


## algorithmes pour la soustraction d'arrière-plans dynamique
backSub1 = cv2.createBackgroundSubtractorMOG2()
backSub2 = cv2.createBackgroundSubtractorKNN()

while cap.isOpened():

    success, frame = cap.read()

    if not success: 
        print("ignoring empty camera frame.")

        continue


    ## RESIZE ##

    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # frame = cv2.resize(frame, (int(0.5*width), int(0.5*height)))

   
    ## METHODE DE SOUSTRACTION D'ARRIERE PLAN no. 1 ##
    
    # if has_background_img:

    #     temp_background_img = frame
    #     frame = cv2.subtract(frame, background_img)
    #     background_img = temp_background_img

    # if not has_background_img:

    #     background_img = frame  
    #     has_background_img = True 

    ## METHODE DE SOUSTRACTION D'ARRIERE PLAN à l'aide d'algorithmes##

    # fgmask1 = backSub1.apply(frame)
    # fgmask2 = backSub2.apply(frame)




    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

    #cv2.waitKey(30) #pour rajouter un délai sur l'exécution de la boucle while

cap.release()
cv2.destroyAllWindows()

