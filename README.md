# Video to ASCII Player (PowerShell / Windows Terminal)

Chương trình chuyển đổi và phát video trực tiếp trong **PowerShell**, **Command Prompt** hoặc **Windows Terminal** bằng các ký tự văn bản ASCII với hệ thống **bảng chọn video & chế độ phát hoàn toàn trong Terminal** (không dùng cửa sổ pop-up).

---

## ⚡ Thao tác siêu tốc 100% trong Terminal

### 🖱️ Cách 1: Kéo & thả video vào `Play_ASCII.bat` (Nhanh nhất)
- Giữ chuột kéo file video (`.mp4`, `.mkv`, `.avi`,...) **thả thẳng vào file `Play_ASCII.bat`**.
- Bảng chọn chế độ sẽ hiện ra trong terminal 👉 Bấm **Enter** là chạy ngay!

### 💻 Cách 2: Chạy trực tiếp `Play_ASCII.bat` hoặc lệnh `python`
1. Nhấp đúp vào **`Play_ASCII.bat`** (hoặc gõ `python ascii_player.py` trong PowerShell).
2. Chương trình sẽ tự quét và hiển thị **Bảng danh sách video có sẵn** ngay trên màn hình:
   ```text
   ====================================================================
             🎬 VIDEO TO ASCII - BẢNG CHỌN VIDEO TRỰC TIẾP 🎬
   ====================================================================
    Danh sách video tìm thấy trong thư mục:
      [1] demo.mp4                         (73.2 KB) [MẶC ĐỊNH]
      [2] my_video.mp4                     (15.4 MB)
   ────────────────────────────────────────────────────────────────────
    👉 Nhập số [1-2] (hoặc bấm [Enter] để chọn số [1])
    👉 Hoặc KÉO THẢ bất kỳ file video nào vào đây rồi bấm Enter
   ====================================================================
   ```
3. Sau khi chọn video, bảng **chọn chế độ phát** sẽ hiện ra:
   - **[1]** 🎨 Màu sắc TrueColor (RGB sống động, sắc nét) - *[Mặc định]*
   - **[2]** 📺 Đen trắng cổ điển (Monochrome ASCII)
   - **[3]** 🟢 Phong cách Hacker Matrix (Xanh Neon Cyberpunk)
   - **[4]** 💎 Siêu chi tiết Full HD (Bộ ký tự mở rộng 70 ký tự)
   - **[5]** 🔇 Chế độ im lặng (Tắt tiếng)
4. 👉 Chỉ cần bấm **Enter** để chạy chế độ đẹp nhất!

---

## ✨ Tính năng nổi bật

- 🖥️ **Giao diện 100% Terminal:** Không bật bất kỳ cửa sổ pop-up/panel nào, tất cả đều hiển thị thành bảng đẹp mắt ngay trong PowerShell.
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

> **Mẹo:** Nhấn tổ hợp phím `Ctrl + C` bất cứ lúc nào để dừng phát video.

---

## 📄 Giấy phép
Dự án được phát hành dưới giấy phép MIT.
