import os
import cv2
import numpy as np
import json
import time

detector = cv2.FaceDetectorYN.create('models/face_detection_yunet_2023mar.onnx', '', (320, 320), 0.4, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create('models/face_recognition_sface_2021dec.onnx', '')

with open('event_photos_database.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

print(f"Indexing face vectors for {len(photos)} photos...")

indexed_photos = []
total_faces = 0

for i, p in enumerate(photos):
    thumb_path = os.path.join("thumbnails", f"{p['id']}.jpg")
    photo_entry = dict(p)
    photo_entry['descriptors'] = []
    
    if os.path.exists(thumb_path):
        img = cv2.imread(thumb_path)
        if img is not None:
            h, w = img.shape[:2]
            detector.setInputSize((w, h))
            _, faces = detector.detect(img)
            
            if faces is not None:
                for face in faces:
                    aligned = recognizer.alignCrop(img, face)
                    feat = recognizer.feature(aligned)
                    # Round float32 to 4 decimal places to keep JSON size reasonable
                    vec = [round(float(v), 4) for v in feat.flatten()]
                    photo_entry['descriptors'].append(vec)
                    total_faces += 1
                    
    indexed_photos.append(photo_entry)

print(f"✅ Finished indexing! Total faces detected: {total_faces} across {len(indexed_photos)} photos.")

database = {
    "event_info": {
        "title": "LỄ TUYÊN DƯƠNG NHÀ GIÁO TIÊU BIỂU 2026",
        "organization": "Trường Đại học Kinh Tế",
        "total_photos": len(indexed_photos),
        "total_faces_indexed": total_faces,
        "model": "OpenCV-SFace-128d",
        "last_updated": "2026-11-20"
    },
    "photos": indexed_photos
}

with open("database.json", "w", encoding="utf-8") as f:
    json.dump(database, f, ensure_ascii=False)

print("💾 Saved complete vector database to database.json!")
