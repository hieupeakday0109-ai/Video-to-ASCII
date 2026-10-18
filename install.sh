#!/usr/bin/env bash
# ==============================================================================
# Script cài đặt 1-Click cho macOS và Linux (Video to ASCII Player)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================"
echo "  🎬 CÀI ĐẶT VIDEO TO ASCII PLAYER (macOS / Linux)    "
echo "======================================================"
echo ""

# 1. Kiểm tra Python 3
if ! command -v python3 &>/dev/null; then
    echo "[!] Không tìm thấy Python 3 trên máy tính của bạn."
    echo "    Vui lòng cài đặt Python 3 trước khi tiếp tục."
    exit 1
fi

echo "[*] Đang kiểm tra và cài đặt các thư viện cần thiết..."
python3 -m pip install -r requirements.txt --quiet || python3 -m pip install -r requirements.txt

# Cấp quyền thực thi cho các script
chmod +x "$SCRIPT_DIR/ascii_player.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/gui_launcher.py" 2>/dev/null || true

DESKTOP="$HOME/Desktop"

# 2. Xử lý cho macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "[*] Phát hiện hệ điều hành: macOS"
    if [ -d "$DESKTOP" ]; then
        LAUNCHER="$DESKTOP/Video to ASCII.command"
        cat << 'EOF' > "$LAUNCHER"
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Tìm thư mục gốc của dự án nếu file shortcut nằm ngoài Desktop
PROJECT_DIR="$DIR"
if [ ! -f "$PROJECT_DIR/gui_launcher.py" ]; then
EOF
        echo "PROJECT_DIR=\"$SCRIPT_DIR\"" >> "$LAUNCHER"
        cat << 'EOF' >> "$LAUNCHER"
fi
cd "$PROJECT_DIR"
python3 gui_launcher.py
EOF
        chmod +x "$LAUNCHER"
        echo "[+] Đã tạo biểu tượng mở nhanh ngoài màn hình chính:"
        echo "    $LAUNCHER"
    fi

# 3. Xử lý cho Linux
elif [[ "$OSTYPE" == "linux"* ]]; then
    echo "[*] Phát hiện hệ điều hành: Linux"
    if [ -d "$DESKTOP" ]; then
        DESKTOP_ENTRY="$DESKTOP/video-to-ascii.desktop"
        cat << EOF > "$DESKTOP_ENTRY"
[Desktop Entry]
Version=1.0
Type=Application
Name=Video to ASCII Player
Comment=Phát video bằng ký tự ASCII trên Terminal
Exec=python3 "$SCRIPT_DIR/gui_launcher.py"
Icon=$SCRIPT_DIR/icon.ico
Path=$SCRIPT_DIR
Terminal=false
Categories=AudioVideo;Player;
EOF
        chmod +x "$DESKTOP_ENTRY"
        # Tin tưởng desktop file trên GNOME / Ubuntu nếu có gio
        if command -v gio &>/dev/null; then
            gio set "$DESKTOP_ENTRY" metadata::trusted true 2>/dev/null || true
        fi
        echo "[+] Đã tạo biểu tượng mở nhanh ngoài màn hình chính:"
        echo "    $DESKTOP_ENTRY"
    fi
fi

echo ""
echo "======================================================"
echo "  🎉 CÀI ĐẶT HOÀN TẤT!"
echo "  Bạn có thể khởi động ứng dụng bằng cách:"
echo "    - Mở biểu tượng trên màn hình Desktop"
echo "    - Hoặc chạy lệnh: python3 gui_launcher.py"
echo "======================================================"
echo ""
read -p "👉 Bạn có muốn mở ứng dụng ngay bây giờ không? (Y/n): " choice
if [[ "$choice" != "n" && "$choice" != "N" ]]; then
    python3 "$SCRIPT_DIR/gui_launcher.py" &
fi
