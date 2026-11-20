import json

notebook = {
    'nbformat': 4,
    'nbformat_minor': 2,
    'metadata': {
        'language_info': {'name': 'python'},
        'accelerator': 'GPU',
        'colab': {
            'provenance': [],
            'gpuType': 'T4'
        }
    },
    'cells': []
}

def add_markdown(source):
    notebook['cells'].append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line + '\n' for line in source.split('\n')]
    })

def add_code(source):
    notebook['cells'].append({
        'cell_type': 'code',
        'metadata': {},
        'execution_count': None,
        'outputs': [],
        'source': [line + '\n' for line in source.split('\n')]
    })

# Cell 1: Intro
add_markdown('''# 📸 ỨNG DỤNG TÌM KIẾM ẢNH THEO KHUÔN MẶT TỪ GOOGLE DRIVE
> **Đặc điểm nổi bật:**
> - ✅ **Không tốn 1MB dung lượng ổ cứng máy tính cá nhân**: Xử lý 100% trên Cloud của Google Colab (có sẵn GPU T4 miễn phí).
> - ✅ **Tự động quét toàn bộ các link Drive bạn đã cung cấp**:
>   1. MÁY 1 (`1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor`)
>   2. MÁY 2 (`1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE`)
>   3. Trường Kinh Tế (`1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx`)
>   4. Ảnh Vinh Danh (`1k561p2E4havGIaTQL-e66oFAeuEz4Ywy`)
>   5. Lễ 2011.rar (`11rymbDb2rXEvv8viFivthLW49Ct3ICwj`)
> - ✅ **Sử dụng AI InsightFace**: Chuẩn nhận diện khuôn mặt chính xác nhất hiện nay, tìm chuẩn xác dù ảnh đông người hay chụp từ xa.
> - ✅ **Giao diện Web trực quan**: Có link web để bấm vào tải mặt mẫu lên và nhận diện ngay lập tức!
''')

# Cell 2: Install dependencies
add_markdown('''### 🚀 Bước 1: Cài đặt các thư viện cần thiết trên Colab (Mất ~1-2 phút)
*Bấm nút ▶️ Play để chạy ô này.*''')

add_code('''!pip install -q gdown insightface onnxruntime-gpu gradio opencv-python-headless pillow unrar
!apt-get install -y unrar''')

# Cell 3: Download & Extract
add_markdown('''### 📥 Bước 2: Tự động tải & chuẩn bị ảnh từ Google Drive lên đám mây Colab
*Toàn bộ ảnh sẽ được tải vào bộ nhớ tạm của Google Colab, hoàn toàn KHÔNG tải vào máy tính của bạn.*''')

add_code('''import os
import gdown
import subprocess
import shutil

os.makedirs("/content/photos_raw", exist_ok=True)
os.makedirs("/content/all_photos", exist_ok=True)

# Danh sách tất cả các link của bạn
DRIVE_SOURCES = [
    {"name": "MAY_1", "id": "1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor", "type": "folder"},
    {"name": "MAY_2", "id": "1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE", "type": "folder"},
    {"name": "Truong_Kinh_Te", "id": "1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx", "type": "folder"},
    {"name": "Anh_Vinh_Danh", "id": "1k561p2E4havGIaTQL-e66oFAeuEz4Ywy", "type": "folder"},
    {"name": "Le_2011_rar", "id": "11rymbDb2rXEvv8viFivthLW49Ct3ICwj", "type": "file"}
]

print("🔄 Đang tải các thư mục và file từ Google Drive lên Cloud...")

for src in DRIVE_SOURCES:
    folder_path = f"/content/photos_raw/{src['name']}"
    os.makedirs(folder_path, exist_ok=True)
    print(f"\\n⬇️ Đang tải nguồn: {src['name']}...")
    try:
        if src['type'] == 'folder':
            gdown.download_folder(id=src['id'], output=folder_path, quiet=False, use_cookies=False)
        else:
            rar_dest = f"/content/photos_raw/{src['name']}.rar"
            gdown.download(id=src['id'], output=rar_dest, quiet=False)
            if os.path.exists(rar_dest):
                print(f"📦 Đang giải nén {rar_dest}...")
                subprocess.run(["unrar", "x", "-o+", rar_dest, folder_path], stdout=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Lỗi khi tải {src['name']}: {e}")

# Gom toàn bộ ảnh vào 1 thư mục chuẩn để AI quét
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.heic', '.JPG', '.JPEG', '.PNG'}
count = 0
for root, dirs, files in os.walk("/content/photos_raw"):
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext in IMAGE_EXTS:
            src_file = os.path.join(root, file)
            prefix = os.path.basename(os.path.dirname(src_file))
            new_name = f"{prefix}_{file}".replace(" ", "_")
            dst_file = os.path.join("/content/all_photos", new_name)
            shutil.copy2(src_file, dst_file)
            count += 1

print(f"\\n✅ HOÀN TẤT! Đã tập hợp tổng cộng {count} bức ảnh vào kho dữ liệu.")
''')

# Cell 4: Face Indexing
add_markdown('''### 🧠 Bước 3: AI Quét khuôn mặt & Tạo dữ liệu tìm kiếm
*Mô hình InsightFace sẽ quét và trích xuất vector đặc trưng khuôn mặt trong toàn bộ kho ảnh.*''')

