import cv2
import numpy as np
import urllib.request
import json
import time

# 1. Load target query face (Cô Đinh Thị Ngọc)
query_path = r'c:\Users\ADMIN\Desktop\1795170991205_2276516459885095864_2138731840136663169_f4193a5c54cdc2270bd87a9353ce03fa.jpg'
q_data = np.fromfile(query_path, dtype=np.uint8)
q_img = cv2.imdecode(q_data, cv2.IMREAD_COLOR)

detector = cv2.FaceDetectorYN.create('models/face_detection_yunet_2023mar.onnx', '', (q_img.shape[1], q_img.shape[0]), 0.3, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create('models/face_recognition_sface_2021dec.onnx', '')

_, q_faces = detector.detect(q_img)
q_aligned = recognizer.alignCrop(q_img, q_faces[0])
target_feat = recognizer.feature(q_aligned)

print("🎯 Extracted target face feature for Cô Đinh Thị Ngọc!")

# 2. Search in event photos
with open('event_photos_database.json', 'r', encoding='utf-8') as f:
    photos = json.load(f)

# Priority: check photos in 'Ảnh Check-in (Máy 1)' and 'Ảnh Vinh Danh (Máy 1)'
check_list = [p for p in photos if 'Check-in' in p['category'] or 'Vinh Danh' in p['category']]
print(f"Scanning {len(check_list)} photos in Check-in and Vinh Danh...")

matched_photos = []

for i, p in enumerate(check_list):
    try:
        req = urllib.request.Request(p['thumbnail'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = np.frombuffer(resp.read(), dtype=np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            
        if img is None:
            continue
            
        h, w = img.shape[:2]
        detector.setInputSize((w, h))
        _, faces = detector.detect(img)
        
        if faces is not None:
            max_score = 0
            for face in faces:
                aligned = recognizer.alignCrop(img, face)
                feat = recognizer.feature(aligned)
                # Cosine similarity
                score = recognizer.match(target_feat, feat, cv2.FaceRecognizerSF_FR_COSINE)
                if score > max_score:
                    max_score = score
            
            # SFace cosine similarity threshold typically: > 0.363 is same person
            if max_score > 0.363:
                print(f"✨ MATCH FOUND! {p['filename']} ({p['category']}) -> Cosine Score: {max_score:.3f}")
                matched_photos.append({
                    "filename": p['filename'],
                    "category": p['category'],
                    "score": float(max_score),
                    "drive_link": p['drive_link'],
                    "thumbnail": p['thumbnail']
                })
    except Exception as e:
        continue

print(f"\n==========================================")
print(f"🎉 FOUND {len(matched_photos)} EXACT MATCHING PHOTOS!")
for m in matched_photos:
    print(f" - {m['filename']} ({m['category']}): {m['score']*100:.1f}% -> {m['drive_link']}")
print(f"==========================================")

with open('matched_teacher_photos.json', 'w', encoding='utf-8') as f:
    json.dump(matched_photos, f, ensure_ascii=False, indent=2)
