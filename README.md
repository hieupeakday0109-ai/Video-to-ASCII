# Video to ASCII Player (PowerShell / Windows Terminal)

Chương trình chuyển đổi và phát video trực tiếp trong **PowerShell**, **Command Prompt** hoặc **Windows Terminal** bằng các ký tự văn bản ASCII với bảng menu tương tác trực quan.

---

## ⚡ Cực kỳ đơn giản - Không cần nhớ câu lệnh!

### 🎯 Cách 1: Kéo thả video vào `Play_ASCII.bat` (Khuyên dùng)
1. Nắm chuột kéo file video (`.mp4`, `.mkv`, `.avi`,...) thả thẳng vào file **`Play_ASCII.bat`**.
2. Bảng điều khiển sẽ hiện ra, bạn chỉ cần bấm **Enter** để phát ngay (hoặc bấm phím `1` đến `5` để đổi chế độ):
   - **[1]** 🎨 Màu sắc TrueColor (RGB sống động, sắc nét) - *[Mặc định]*
   - **[2]** 📺 Đen trắng cổ điển (Monochrome ASCII)
   - **[3]** 🟢 Phong cách Hacker Matrix (Xanh Neon Cyberpunk siêu ngầu)
   - **[4]** 💎 Siêu chi tiết Full HD (Bộ ký tự mở rộng 70 ký tự)
   - **[5]** 🔇 Chế độ im lặng (Phát không tiếng)

### 🖱️ Cách 2: Click đúp vào `Play_ASCII.bat`
- Click đúp vào file `Play_ASCII.bat`.
- Cửa sổ chọn file của Windows sẽ tự động mở lên để bạn chọn video, sau đó bảng menu sẽ xuất hiện để bạn chọn chế độ.

### 💻 Cách 3: Chạy qua dòng lệnh
```bash
# Mở menu tương tác chọn chế độ
python ascii_player.py "duong_dan_video.mp4"

# Hoặc chạy thẳng không qua menu bằng các cờ tùy chọn:
python ascii_player.py "duong_dan_video.mp4" --matrix    # Chế độ Matrix Hacker
python ascii_player.py "duong_dan_video.mp4" --mono      # Chế độ đen trắng
python ascii_player.py "duong_dan_video.mp4" --detailed  # Chế độ ký tự chi tiết
python ascii_player.py "duong_dan_video.mp4" --no-audio  # Tắt tiếng
```

> **Mẹo:** Nhấn tổ hợp phím `Ctrl + C` bất cứ lúc nào để dừng phát video.

---

## ✨ Tính năng nổi bật

- ⚡ **Chống nhấp nháy (Flicker-Free):** Dùng mã ANSI `\x1b[H` định vị con trỏ, khung hình 30-60 FPS mượt mà tuyệt đối.
- 🟢 **Chế độ Matrix Hacker:** Chuyển đổi toàn bộ video sang tông màu xanh lá neon Cyberpunk đặc trưng.
- 🎨 **Màu sắc TrueColor RGB:** Giữ nguyên vẹn màu sắc điểm ảnh gốc của video.
- 📐 **Tự cân bằng tỷ lệ:** Tự tính toán theo font chữ terminal để video không bị biến dạng kéo dài.
- 📺 **Tự co giãn:** Tự căn chỉnh vừa khít với kích thước cửa sổ console hiện tại.
- 🔊 **Âm thanh đồng bộ:** Tự động phát âm thanh nền qua `ffplay` (nếu máy có cài FFmpeg).

---

## 🚀 Cài đặt thư viện (nếu dùng trên máy mới)

```bash
pip install -r requirements.txt
```

---

## 🛠️ Cấu trúc dự án
```text
Video-to-ASCII/
│
├── Play_ASCII.bat     # File chạy nhanh (click đúp hoặc kéo thả video vào)
├── ascii_player.py    # Mã nguồn chính tích hợp menu tương tác & phát video
├── run.ps1            # Script hỗ trợ chạy trên PowerShell
├── demo.mp4           # Video mẫu kiểm tra
├── requirements.txt   # Danh sách thư viện Python cần thiết
├── .gitignore         # Tệp cấu hình bỏ qua của Git
└── README.md          # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
