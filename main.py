import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from brain import ask_brite
from voice import speak

import urllib.request
import os

# download the face detection model if you dont have it
model_path = 'blaze_face_short_range.tflite'
if not os.path.exists(model_path):
    print("downloading face detection model...")
    urllib.request.urlretrieve(
        'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite',
        model_path
    )
    print("done")

# set up the detector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

cap = cv2.VideoCapture(0)

face = True
while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("error: failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)

    # convert frame to mediapipe image format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # run detection
    results = detector.detect(mp_image)

    face_detected = len(results.detections) > 0

    if face_detected and not face:
        response = ask_brite("A person just looked at me for the first time!")
        speak(response["speech"])        
    elif not face_detected and face:
        print("face just left")

    face = face_detected

    if face_detected:
        color = (0, 255, 0)
        message = "FACE DETECTED"
    else:
        color = (0, 0, 255)
        message = "NO FACE"

    cv2.circle(frame, (30, 30), 15, color, -1)
    cv2.putText(frame, message, (55, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('webcam live feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()