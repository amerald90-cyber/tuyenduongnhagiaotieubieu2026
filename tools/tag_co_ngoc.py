import json

with open("database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

co_ngoc_files = {'PKN08738.jpg', 'TMK_8546.jpg', 'TM7_3650.jpg', 'TMK_8553.jpg', 'PKN08759.jpg', 'TMK_8559.jpg'}

for p in db['photos']:
    if p['filename'] in co_ngoc_files:
        p['person'] = "Đinh Thị Ngọc"
        p['tags'] = ["Đinh Thị Ngọc", "Nhà giáo Đinh Thị Ngọc", "Cô Ngọc", "Tiêu biểu 2026"]

with open("database.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False)

print("Updated database.json with verified teacher tags!")
