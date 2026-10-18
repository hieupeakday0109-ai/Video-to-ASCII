import sys
import os
import time
import argparse
import shutil
import subprocess

# Kích hoạt chế độ mã màu ANSI trên Windows Console
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        hOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
            kernel32.SetConsoleMode(hOut, mode.value | 0x0004)
    except Exception:
        pass
    os.system("")

# Tự động kiểm tra và cài đặt thư viện nếu thiếu
try:
    import cv2
    import numpy as np
except ImportError:
    print("\n[!] Đang thiếu thư viện OpenCV hoặc NumPy.")
    print("    Đang tự động cài đặt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])
    import cv2
    import numpy as np

# Bảng ký tự ASCII theo độ sáng tăng dần
ASCII_RAMP_SIMPLE = " .:-=+*#%@"
ASCII_RAMP_DETAILED = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".ts", ".m4v"}

def get_format_size(size_in_bytes):
    """Chuyển đổi kích thước file sang KB, MB dễ đọc"""
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    return f"{size_in_bytes / (1024 * 1024):.1f} MB"

def scan_local_videos():
    """Tìm tất cả các file video trong thư mục hiện tại và thư mục của mã nguồn"""
    dirs_to_check = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    found_videos = []
    seen_paths = set()

    for d in dirs_to_check:
        if not os.path.isdir(d):
            continue
        try:
            for item in os.listdir(d):
                full_path = os.path.join(d, item)
                if os.path.isfile(full_path):
                    _, ext = os.path.splitext(item)
                    if ext.lower() in VIDEO_EXTENSIONS and full_path not in seen_paths:
                        seen_paths.add(full_path)
                        found_videos.append(full_path)
        except Exception:
            pass

    found_videos.sort(key=lambda p: os.path.basename(p).lower())
    return found_videos

def prompt_video_terminal_menu():
    """Bảng menu chọn video trực tiếp trong PowerShell, không mở cửa sổ pop-up/panel"""
    CYAN = "\x1b[36;1m"
    GREEN = "\x1b[32;1m"
    YELLOW = "\x1b[33;1m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"

    while True:
        videos = scan_local_videos()

        print("\n" + "=" * 68)
        print(f"{CYAN}          🎬 VIDEO TO ASCII - BẢNG CHỌN VIDEO TRỰC TIẾP 🎬{RESET}")
        print("=" * 68)

        if videos:
            print(f" {BOLD}Danh sách video tìm thấy trong thư mục:{RESET}")
            for idx, vid in enumerate(videos, start=1):
                name = os.path.basename(vid)
                try:
                    size = get_format_size(os.path.getsize(vid))
                except Exception:
                    size = "Unknown"
                default_tag = f" {CYAN}[MẶC ĐỊNH]{RESET}" if idx == 1 else ""
                print(f"   {GREEN}[{idx}]{RESET} {YELLOW}{name:<32}{RESET} ({size}){default_tag}")
            print("─" * 68)
            print(f" 👉 Nhập số {BOLD}[1-{len(videos)}]{RESET} (hoặc bấm {GREEN}[Enter]{RESET} để chọn số [1])")
        else:
            print(f" {YELLOW}[!] Chưa có sẵn file video nào trong thư mục này.{RESET}")
            print("─" * 68)

        print(f" 👉 Hoặc {BOLD}KÉO THẢ{RESET} bất kỳ file video nào vào đây rồi bấm {GREEN}Enter{RESET}")
        print("=" * 68)

        user_input = input(" 📁 Nhập lựa chọn của bạn: ").strip()

        if user_input.lower() in {"q", "exit", "quit"}:
            sys.exit(0)

        if user_input == "" and videos:
            return videos[0]

        if user_input.isdigit():
            choice_num = int(user_input)
            if 1 <= choice_num <= len(videos):
                return videos[choice_num - 1]
            else:
                print(f"\n[-] Số {choice_num} không có trong danh sách. Vui lòng chọn lại!")
                continue

        cleaned_path = user_input.strip("\"' ")
        if os.path.isfile(cleaned_path):
            return os.path.abspath(cleaned_path)

        print("\n[-] Không tìm thấy file video hợp lệ. Vui lòng thử lại!")

