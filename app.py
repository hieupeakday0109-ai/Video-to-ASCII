import sys
import os

# Xác định thư mục cơ sở khi đóng gói hoặc chạy mã nguồn
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    args = sys.argv[1:]

    # Nếu người dùng truyền cờ --cli hoặc --terminal thì mới chạy giao diện dòng lệnh cũ
    if "--cli" in args or "--terminal" in args:
        from ascii_player import main as run_cli
        try:
            run_cli()
        except Exception as e:
            print(f"\n[!] Lỗi: {e}")
            try:
                input("\n👉 Nhấn Enter để đóng...")
            except Exception:
                pass
        return

    # Mặc định: Mở ứng dụng Desktop Player hiện đại (60 FPS, không dùng CMD)
    # Nếu có truyền file video (hoặc kéo thả video vào file exe) thì phát luôn
    video_file = None
    for arg in args:
        if not arg.startswith("-") and os.path.isfile(arg):
            video_file = arg
            break

    from player_gui import main as run_app
    run_app(video_file)

if __name__ == "__main__":
    main()
