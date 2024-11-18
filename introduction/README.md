Une fois que le dépôt Git est cloné sur vos machines, je vous invite à tester les scripts dans le sous-dossier introduction.

Il faudra premièrement s'assurer d'installer les dépendances:
` pip install mediapipe ultralytics opencv-python `

Les scripts dans le dossier sont les suivants: 

* camera_opencv.py : pour valider la détection de webcam dans python
* test_yolo.py: pour voir comment les différents modèles d'IA en vision par ordinateur fonctionnent
* mediapipe_pose.py: pour tester un modèle de détection de squelettes

Pour aller plus loin dans l'exploration des scripts de base: 

*[Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8/) : pour tester différentes modalités de détection dans le script test_yolo.py
*[MediaPipe Solutions guide](https://ai.google.dev/edge/mediapipe/solutions/guide): pour voir quelles modalités de détection sont disponible dans l'architecture mediapipe