def show_mode_menu(video_path):
    """Bảng menu tương tác đẹp mắt cho phép người dùng chọn chế độ phát"""
    file_name = os.path.basename(video_path)
    
    CYAN = "\x1b[36;1m"
    GREEN = "\x1b[32;1m"
    YELLOW = "\x1b[33;1m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"

    print("\n" + "=" * 68)
    print(f"{CYAN}       🎬 VIDEO TO ASCII PLAYER - BẢNG ĐIỀU KHIỂN CHẾ ĐỘ 🎬{RESET}")
    print("=" * 68)
    print(f" 📁 Video đang chọn: {YELLOW}{file_name}{RESET}")
    print("─" * 68)
    print(f" {GREEN}[1]{RESET} {BOLD}🎨 Màu sắc TrueColor{RESET} (RGB sống động, sắc nét)    {CYAN}[MẶC ĐỊNH]{RESET}")
    print(f" {GREEN}[2]{RESET} {BOLD}📺 Đen trắng cổ điển{RESET} (Classic ASCII Monochrome)")
    print(f" {GREEN}[3]{RESET} {BOLD}🟢 Phong cách Hacker Matrix{RESET} (Xanh Neon Cyberpunk)")
    print(f" {GREEN}[4]{RESET} {BOLD}💎 Siêu chi tiết Full HD{RESET} (Bộ ký tự mở rộng 70 ký tự)")
    print(f" {GREEN}[5]{RESET} {BOLD}🔇 Chế độ im lặng{RESET} (Phát không tiếng / Mute)")
    print("─" * 68)
    
    choice = input(f" 👉 Nhấn {GREEN}[Enter]{RESET} để chạy chế độ [1], hoặc nhập {BOLD}[1-5]{RESET}: ").strip()
    
    if choice == "2":
        return {"color": False, "detailed": False, "matrix": False, "with_audio": True}
    elif choice == "3":
        return {"color": False, "detailed": False, "matrix": True, "with_audio": True}
    elif choice == "4":
        return {"color": True, "detailed": True, "matrix": False, "with_audio": True}
    elif choice == "5":
        return {"color": True, "detailed": False, "matrix": False, "with_audio": False}
    else:
        return {"color": True, "detailed": False, "matrix": False, "with_audio": True}

