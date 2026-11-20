import os
import json
import urllib.request
import re

os.makedirs("thumbnails", exist_ok=True)

with open("event_photos_database.json", "r", encoding="utf-8") as f:
    photos = json.load(f)

print(f"Total photos in database: {len(photos)}")

success = 0
failed = 0

for i, p in enumerate(photos):
    out_path = os.path.join("thumbnails", f"{p['id']}.jpg")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        success += 1
        continue
    
    # Try thumbnail URL
    url = p['thumbnail']
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(out_path, "wb") as f:
                    f.write(data)
                success += 1
            else:
                failed += 1
    except Exception as e:
        failed += 1

print(f"✅ Finished! Available thumbnails: {success}, Failed: {failed}")
