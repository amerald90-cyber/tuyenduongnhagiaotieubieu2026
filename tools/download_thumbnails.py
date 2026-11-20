import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

os.makedirs("thumbnails", exist_ok=True)

with open("event_photos_database.json", "r", encoding="utf-8") as f:
    photos = json.load(f)

def download_one(p):
    out_path = os.path.join("thumbnails", f"{p['id']}.jpg")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return True
    try:
        req = urllib.request.Request(p['thumbnail'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(out_path, "wb") as f:
                    f.write(data)
                return True
    except Exception as e:
        pass
    return False

print(f"Downloading thumbnails for {len(photos)} photos using 12 threads...")
with ThreadPoolExecutor(max_workers=12) as executor:
    results = list(executor.map(download_one, photos))

downloaded = len([f for f in os.listdir("thumbnails") if f.endswith(".jpg")])
print(f"✅ Successfully downloaded {downloaded}/{len(photos)} thumbnails to local folder!")