def play_video(video_path, color=True, detailed=False, matrix=False, with_audio=True):
    video_path = os.path.abspath(video_path)
    if not os.path.isfile(video_path):
        print(f"[-] Không tìm thấy tệp video: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[-] Không thể mở video: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps > 120 or np.isnan(fps):
        fps = 30.0
    frame_delay = 1.0 / fps

    ramp = ASCII_RAMP_DETAILED if detailed else ASCII_RAMP_SIMPLE
    ramp_chars = np.array(list(ramp))
    num_chars = len(ramp)

    CHAR_ASPECT_RATIO = 0.5

    # Ẩn con trỏ chuột và xóa màn hình
    sys.stdout.write("\x1b[?25l\x1b[2J")
    sys.stdout.flush()

    audio_proc = None
    if with_audio and shutil.which("ffplay"):
        try:
            audio_proc = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", video_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    start_time = time.time()
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            term_cols, term_lines = shutil.get_terminal_size(fallback=(80, 24))
            max_w = term_cols
            max_h = term_lines - 1

            h, w = frame.shape[:2]
            aspect = (w / h) / CHAR_ASPECT_RATIO

            target_w = max_w
            target_h = int(target_w / aspect)

            if target_h > max_h:
                target_h = max_h
                target_w = int(target_h * aspect)

            target_w = max(1, target_w)
            target_h = max(1, target_h)

            resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

            if matrix:
                # Chế độ Matrix Hacker: Xanh lá neon theo độ sáng
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                indices = ((gray.astype(np.float32) / 255.0) * (num_chars - 1)).astype(np.int32)
                char_grid = ramp_chars[indices]

                output_lines = []
                for row_idx in range(target_h):
                    line_parts = []
                    row_gray = gray[row_idx]
                    row_chars = char_grid[row_idx]
                    for col_idx in range(target_w):
                        val = row_gray[col_idx]
                        ch = row_chars[col_idx]
                        r = int(val * 0.15)
                        g = val
                        b = int(val * 0.25)
                        line_parts.append(f"\x1b[38;2;{r};{g};{b}m{ch}")
                    output_lines.append("".join(line_parts) + "\x1b[0m")
                buffer = "\x1b[H" + "\n".join(output_lines)

            elif color:
                # Chế độ màu TrueColor RGB
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                indices = ((gray.astype(np.float32) / 255.0) * (num_chars - 1)).astype(np.int32)
                char_grid = ramp_chars[indices]

                output_lines = []
                for row_idx in range(target_h):
                    line_parts = []
                    row_chars = char_grid[row_idx]
                    row_rgb = rgb[row_idx]
                    for col_idx in range(target_w):
                        r, g, b = row_rgb[col_idx]
                        ch = row_chars[col_idx]
                        line_parts.append(f"\x1b[38;2;{r};{g};{b}m{ch}")
                    output_lines.append("".join(line_parts) + "\x1b[0m")
                buffer = "\x1b[H" + "\n".join(output_lines)
            else:
                # Chế độ đen trắng cổ điển
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                indices = ((gray.astype(np.float32) / 255.0) * (num_chars - 1)).astype(np.int32)
                char_grid = ramp_chars[indices]
                output_lines = ["".join(row) for row in char_grid]
                buffer = "\x1b[H" + "\n".join(output_lines)

            sys.stdout.write(buffer)
            sys.stdout.flush()

            target_time = start_time + (frame_count * frame_delay)
            sleep_duration = target_time - time.time()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if audio_proc:
            try:
                audio_proc.terminate()
            except Exception:
                pass
        sys.stdout.write("\x1b[?25h\x1b[0m\n")
        sys.stdout.flush()
        print("\n[+] Đã kết thúc phát video.")
        try:
            input("\n👉 Nhấn Enter để đóng cửa sổ...")
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(
        description="Trình phát video bằng ký tự ASCII trên PowerShell / Terminal."
    )
    parser.add_argument("video", nargs="?", default=None, help="Đường dẫn đến file video")
    parser.add_argument("--color", "-c", action="store_true", help="Chế độ màu TrueColor")
    parser.add_argument("--mono", "-m", action="store_true", help="Chế độ đen trắng")
    parser.add_argument("--matrix", action="store_true", help="Chế độ Matrix Green")
    parser.add_argument("--detailed", "-d", action="store_true", help="Dùng bộ ký tự chi tiết hơn")
    parser.add_argument("--no-audio", action="store_true", help="Tắt âm thanh")
    parser.add_argument("--direct", action="store_true", help="Chạy thẳng không hỏi lại menu")
    parser.add_argument("--menu", action="store_true", help="Luôn hiển thị menu chọn chế độ")

    args = parser.parse_args()

    # 1. Chọn video (bằng menu dòng lệnh nếu chưa có)
    video_path = args.video
    interactive = False
    if not video_path:
        video_path = prompt_video_terminal_menu()
        interactive = True

    # 2. Quyết định chế độ phát:
    # Nếu có cờ --direct hoặc bất kỳ cờ chế độ nào, phát trực tiếp ngay lập tức!
    has_flags = args.direct or args.color or args.mono or args.matrix or args.detailed or args.no_audio

    if args.menu or (interactive and not has_flags) or (not has_flags and not args.direct):
        settings = show_mode_menu(video_path)
        play_video(
            video_path=video_path,
            color=settings["color"],
            detailed=settings["detailed"],
            matrix=settings["matrix"],
            with_audio=settings["with_audio"]
        )
    else:
        play_video(
            video_path=video_path,
            color=not args.mono and not args.matrix,
            detailed=args.detailed,
            matrix=args.matrix,
            with_audio=not args.no_audio
        )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] Có lỗi xảy ra trong quá trình phát video:\n{e}")
        try:
            input("\n👉 Nhấn Enter để thoát...")
        except Exception:
            pass
