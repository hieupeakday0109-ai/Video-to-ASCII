# 🎬 Video to ASCII Player (Cyberpunk Desktop App)

<p align="center">
  <img src="https://img.shields.io/github/v/release/hieupeakday0109-ai/Video-to-ASCII?color=brightgreen&label=Release&style=for-the-badge" alt="Release" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/FPS-60%20Buttery%20Smooth-success?style=for-the-badge" alt="FPS" />
  <img src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge" alt="License" />
</p>

Ứng dụng xem video phong cách ký tự **ASCII Cyberpunk** thế hệ mới dành cho máy tính. Giao diện Desktop hiện đại, mượt mà chuẩn **60 FPS**, hỗ trợ kéo thả video trực tiếp, đồng bộ âm thanh, thanh tua tiến độ thời gian thực và chuyển đổi chế độ màu sắc tức thì chỉ với một cú nhấp chuột!

---

## 🚀 Tải về bản chạy ngay (Không cần cài đặt Python)

Tải file chạy độc lập (**Standalone Executable**) trực tiếp tại trang:  
👉 **[GitHub Releases - Video to ASCII Player](https://github.com/hieupeakday0109-ai/Video-to-ASCII/releases)**

| Hệ điều hành | File tải về | Hướng dẫn nhanh |
| :--- | :--- | :--- |
| **🪟 Windows** | **`VideoToASCII-Windows.exe`** | Nhấp đúp chuột để mở ứng dụng, hoặc kéo thả file video thẳng vào file `.exe`! |
| **🍎 macOS** | **`VideoToASCII-macOS`** | Cấp quyền `chmod +x VideoToASCII-macOS` và nhấp đúp hoặc chạy `./VideoToASCII-macOS` |
| **🐧 Linux** | **`VideoToASCII-Linux`** | Cấp quyền `chmod +x VideoToASCII-Linux` và chạy `./VideoToASCII-Linux` |

---

## ✨ Điểm nổi bật của phiên bản App mới

- 🖥️ **Giao diện Desktop hiện đại (Native GUI):** Không còn chạy qua cửa sổ Command Prompt / Terminal đen sì giật lag. Video được render trực tiếp trong cửa sổ ứng dụng đồ họa chuyên nghiệp.
- ⚡ **Tốc độ khung hình 60 FPS mượt mà:** Ứng dụng công nghệ **NumPy + OpenCV Glyph Atlas Vectorization**, kết hợp phần cứng tăng tốc giúp chuyển đổi và hiển thị hàng ngàn ký tự ASCII trong tích tắc mà không hề bị xé hình hay giật lag.
- 🎨 **Đa dạng phong cách hiển thị:**
  - **Màu sắc TrueColor (RGB):** Tái hiện màu sắc trung thực theo từng pixel của video gốc.
  - **Phong cách Hacker Matrix:** Tông màu xanh neon đặc trưng của thế giới Cyberpunk huyền thoại.
  - **Đen trắng cổ điển (Monochrome):** Đồ họa ASCII hoài niệm phong cách máy tính thập niên 80.
- 🖱️ **Kéo thả thông minh (Drag & Drop):** Giữ chuột kéo bất kỳ video nào (`.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`,...) thả vào cửa sổ ứng dụng là phát ngay lập tức.
- ⏩ **Thanh tua tiến độ thời gian thực (Scrubber Timeline):** Dễ dàng nhấp hoặc kéo con trỏ trên thanh timeline để tua đến bất kỳ giây nào của video.
- 🔊 **Âm thanh nền đồng bộ:** Tự động phát âm thanh video khớp từng khung hình, hỗ trợ tạm dừng và tua cùng lúc với hình ảnh.
- 🖥️ **Chế độ toàn màn hình (Fullscreen):** Nhấn `F11` để tận hưởng trải nghiệm chiếu video ASCII toàn màn hình cực kỳ ấn tượng.

---

## ⌨️ Bảng phím tắt tiện lợi (Hotkeys)

| Phím tắt | Chức năng |
| :--- | :--- |
| **`Space`** | Tạm dừng / Tiếp tục phát video (Play / Pause) |
| **`1`** | Chuyển sang chế độ **Màu sắc TrueColor (RGB)** |
| **`2`** | Chuyển sang chế độ **Hacker Matrix (Xanh neon)** |
| **`3`** | Chuyển sang chế độ **Đen trắng (Monochrome)** |
| **`D`** | Chuyển đổi giữa bộ **70 ký tự siêu nét** và **10 ký tự cơ bản** |
| **`M`** | Bật / Tắt âm thanh (Mute / Unmute) |
| **`←` / `→`** | Tua lùi / Tua tiến 5 giây |
| **`F11`** | Bật / Tắt chế độ toàn màn hình (Fullscreen) |
| **`Esc`** | Thoát toàn màn hình hoặc đóng ứng dụng |

---

## ⚡ Hướng dẫn cài đặt bằng mã nguồn (Dành cho lập trình viên)

### 🪟 Trên Windows:
1. Tải toàn bộ mã nguồn về máy hoặc clone qua Git:
   ```bash
   git clone https://github.com/hieupeakday0109-ai/Video-to-ASCII.git
   ```
2. Nhấp đúp vào file **`Cai_Dat_Icon.bat`**.
3. Chương trình sẽ tự động cài thư viện và tạo biểu tượng **`Video to ASCII Player`** ra ngoài màn hình chính (Desktop).

### 🍎 Trên macOS & 🐧 Linux:
1. Mở Terminal tại thư mục dự án và chạy:
   ```bash
   bash install.sh
   ```
2. Script sẽ tự cài đặt thư viện và tạo biểu tượng mở nhanh ngay trên Desktop của bạn!

---

## 🛠️ Cấu trúc thư mục

```text
Video-to-ASCII/
│
├── app.py                      # Điểm khởi chạy chính của ứng dụng
├── player_gui.py               # Ứng dụng Desktop Player đồ họa 60 FPS
├── ascii_player.py             # Động cơ dự phòng cho dòng lệnh (CLI Terminal)
├── Cai_Dat_Icon.bat            # Trình cài đặt tự động 1-Click trên Windows
├── install.sh                  # Trình cài đặt tự động 1-Click trên macOS & Linux
├── icon.ico                    # Biểu tượng ứng dụng
├── Play_ASCII.bat              # Script chạy nhanh ứng dụng trên Windows
├── requirements.txt            # Danh sách thư viện Python cần thiết
├── .github/workflows/          # Quy trình tự động đóng gói release đa nền tảng
└── README.md                   # Hướng dẫn chi tiết sử dụng dự án
```

---

## 📄 Giấy phép (License)
Dự án được phân phối miễn phí mã nguồn mở dưới giấy phép [MIT License](LICENSE).
