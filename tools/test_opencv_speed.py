import cv2
import numpy as np
import urllib.request
import time
import json

detector = cv2.FaceDetectorYN.create('models/face_detection_yunet_2023mar.onnx', '', (320, 320), 0.5, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create('models/face_recognition_sface_2021dec.onnx', '')

with open('event_photos_database.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

print(f"Testing on first 5 photos...")
start_time = time.time()

for i, p in enumerate(photos[:5]):
    t0 = time.time()
    req = urllib.request.Request(p['thumbnail'], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        img_bytes = np.frombuffer(resp.read(), dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)
    
    n_faces = len(faces) if faces is not None else 0
    descriptors = []
    if faces is not None:
        for face in faces:
            aligned_face = recognizer.alignCrop(img, face)
            feat = recognizer.feature(aligned_face)
            descriptors.append(feat.flatten().tolist())
            
    print(f"[{i+1}/5] {p['filename']} ({w}x{h}): {n_faces} faces, took {round(time.time() - t0, 2)}s")

print(f"Total time for 5 photos: {round(time.time() - start_time, 2)}s")
