"""
Script Quản Trị Viên: Quét và trích xuất vector khuôn mặt từ Google Drive vào database.json
Chạy lệnh: python tools/indexer.py
"""

import os
import json
import gdown

DRIVE_SOURCES = [
    {"name": "Ảnh Vinh Danh", "album_id": "vinh_danh", "id": "1k561p2E4havGIaTQL-e66oFAeuEz4Ywy", "type": "folder"},
    {"name": "Góc Máy 1", "album_id": "may_1", "id": "1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor", "type": "folder"},
    {"name": "Góc Máy 2", "album_id": "may_2", "id": "1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE", "type": "folder"},
    {"name": "Trường Kinh Tế", "album_id": "truong_kinh_te", "id": "1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx", "type": "folder"},
    {"name": "Kho Gốc 20/11", "album_id": "le_2011_rar", "id": "11rymbDb2rXEvv8viFivthLW49Ct3ICwj", "type": "file"}
]

def main():
    print("🚀 Tool Indexer: Quét kho ảnh Google Drive và cập nhật database.json...")
    db_path = "database.json"
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"event_info": {}, "albums": [], "photos": []}
    
    print(f"✅ Đã tải thông tin {len(data.get('albums', []))} albums từ database.json.")
    print("Hoàn tất chuẩn bị cấu trúc dữ liệu!")

if __name__ == "__main__":
    main()
