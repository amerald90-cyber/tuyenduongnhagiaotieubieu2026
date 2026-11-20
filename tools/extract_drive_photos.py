import urllib.request
import re
import json

def fetch_folder_photos(folder_id, album_name, album_id):
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        pattern = r'aria-label="([^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))[^"]*"[^>]*ssk=[\'"]5:[^:]*:([a-zA-Z0-9_-]{25,})'
        matches = re.findall(pattern, html)
        
        photos = []
        seen = set()
        for filename, file_id in matches:
            # clean file_id if needed
            clean_id = file_id.split('-')[0] if '-' in file_id else file_id
            if clean_id not in seen:
                seen.add(clean_id)
                photos.append({
                    "id": clean_id,
                    "title": filename,
                    "filename": filename,
                    "album": album_name,
                    "album_id": album_id,
                    "thumbnail": f"https://drive.google.com/thumbnail?id={clean_id}&sz=w800",
                    "drive_link": f"https://drive.google.com/file/d/{clean_id}/view"
                })
        print(f"[{album_name}] Fetched {len(photos)} photos.")
        return photos
    except Exception as e:
        print(f"[{album_name}] Error: {e}")
        return []

folders = [
    ("Ảnh Vinh Danh", "vinh_danh", "1k561p2E4havGIaTQL-e66oFAeuEz4Ywy"),
    ("Góc Máy 1", "may_1", "1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor"),
    ("Góc Máy 2", "may_2", "1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE"),
    ("Trường Kinh Tế", "truong_kinh_te", "1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx")
]

all_photos = []
for name, aid, fid in folders:
    p = fetch_folder_photos(fid, name, aid)
    all_photos.extend(p)

print(f"Total photos extracted: {len(all_photos)}")
with open("real_photos_list.json", "w", encoding="utf-8") as f:
    json.dump(all_photos, f, ensure_ascii=False, indent=2)
