# Video to ASCII Player (PowerShell / Terminal)

Chương trình chuyển đổi và phát video trực tiếp trong **PowerShell**, **Command Prompt** hoặc **Windows Terminal** bằng các ký tự văn bản ASCII.

## ✨ Tính năng nổi bật

- ⚡ **Chống nhấp nháy (Flicker-Free):** Sử dụng mã điều khiển con trỏ ANSI `\x1b[H` thay vì lệnh xóa màn hình `cls`, giúp khung hình mượt mà tuyệt đối ở 30-60 FPS.
- 🎨 **Hỗ trợ 2 chế độ hiển thị:**
  - **Đen trắng (Monochrome):** Chế độ ASCII cổ điển, sử dụng mật độ sáng tối của ký tự.
  - **Màu sắc (TrueColor RGB):** Hiển thị ký tự với màu sắc gốc của từng điểm ảnh trong video.
- 📐 **Tự động cân bằng tỷ lệ khung hình:** Ký tự terminal có chiều cao gấp đôi bề ngang, thuật toán tự động bù trừ tỷ lệ để hình ảnh không bị kéo dãn.
- 📺 **Tự động co giãn theo cửa sổ:** Tự đo kích thước cột và dòng của cửa sổ PowerShell để phóng to/thu nhỏ video tối ưu nhất.
- 🔊 **Đồng bộ âm thanh:** Tự động phát âm thanh nền song song bằng `ffplay` nếu máy tính có cài đặt FFmpeg.

---

## 🚀 Cài đặt & Chuẩn bị

### 1. Yêu cầu hệ thống
- **Python 3.8+**
- Hệ điều hành: Windows (PowerShell / Windows Terminal), macOS hoặc Linux.

### 2. Cài đặt thư viện Python
```bash
pip install -r requirements.txt
```

*(Tùy chọn)* Nếu muốn có âm thanh đồng bộ khi phát video, hãy cài đặt **FFmpeg** (đảm bảo lệnh `ffplay` khả dụng trong terminal).

---

## 🎬 Hướng dẫn sử dụng

### 1. Chạy cơ bản (Đen trắng)
```bash
python ascii_player.py "duong_dan_video.mp4"
```

### 2. Chạy với màu sắc đầy đủ (TrueColor)
```bash
python ascii_player.py "duong_dan_video.mp4" --color
# hoặc
python ascii_player.py "duong_dan_video.mp4" -c
```

### 3. Dùng bộ ký tự ASCII chi tiết cao
```bash
python ascii_player.py "duong_dan_video.mp4" --color --detailed
```

### 4. Tắt âm thanh
```bash
python ascii_player.py "duong_dan_video.mp4" --no-audio
```

### 5. Dùng script hỗ trợ nhanh trong PowerShell
```powershell
.\run.ps1 -VideoPath "duong_dan_video.mp4" -Color
```

> **Mẹo:** Nhấn tổ hợp phím `Ctrl + C` bất cứ lúc nào để dừng phát video.

---

## 🛠️ Cấu trúc dự án
```text
Video-to-ASCII/
│
├── ascii_player.py    # Mã nguồn chính xử lý và phát video
├── run.ps1            # Script chạy nhanh trên PowerShell
├── demo.mp4           # Video mẫu kiểm tra
├── requirements.txt   # Danh sách thư viện Python cần thiết
├── .gitignore         # Tệp cấu hình bỏ qua của Git
└── README.md          # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
