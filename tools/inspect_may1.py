import re

with open('may_1_sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

items = re.findall(r'aria-label="([^"]+)"[^>]*ssk=[\'"]5:[^:]*:([a-zA-Z0-9_-]{25,})', text)
print(f"Total aria-label items in may_1: {len(items)}")
for name, fid in items[:15]:
    print(f"  {name} -> {fid}")
