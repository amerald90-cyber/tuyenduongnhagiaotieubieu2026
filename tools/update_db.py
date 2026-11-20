import json

with open("event_photos_database.json", "r", encoding="utf-8") as f:
    photos = json.load(f)

# Update database.json
database = {
    "event_info": {
        "title": "LỄ TUYÊN DƯƠNG NHÀ GIÁO TIÊU BIỂU 2026",
        "organization": "Trường Đại học Kinh Tế",
        "total_photos": len(photos),
        "last_updated": "2026-11-20"
    },
    "albums": [
        {
            "id": "vinh_danh",
            "name": "Ảnh Vinh Danh (Máy 1)",
            "drive_id": "1k561p2E4havGIaTQL-e66oFAeuEz4Ywy",
            "drive_link": "https://drive.google.com/drive/folders/1k561p2E4havGIaTQL-e66oFAeuEz4Ywy",
            "count": 49
        },
        {
            "id": "may_1",
            "name": "Góc Máy 1 (Check-in & MC & Toàn Cảnh)",
            "drive_id": "1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor",
            "drive_link": "https://drive.google.com/drive/folders/1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor",
            "count": 100
        },
        {
            "id": "may_2",
            "name": "Góc Máy 2 (Biểu Diễn, Thứ Trưởng & Khán Giả)",
            "drive_id": "1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE",
            "drive_link": "https://drive.google.com/drive/folders/1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE",
            "count": 124
        },
        {
            "id": "truong_kinh_te",
            "name": "Trường Kinh Tế (Tập Thể)",
            "drive_id": "1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx",
            "drive_link": "https://drive.google.com/drive/folders/1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx",
            "count": 49
        }
    ],
    "photos": photos
}

with open("database.json", "w", encoding="utf-8") as f:
    json.dump(database, f, ensure_ascii=False, indent=2)

print(f"Successfully updated database.json with {len(photos)} real photos!")