add_code('''import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import pickle
from tqdm import tqdm

print("🤖 Đang khởi tạo mô hình AI InsightFace...")
# Khởi tạo mô hình AI sử dụng GPU
app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

photo_dir = "/content/all_photos"
all_files = [f for f in os.listdir(photo_dir) if os.path.isfile(os.path.join(photo_dir, f))]

face_database = [] # Lưu: {'filename': ..., 'embedding': ...}

print(f"🔍 Bắt đầu quét khuôn mặt trên {len(all_files)} ảnh...")

for fname in tqdm(all_files):
    fpath = os.path.join(photo_dir, fname)
    img = cv2.imread(fpath)
    if img is None:
        continue
    
    # Nhận diện khuôn mặt trong ảnh
    faces = app.get(img)
    for face in faces:
        norm_emb = face.normed_embedding
        face_database.append({
            'filename': fname,
            'embedding': norm_emb
        })

print(f"\\n✅ ĐÃ QUÉT XONG! Tìm thấy và ghi nhớ {len(face_database)} khuôn mặt trong toàn bộ kho ảnh.")

# Lưu file database nhỏ gọn
with open("/content/face_database.pkl", "wb") as f:
    pickle.dump(face_database, f)
print("💾 Đã lưu chỉ mục tìm kiếm vào /content/face_database.pkl!")
''')

# Cell 5: Gradio UI
add_markdown('''### 🌐 Bước 4: Mở Giao diện Web Tìm kiếm khuôn mặt (Web App)
*Bấm Play để nhận đường link Web (Public URL). Bạn có thể mở web trên máy tính hoặc điện thoại để tải mặt lên lọc ảnh.*''')

add_code('''import gradio as gr
import zipfile

with open("/content/face_database.pkl", "rb") as f:
    face_database = pickle.load(f)

def search_face(query_img, similarity_threshold=0.45):
    if query_img is None:
        return [], "Vui lòng chọn hoặc chụp ảnh khuôn mặt cần tìm!", None
    
    # Đổi RGB sang BGR cho OpenCV
    query_bgr = cv2.cvtColor(np.array(query_img), cv2.COLOR_RGB2BGR)
    query_faces = app.get(query_bgr)
    
    if len(query_faces) == 0:
        return [], "❌ Không nhận diện được khuôn mặt nào trong ảnh tải lên. Vui lòng thử ảnh rõ nét hơn!", None
    
    # Lấy khuôn mặt rõ nhất trong ảnh mẫu
    best_query_face = max(query_faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
    target_emb = best_query_face.normed_embedding
    
    # So khớp độ tương đồng Cosine
    matched_photos = {}
    for item in face_database:
        sim = float(np.dot(target_emb, item['embedding']))
        if sim >= similarity_threshold:
            fname = item['filename']
            if fname not in matched_photos or sim > matched_photos[fname]:
                matched_photos[fname] = sim
    
    # Sắp xếp ảnh theo độ khớp từ cao xuống thấp
    sorted_matches = sorted(matched_photos.items(), key=lambda x: x[1], reverse=True)
    
    gallery_images = []
    zip_path = None
    
    if sorted_matches:
        zip_path = "/content/ket_qua_anh_cua_ban.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for fname, score in sorted_matches:
                img_path = os.path.join("/content/all_photos", fname)
                gallery_images.append(img_path)
                zipf.write(img_path, arcname=fname)
        
        status_msg = f"🎉 TÌM THẤY {len(sorted_matches)} BỨC ẢNH CÓ MẶT NGƯỜI NÀY!\\nĐộ chính xác cao nhất: {sorted_matches[0][1]*100:.1f}%"
    else:
        status_msg = f"Không tìm thấy ảnh nào khớp với ngưỡng tương đồng {similarity_threshold}. Thử hạ thanh trượt ngưỡng xuống xem sao nhé!"
        
    return gallery_images, status_msg, zip_path

# Thiết kế giao diện Web
with gr.Blocks(title="AI Tìm Kiếm Ảnh Theo Khuôn Mặt") as demo:
    gr.Markdown("# 🎓 HỆ THỐNG TÌM KIẾM ẢNH SỰ KIỆN QUA KHUÔN MẶT")
    gr.Markdown("Chỉ cần tải lên 1 tấm ảnh khuôn mặt (ảnh thẻ, selfie, chân dung), AI sẽ lọc toàn bộ ảnh có bạn trong sự kiện.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_img = gr.Image(type="pil", label="1. Tải ảnh khuôn mặt cần tìm")
            threshold_slider = gr.Slider(minimum=0.3, maximum=0.7, value=0.45, step=0.02, label="Độ nhạy nhận diện (Mặc định: 0.45)")
            search_btn = gr.Button("🔍 Bắt đầu tìm kiếm ảnh", variant="primary")
            status_output = gr.Textbox(label="Thông báo kết quả", interactive=False)
            download_zip = gr.File(label="📥 Tải về file ZIP chứa tất cả ảnh tìm được")
            
        with gr.Column(scale=2):
            result_gallery = gr.Gallery(label="2. Danh sách ảnh tìm thấy", columns=3, height=600)
            
    search_btn.click(
        fn=search_face,
        inputs=[input_img, threshold_slider],
        outputs=[result_gallery, status_output, download_zip]
    )

# Khởi chạy kèm link chia sẻ công khai
demo.launch(share=True, debug=True)
''')

# Write notebook file
with open(r'c:\Users\ADMIN\Desktop\ảnh nhà giáo\Tim_Kiem_Khuon_Mat_GoogleDrive.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print('Notebook created successfully!')
