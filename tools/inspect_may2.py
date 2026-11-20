import urllib.request
import re

url = 'https://drive.google.com/drive/folders/1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    text = resp.read().decode('utf-8', errors='ignore')

items = re.findall(r'aria-label="([^"]+)"[^>]*ssk=[\'"]5:[^:]*:([a-zA-Z0-9_-]{25,})', text)
print(f"Total aria-label items in may_2: {len(items)}")
for name, fid in items[:15]:
    print(f"  {name} -> {fid}")
