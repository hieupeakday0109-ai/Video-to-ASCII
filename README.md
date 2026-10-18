# Video to ASCII Player (PowerShell / Windows Terminal)

Chương trình chuyển đổi và phát video trực tiếp trong **PowerShell**, **Command Prompt** hoặc **Windows Terminal** bằng các ký tự văn bản ASCII.

---

## ⚡ Cực kỳ đơn giản - Không cần gõ lệnh phức tạp!

Bạn có thể chạy video theo **3 cách siêu nhanh**:

### 🎯 Cách 1: Kéo thả video vào file `Play_ASCII.bat` (Nhanh nhất!)
- Chỉ cần nắm chuột kéo file video (`.mp4`, `.mkv`, `.avi`,...) và **thả thẳng vào file `Play_ASCII.bat`**.
- Video sẽ tự động phát với đầy đủ màu sắc và âm thanh ngay lập tức!

### 🖱️ Cách 2: Click đúp vào `Play_ASCII.bat`
- Nhấp đúp chuột vào file `Play_ASCII.bat` (hoặc chạy `python ascii_player.py`).
- Cửa sổ chọn tệp của Windows sẽ hiện lên để bạn chọn video, hoặc bạn có thể kéo thả file video vào cửa sổ đen rồi nhấn **Enter**.

### 💻 Cách 3: Chạy qua dòng lệnh (Dành cho ai thích gõ lệnh)
```bash
# Phát video bất kỳ (Mặc định tự bật màu đẹp nhất)
python ascii_player.py "duong_dan_video.mp4"

# Chế độ đen trắng cổ điển
python ascii_player.py "duong_dan_video.mp4" --mono

# Tắt âm thanh
python ascii_player.py "duong_dan_video.mp4" --no-audio
```

> **Mẹo:** Nhấn tổ hợp phím `Ctrl + C` bất cứ lúc nào để dừng phát video.

---

## ✨ Tính năng nổi bật

- ⚡ **Chống nhấp nháy (Flicker-Free):** Sử dụng mã điều khiển con trỏ ANSI `\x1b[H` thay vì lệnh xóa màn hình `cls`, giúp khung hình mượt mà tuyệt đối ở 30-60 FPS.
- 🎨 **Màu sắc sống động (TrueColor RGB):** Mặc định hiển thị đầy đủ màu sắc nguyên bản của từng điểm ảnh.
- 📐 **Tự động cân bằng tỷ lệ khung hình:** Ký tự terminal có chiều cao gấp đôi bề ngang, thuật toán tự động bù trừ tỷ lệ để hình ảnh không bị méo.
- 📺 **Tự động co giãn theo cửa sổ:** Tự đo kích thước cột và dòng của cửa sổ PowerShell để phóng to/thu nhỏ video tối ưu nhất.
- 🔊 **Đồng bộ âm thanh:** Tự động phát âm thanh nền song song bằng `ffplay` nếu máy tính có cài đặt FFmpeg.

---

## 🚀 Cài đặt thư viện (nếu dùng trên máy mới)

Chỉ cần chạy lệnh:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Cấu trúc dự án
```text
Video-to-ASCII/
│
├── Play_ASCII.bat     # File nhấp đúp hoặc kéo thả video vào để chạy ngay
├── ascii_player.py    # Mã nguồn chính xử lý video sang ASCII
├── run.ps1            # Script hỗ trợ chạy trên PowerShell
├── demo.mp4           # Video mẫu kiểm tra
├── requirements.txt   # Danh sách thư viện Python cần thiết
├── .gitignore         # Tệp cấu hình bỏ qua của Git
└── README.md          # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
