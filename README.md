# 🎓 Hệ Thống Tra Cứu Ảnh Khuôn Mặt - Lễ Tuyên Dương Nhà Giáo Tiêu Biểu 2026

Ứng dụng web tìm kiếm và lọc ảnh sự kiện thông minh bằng công nghệ **AI Nhận diện khuôn mặt (Face Recognition)** chạy trực tiếp trên trình duyệt web, triển khai nhanh chóng lên **Vercel** và **GitHub**.

---

## 🌟 Tính Năng Nổi Bật

- 🤖 **AI Nhận diện khuôn mặt Client-side**: Sử dụng mô hình `face-api.js` (TensorFlow.js) chạy trực tiếp trong trình duyệt bằng WebGL. Không tốn chi phí server backend, không sợ quá tải.
- 📸 **Đa dạng cách thức nhập ảnh**: Hỗ trợ kéo-thả ảnh từ máy tính/điện thoại hoặc bật trực tiếp Camera selfie để chụp.
- 🎚️ **Thanh điều chỉnh độ nhạy AI (Threshold)**: Dễ dàng tùy chỉnh độ khớp từ 40% đến 85% để tìm được nhiều ảnh hơn hoặc chính xác hơn.
- 📂 **Tích hợp 5 nguồn ảnh Google Drive chính thức**:
  1. **Ảnh Vinh Danh** (`1k561p2E4havGIaTQL-e66oFAeuEz4Ywy`)
  2. **Góc Máy 1** (`1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor`)
  3. **Góc Máy 2** (`1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE`)
  4. **Trường Kinh Tế** (`1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx`)
  5. **Bản Gốc Lễ 20/11** (`11rymbDb2rXEvv8viFivthLW49Ct3ICwj`)
- 📥 **Tải về nhanh chóng**: Xem ảnh phóng to, liên kết mở trực tiếp file gốc trên Google Drive, hoặc bấm nút tải toàn bộ ảnh tìm thấy thành file `.ZIP`.
- 📱 **Giao diện chuẩn Responsive**: Tối ưu hiển thị tuyệt đẹp trên cả điện thoại (iPhone, Android), iPad và máy tính.

---

## 🚀 Hướng Dẫn Đưa Lên Vercel (1 Phút)

### Bước 1: Đăng nhập Vercel
1. Truy cập: [vercel.com](https://vercel.com)
2. Đăng nhập bằng tài khoản **GitHub** (amerald90-cyber).

### Bước 2: Nhập dự án từ GitHub
1. Bấm vào nút **"Add New..."** ➔ **"Project"**.
2. Tìm và chọn repository: `amerald90-cyber/tuyenduongnhagiaotieubieu2026`.
3. Bấm **"Import"**.

### Bước 3: Triển khai (Deploy)
1. Giữ nguyên toàn bộ cấu hình mặc định (Framework Preset: Other / Static).
2. Bấm nút **"Deploy"**.
3. Sau khoảng 20-30 giây, Vercel sẽ cấp cho bạn một đường link website chính thức dạng:  
   👉 `https://tuyenduongnhagiaotieubieu2026.vercel.app`

---

## 💻 Cấu Trúc Mã Nguồn

```
├── index.html        # Giao diện web chính
├── app.js            # Logic AI nhận diện, so khớp vector và xử lý giao diện
├── styles.css         # Giao diện thiết kế (Tailwind CSS + Glassmorphism)
├── database.json     # Cơ sở dữ liệu danh mục Album và metadata ảnh
├── vercel.json       # File cấu hình deploy cho Vercel
├── package.json      # Metadata dự án
├── tools/
│   └── indexer.py    # Script hỗ trợ cập nhật ảnh mới
└── README.md         # Tài liệu dự án
```

---

## 🔒 Bản Quyền & Quyền Riêng Tư

- Ảnh selfie của người dùng chỉ được xử lý tạm thời trên bộ nhớ RAM của trình duyệt thiết bị, không lưu trữ lên bất kỳ server trung gian nào.
- Hệ thống phát triển bởi AI Antigravity phục vụ sự kiện Tuyên dương Nhà giáo Tiêu biểu 2026.
