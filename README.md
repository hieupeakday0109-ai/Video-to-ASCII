# Video to ASCII Player (Cross-Platform: Windows, macOS, Linux)

Chương trình chuyển đổi và phát video trực tiếp trong **Terminal / PowerShell / Command Prompt** bằng các ký tự văn bản ASCII với giao diện bảng điều khiển hiện đại, hỗ trợ đầy đủ trên **Windows, macOS và Linux**!

---

## ⚡ Hướng dẫn cài đặt nhanh 1-Click

### 🪟 Trên Windows
1. Tải bản nén từ mục [Releases](https://github.com/hieupeakday0109-ai/Video-to-ASCII/releases) hoặc tải toàn bộ mã nguồn về máy.
2. Nhấp đúp chuột vào file **`Cai_Dat_Icon.bat`**.
3. Chương trình sẽ tự động cài thư viện và tạo biểu tượng **`Video to ASCII Player`** ra ngoài màn hình chính (Desktop).

---

### 🍎 Trên macOS
1. Mở ứng dụng **Terminal** tại thư mục dự án và chạy:
   ```bash
   bash install.sh
   ```
2. Script sẽ tự cài đặt thư viện và tạo phím tắt **`Video to ASCII.command`** ngay trên màn hình Desktop của bạn.
3. Từ lần sau, bạn chỉ cần nhấp đúp vào phím tắt trên Desktop để mở!

---

### 🐧 Trên Linux (Ubuntu, Debian, Fedora, Arch,...)
1. Mở Terminal tại thư mục dự án và chạy:
   ```bash
   bash install.sh
   ```
2. Script sẽ tự cài đặt thư viện và tạo tệp biểu tượng **`video-to-ascii.desktop`** trên Desktop và Menu ứng dụng của bạn.

---

## 🎮 Cách sử dụng

### 🖱️ 1. Mở từ Icon trên màn hình Desktop:
1. Nhấp đúp vào biểu tượng **`Video to ASCII Player`** trên Desktop.
2. Bảng điều khiển trực quan sẽ xuất hiện:
   - 📂 **Chọn Video:** Chọn bất kỳ video nào trên máy tính (`.mp4`, `.mkv`, `.avi`,...).
   - 🎨 **Chế độ màu:** Chọn *Màu sắc TrueColor*, *Hacker Matrix (Xanh neon)*, hoặc *Đen trắng cổ điển*.
   - ⚙️ **Tùy chọn bổ sung:** Tích chọn *Bật âm thanh*, *Bộ 70 ký tự siêu chi tiết*.
3. Bấm **`▶ BẮT ĐẦU PHÁT VIDEO (OK)`** 👉 Cửa sổ chiếu video sẽ bật lên và phát video ngay lập tức!

---

### 🎯 2. Kéo thả video (Windows):
- Giữ chuột kéo file video bất kỳ **thả thẳng vào file `Play_ASCII.bat`** để chiếu ngay lập tức.

---

### 💻 3. Chạy qua dòng lệnh (Terminal):
```bash
# Mở bảng chọn video và chế độ tương tác ngay trong terminal
python3 ascii_player.py

# Hoặc mở bảng điều khiển GUI tích chọn:
python3 gui_launcher.py

# Hoặc phát trực tiếp video chỉ định:
python3 ascii_player.py "duong_dan_video.mp4" --direct --color
```

---

## ✨ Tính năng nổi bật

- 🖥️ **Đa nền tảng (Cross-Platform):** Hỗ trợ Windows, macOS và mọi bản phân phối Linux.
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
├── Cai_Dat_Icon.bat            # Cài đặt 1-Click trên Windows
├── install.sh                  # Cài đặt 1-Click trên macOS và Linux
├── icon.ico                    # Biểu tượng ứng dụng
├── gui_launcher.py             # Bảng điều khiển GUI tích chọn chế độ
├── create_desktop_shortcut.ps1 # Script hỗ trợ tạo shortcut trên Windows
├── Play_ASCII.bat              # Chạy nhanh trên Windows
├── ascii_player.py             # Động cơ chính xử lý video sang ASCII
├── run.ps1                     # Script hỗ trợ chạy trên PowerShell
├── demo.mp4                    # Video mẫu kiểm tra
├── requirements.txt            # Danh sách thư viện Python cần thiết
├── .gitignore                  # Tệp cấu hình bỏ qua của Git
├── .github/workflows/          # Tự động đóng gói phát hành Release trên GitHub
└── README.md                   # Hướng dẫn sử dụng dự án
```

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
