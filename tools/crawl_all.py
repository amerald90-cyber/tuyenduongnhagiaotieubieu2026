import urllib.request
import re
import json

folders_to_crawl = [
    # MÁY 1 Subfolders
    {"name": "Ảnh Check-in (Máy 1)", "album_id": "may_1", "id": "1LMkw69BGat0zhjLVdlD3zAf3X0v88mMb"},
    {"name": "Ảnh MC (Máy 1)", "album_id": "may_1", "id": "1kZNK_5CMsEQuRbwKvRms_6FUP6BpdH8v"},
    {"name": "Ảnh Vinh Danh (Máy 1)", "album_id": "vinh_danh", "id": "1k561p2E4havGIaTQL-e66oFAeuEz4Ywy"},
    # MÁY 2 Subfolders
    {"name": "Biểu Diễn Nghệ Thuật (Máy 2)", "album_id": "may_2", "id": "1hIY5b6jjhtn6SiKEAN28QApj_JPA2bWK"},
    {"name": "Thứ Trưởng Phát Biểu (Máy 2)", "album_id": "may_2", "id": "1mxQ_10ZdhFbdQWjhZ-xyLFxutUAQuiqb"},
    {"name": "Đại Biểu & Khán Giả (Máy 2)", "album_id": "may_2", "id": "1LoqNhvwoGAmVs2FO04yeqaqsJp74rgzW"},
    # Trường Kinh Tế
    {"name": "Trường Kinh Tế", "album_id": "truong_kinh_te", "id": "1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx"},
]

def get_photos(item):
    fid = item['id']
    url = f"https://drive.google.com/drive/folders/{fid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        pattern = r'aria-label="([^"]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))[^"]*"[^>]*ssk=[\'"]5:[^:]*:([a-zA-Z0-9_-]{25,})'
        matches = re.findall(pattern, html)
        
        photos = []
        seen = set()
        for filename, raw_id in matches:
            clean_id = raw_id.split('-')[0]
            if clean_id not in seen:
                seen.add(clean_id)
                photos.append({
                    "id": clean_id,
                    "title": filename,
                    "filename": filename,
                    "category": item['name'],
                    "album": item['name'],
                    "album_id": item['album_id'],
                    "thumbnail": f"https://drive.google.com/thumbnail?id={clean_id}&sz=w800",
                    "drive_link": f"https://drive.google.com/file/d/{clean_id}/view"
                })
        print(f"[{item['name']}] Found {len(photos)} photos.")
        return photos
    except Exception as e:
        print(f"[{item['name']}] Error: {e}")
        return []

all_event_photos = []
for f in folders_to_crawl:
    photos = get_photos(f)
    all_event_photos.extend(photos)

print(f"\n==========================================")
print(f"TOTAL REAL EVENT PHOTOS FOUND: {len(all_event_photos)}")
print(f"==========================================")

with open("event_photos_database.json", "w", encoding="utf-8") as f:
    json.dump(all_event_photos, f, ensure_ascii=False, indent=2)
