import os
import cv2
import numpy as np
import json
import time

detector = cv2.FaceDetectorYN.create('models/face_detection_yunet_2023mar.onnx', '', (320, 320), 0.4, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create('models/face_recognition_sface_2021dec.onnx', '')

with open('event_photos_database.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

# Find target query face from Desktop
q_path = r'c:\Users\ADMIN\Desktop\1795170991205_2276516459885095864_2138731840136663169_f4193a5c54cdc2270bd87a9353ce03fa.jpg'
q_img = cv2.imdecode(np.fromfile(q_path, dtype=np.uint8), cv2.IMREAD_COLOR)

detector.setInputSize((q_img.shape[1], q_img.shape[0]))
_, q_faces = detector.detect(q_img)
q_aligned = recognizer.alignCrop(q_img, q_faces[0])
target_feat = recognizer.feature(q_aligned)

print("🎯 Target face vector loaded for Cô Đinh Thị Ngọc!")

matches = []
processed = 0

for p in photos:
    thumb_path = os.path.join("thumbnails", f"{p['id']}.jpg")
    if not os.path.exists(thumb_path):
        continue
        
    img = cv2.imread(thumb_path)
    if img is None:
        continue
        
    processed += 1
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)
    
    if faces is not None:
        max_score = 0
        for face in faces:
            aligned = recognizer.alignCrop(img, face)
            feat = recognizer.feature(aligned)
            score = float(recognizer.match(target_feat, feat, cv2.FaceRecognizerSF_FR_COSINE))
            if score > max_score:
                max_score = score
                
        # SFace Cosine Threshold: > 0.363 is considered matching
        if max_score >= 0.30:
            matches.append({
                "filename": p['filename'],
                "category": p['category'],
                "score": max_score,
                "drive_link": p['drive_link'],
                "thumbnail": p['thumbnail']
            })

matches.sort(key=lambda x: x['score'], reverse=True)
print(f"Processed {processed} local photos. Found {len(matches)} potential matches:")
for m in matches[:15]:
    print(f"  {m['filename']} ({m['category']}) -> Score: {m['score']*100:.1f}%")

with open('top_matches_co_ngoc.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)
