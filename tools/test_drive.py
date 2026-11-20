import urllib.request
import re
import json

folder_id = '1k561p2E4havGIaTQL-e66oFAeuEz4Ywy'
url = f'https://drive.google.com/drive/folders/{folder_id}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print('HTML length:', len(html))
        
        # Look for drive data
        with open('drive_sample.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Wrote drive_sample.html')
except Exception as e:
    print('Error:', e)
