# Video to ASCII Player (PowerShell / Windows Terminal)

Chương trình chuyển đổi và phát video trực tiếp trong **PowerShell**, **Command Prompt** hoặc **Windows Terminal** bằng các ký tự văn bản ASCII.

---

## 🌟 Trải nghiệm ứng dụng với Icon trên màn hình (Desktop)

### 🖱️ 1. Mở từ Icon trên màn hình Desktop:
1. Nhấp đúp vào biểu tượng **`Video to ASCII Player`** trên màn hình Desktop của bạn.
2. Bảng điều khiển trực quan sẽ xuất hiện:
   - 📂 **Chọn Video:** Chọn bất kỳ video nào trên máy tính (`.mp4`, `.mkv`, `.avi`,...).
   - 🎨 **Chế độ màu:** Chọn *Màu sắc TrueColor*, *Hacker Matrix (Xanh neon)*, hoặc *Đen trắng cổ điển*.
   - ☑️ **Tích chọn tính năng:** Bật/tắt âm thanh, bật chế độ 70 ký tự siêu chi tiết.
   - 👉 Nhấn nút **`▶ BẮT ĐẦU PHÁT VIDEO (OK)`** là cửa sổ trình chiếu ASCII sẽ hiện ra ngay lập tức!

*(Nếu muốn tạo lại icon ngoài Desktop, bạn chỉ cần chạy script `create_desktop_shortcut.ps1`)*.

---

### 🎯 2. Kéo thả video vào `Play_ASCII.bat`:
- Giữ chuột kéo file video bất kỳ **thả thẳng vào file `Play_ASCII.bat`** để phát ngay lập tức.

---

### 💻 3. Chạy qua dòng lệnh (Terminal):
```bash
# Mở bảng chọn video và chế độ tương tác ngay trong terminal
python ascii_player.py

# Hoặc mở bảng điều khiển GUI tích chọn:
python gui_launcher.py

# Hoặc phát trực tiếp video chỉ định:
python ascii_player.py "duong_dan_video.mp4" --matrix
```

---

## ✨ Tính năng nổi bật

- 🖥️ **Icon & Bảng điều khiển tiện lợi:** Bấm vào icon Desktop, tích chọn chế độ tùy thích rồi bấm OK là xem được ngay.
- ⚡ **Chống nhấp nháy (Flicker-Free):** Dùng mã ANSI `\x1b[H` định vị con trỏ, khung hình 30-60 FPS mượt mà tuyệt đối.
- 🟢 **Chế độ Matrix Hacker:** Chuyển đổi toàn bộ video sang tông màu xanh lá neon Cyberpunk đặc trưng.
- 🎨 **Màu sắc TrueColor RGB:** Giữ nguyên vẹn màu sắc điểm ảnh gốc của video.
- 📐 **Tự cân bằng tỷ lệ:** Tự tính toán theo font chữ terminal để video không bị biến dạng kéo dài.
- 📺 **Tự co giãn:** Tự căn chỉnh vừa khít với kích thước cửa sổ console hiện tại.
- 🔊 **Âm thanh đồng bộ:** Tự động phát âm thanh nền qua `ffplay` (nếu máy có cài FFmpeg).

---

## 🛠️ Cấu trúc dự án
```text
Video-to-ASCII/
│
├── gui_launcher.py             # Bảng điều khiển GUI tích chọn chế độ và chọn file
├── create_desktop_shortcut.ps1 # Script tạo icon ra màn hình Desktop
├── Play_ASCII.bat              # File chạy nhanh (click đúp hoặc kéo thả video vào)
├── ascii_player.py             # Mã nguồn chính xử lý video sang ASCII
├── run.ps1                     # Script hỗ trợ chạy trên PowerShell
├── demo.mp4                    # Video mẫu kiểm tra
├── requirements.txt            # Danh sách thư viện Python cần thiết
├── .gitignore                  # Tệp cấu hình bỏ qua của Git
└── README.md                   # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
