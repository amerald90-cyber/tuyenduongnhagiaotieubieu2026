import re

with open('bibpix_sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for forms, search inputs, face search buttons
inputs = re.findall(r'<input[^>]+>', text)
print("=== INPUTS ===")
for inp in inputs:
    print(" ", inp)

# Look for titles
titles = re.findall(r'<title>(.*?)</title>', text, re.IGNORECASE)
print("\n=== TITLE ===")
print(titles)

# Look for keywords like "BIB", "Khuôn mặt", "Face", "Upload", "Tìm kiếm"
keywords = ['bib', 'face', 'khuôn mặt', 'tìm kiếm', 'search', 'selfie', 'nhận diện']
for kw in keywords:
    matches = re.findall(rf'[^.!?\n]*{kw}[^.!?\n]*', text, re.IGNORECASE)
    print(f"\n=== KEYWORD '{kw}' (Found {len(matches)}) ===")
    for m in matches[:3]:
        print(" ", m.strip())
