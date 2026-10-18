import sys
import os
import time
import argparse
import shutil
import subprocess

# Kiểm tra thư viện phụ thuộc
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

def select_file_gui():
    """Mở hộp thoại chọn tệp của Windows để người dùng không phải gõ lệnh"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính của Tkinter
        root.attributes("-topmost", True)  # Đưa cửa sổ chọn tệp lên trên cùng
        file_path = filedialog.askopenfilename(
            title="Chọn file video bạn muốn phát",
            filetypes=[
                ("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm"),
                ("All Files", "*.*")
            ]
        )
        root.destroy()
        if file_path and os.path.isfile(file_path):
            return file_path
    except Exception:
        pass
    return None

def prompt_video_input():
    """Cho phép kéo thả video vào cửa sổ terminal hoặc mở cửa sổ chọn tệp"""
    print("=" * 60)
    print("   🎬 TRÌNH PHÁT VIDEO KÝ TỰ ASCII CHO POWERSHELL / TERMINAL 🎬")
    print("=" * 60)

    # Thử mở cửa sổ chọn file
    print("[*] Đang mở cửa sổ chọn file video (hoặc bạn có thể kéo thả vào đây)...")
    selected = select_file_gui()
    if selected:
        return selected

    # Nếu tắt cửa sổ chọn file thì cho phép kéo thả trực tiếp
    while True:
        user_input = input("\n👉 KÉO THẢ file video vào đây rồi nhấn Enter (hoặc 'q' để thoát): ").strip()
        if user_input.lower() == 'q':
            sys.exit(0)
        
        # Xóa dấu nháy kép / nháy đơn mà Windows tự thêm khi kéo thả file
        cleaned_path = user_input.strip("\"' ")
        if os.path.isfile(cleaned_path):
            return cleaned_path
        elif os.path.isfile("demo.mp4") and user_input == "":
            print("[*] Tự động chọn video mẫu demo.mp4")
            return "demo.mp4"
        else:
            print("[-] Không tìm thấy file video hợp lệ. Vui lòng thử lại!")

def play_video(video_path, color=True, detailed=False, with_audio=True):
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

    # Tỷ lệ hiển thị ký tự (chiều cao ký tự terminal gấp đôi bề ngang)
    CHAR_ASPECT_RATIO = 0.5

    # Ẩn con trỏ chuột và xóa màn hình
    sys.stdout.write("\x1b[?25l\x1b[2J")
    sys.stdout.flush()

    # Tự động đồng bộ âm thanh nền bằng ffplay nếu có
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

            # Lấy kích thước hiện tại của cửa sổ terminal
            term_cols, term_lines = shutil.get_terminal_size(fallback=(80, 24))
            max_w = term_cols
            max_h = term_lines - 1  # Để lại 1 dòng tránh cuộn màn hình

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

            if color:
                # Chế độ màu sắc ANSI TrueColor (siêu đẹp)
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
                # Chế độ đen trắng (ASCII cổ điển, siêu nhẹ)
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                indices = ((gray.astype(np.float32) / 255.0) * (num_chars - 1)).astype(np.int32)
                char_grid = ramp_chars[indices]
                output_lines = ["".join(row) for row in char_grid]
                buffer = "\x1b[H" + "\n".join(output_lines)

            # In đè lên màn hình mà không chớp nháy
            sys.stdout.write(buffer)
            sys.stdout.flush()

            # Giữ đúng FPS
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

def main():
    parser = argparse.ArgumentParser(
        description="Trình phát video bằng ký tự ASCII trên PowerShell / Terminal."
    )
    parser.add_argument("video", nargs="?", default=None, help="Đường dẫn đến file video")
    parser.add_argument("--mono", action="store_true", help="Chạy chế độ đen trắng (mặc định là có màu)")
    parser.add_argument("--detailed", "-d", action="store_true", help="Dùng bộ ký tự chi tiết hơn")
    parser.add_argument("--no-audio", action="store_true", help="Tắt âm thanh")

    args = parser.parse_args()

    # Nếu người dùng không nhập tham số gì, mở giao diện chọn file / kéo thả
    video_path = args.video
    if not video_path:
        video_path = prompt_video_input()

    play_video(
        video_path=video_path,
        color=not args.mono,
        detailed=args.detailed,
        with_audio=not args.no_audio
    )

if __name__ == "__main__":
    main()
