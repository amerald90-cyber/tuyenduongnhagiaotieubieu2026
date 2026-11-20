# 📖 HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG TÌM KIẾM ẢNH BẰNG KHUÔN MẶT (GOOGLE COLAB)

Ứng dụng này đã được cấu hình sẵn **100% các đường link Google Drive bạn đã gửi** và chạy hoàn toàn trên đám mây của Google Colab:
- ✅ **KHÔNG TỐN Ổ CỨNG MÁY TÍNH CỦA BẠN**: Không cần tải hàng chục GB ảnh về máy tính cá nhân.
- ✅ **CÓ GPU MIỄN PHÍ**: Quét hàng nghìn ảnh chỉ trong vài phút.
- ✅ **TỰ ĐỘNG XỬ LÝ TẤT CẢ NGUỒN**:
  1. Thư mục `MÁY 1` (`1-oib_yYHmkONErL_HLcpd7Y8kgAAAFor`)
  2. Thư mục `MÁY 2` (`1pGiZJk4jB5VRaYs66S3_OTU-_oHq2mFE`)
  3. Thư mục `Trường Kinh Tế` (`1UYMSRcwWGh2TEwItW0-idFTSGZvQ2vqx`)
  4. Thư mục `Ảnh Vinh Danh` (`1k561p2E4havGIaTQL-e66oFAeuEz4Ywy`)
  5. File nén `Lễ 2011.rar` (`11rymbDb2rXEvv8viFivthLW49Ct3ICwj`)

---

## 🚀 CÁC BƯỚC SỬ DỤNG CỰC KỲ ĐƠN GIẢN

### Bước 1: Mở Google Colab
1. Truy cập vào trang web: [colab.research.google.com](https://colab.research.google.com)
2. Đăng nhập bằng tài khoản Google (Gmail) của bạn.
3. Chọn tab **Upload** (hoặc **Tải lên**), sau đó chọn file:
   👉 `Tim_Kiem_Khuon_Mat_GoogleDrive.ipynb` (nằm trong thư mục `ảnh nhà giáo` trên Desktop của bạn).

---

### Bước 2: Bật GPU miễn phí (Để AI chạy siêu nhanh)
1. Trên menu trên cùng của Colab, bấm vào **Runtime** (Thời gian chạy) ➔ **Change runtime type** (Thay đổi loại thời gian chạy).
2. Tại mục **Hardware accelerator** (Trình tăng tốc phần cứng), chọn **T4 GPU**.
3. Bấm **Save** (Lưu).

---

### Bước 3: Chạy ứng dụng
- Bạn chỉ cần bấm vào menu **Runtime** ➔ **Run all** (Chạy tất cả) - hoặc bấm lần lượt nút **▶️ Play** ở từng ô code từ trên xuống dưới:
  - **Ô 1 & 2**: Cài đặt AI InsightFace và tự động kéo ảnh từ các link Drive về Cloud.
  - **Ô 3**: AI nhận diện và trích xuất vector khuôn mặt.
  - **Ô 4**: Khởi tạo giao diện Web.

---

### Bước 4: Tìm kiếm ảnh trên giao diện Web
Sau khi ô 4 chạy xong, Colab sẽ cung cấp cho bạn 2 đường link:
- **Local URL**: `http://127.0.0.1:7860`
- **Public URL**: `https://xxxxxxxx.gradio.live` *(Đường link công khai có thể mở trên cả điện thoại hoặc gửi cho người khác dùng)*.

**Cách tìm kiếm:**
1. Mở link Web lên.
2. Tải lên 1 tấm ảnh khuôn mặt người cần tìm (ảnh thẻ, ảnh chụp selfie rõ mặt).
3. Bấm **"🔍 Bắt đầu tìm kiếm ảnh"**.
4. Toàn bộ các bức ảnh chụp người đó trong sự kiện sẽ hiển thị ngay bên phải!
5. Bấm vào mục **"📥 Tải về file ZIP"** để tải toàn bộ các ảnh tìm được về máy trong 1 click.
