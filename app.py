import sys
import os

# Xác định thư mục cơ sở khi đóng gói hoặc chạy mã nguồn
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    # Nếu có tham số dòng lệnh hoặc video được kéo thả vào file exe
    # thì chạy ngay trình phát video ASCII trong console
    is_cli = len(sys.argv) > 1 and sys.argv[1] not in ("--gui", "-g")

    if is_cli:
        from ascii_player import main as run_player
        try:
            run_player()
        except Exception as e:
            print(f"\n[!] Lỗi: {e}")
            try:
                input("\n👉 Nhấn Enter để đóng...")
            except Exception:
                pass
    else:
        # Nếu click đúp mở file exe thì mở bảng điều khiển GUI
        from gui_launcher import main as run_gui
        run_gui()

if __name__ == "__main__":
    main()
