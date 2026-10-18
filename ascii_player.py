import sys
import os
import time
import argparse
import shutil
import subprocess

try:
    import cv2
    import numpy as np
except ImportError:
    print("\n[!] Thiếu thư viện OpenCV hoặc NumPy. Vui lòng cài đặt bằng lệnh:")
    print("    pip install opencv-python numpy\n")
    sys.exit(1)

# Bảng ký tự ASCII theo độ sáng tăng dần (từ tối đến sáng)
ASCII_RAMP_SIMPLE = " .:-=+*#%@"
ASCII_RAMP_DETAILED = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def play_video(video_path, color=False, detailed=False, with_audio=True):
    if not os.path.isfile(video_path):
        print(f"[-] Không tìm thấy tệp video: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[-] Không thể mở video: {video_path}")
        return

    # Lấy thông số video
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps > 120 or np.isnan(fps):
        fps = 30.0
    frame_delay = 1.0 / fps

    ramp = ASCII_RAMP_DETAILED if detailed else ASCII_RAMP_SIMPLE
    ramp_chars = np.array(list(ramp))
    num_chars = len(ramp)

    # Tỷ lệ hiển thị ký tự (trong terminal, ký tự thường cao gấp đôi bề ngang)
    CHAR_ASPECT_RATIO = 0.5

    # Ẩn con trỏ và xóa màn hình một lần duy nhất
    sys.stdout.write("\x1b[?25l\x1b[2J")
    sys.stdout.flush()

    # Phát âm thanh nền đồng bộ bằng ffplay nếu có sẵn
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

            # Lấy kích thước terminal hiện tại
            term_cols, term_lines = shutil.get_terminal_size(fallback=(80, 24))
            max_w = term_cols
            max_h = term_lines - 1  # Để lại 1 dòng tránh tràn màn hình gây scroll

            h, w = frame.shape[:2]
            aspect = (w / h) / CHAR_ASPECT_RATIO

            # Tính toán kích thước frame hiển thị vừa vặn với kích thước terminal
            target_w = max_w
            target_h = int(target_w / aspect)

            if target_h > max_h:
                target_h = max_h
                target_w = int(target_h * aspect)

            target_w = max(1, target_w)
            target_h = max(1, target_h)

            resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

            if color:
                # Chế độ màu TrueColor ANSI (\x1b[38;2;R;G;Bm)
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
                # Chế độ đen trắng (ASCII cổ điển, siêu mượt và nhẹ)
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                indices = ((gray.astype(np.float32) / 255.0) * (num_chars - 1)).astype(np.int32)
                char_grid = ramp_chars[indices]
                output_lines = ["".join(row) for row in char_grid]
                buffer = "\x1b[H" + "\n".join(output_lines)

            # In frame lên màn hình mà không nhấp nháy
            sys.stdout.write(buffer)
            sys.stdout.flush()

            # Giữ nhịp FPS chính xác để đồng bộ âm thanh
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
        # Hiện lại con trỏ chuột và reset màu sắc
        sys.stdout.write("\x1b[?25h\x1b[0m\n")
        sys.stdout.flush()
        print("\n[+] Đã kết thúc phát video.")

def main():
    parser = argparse.ArgumentParser(
        description="Trình phát video bằng ký tự ASCII trên PowerShell / Terminal."
    )
    parser.add_argument("video", help="Đường dẫn đến file video (mp4, mkv, avi, webm, ...)")
    parser.add_argument("--color", "-c", action="store_true", help="Bật màu ANSI TrueColor")
    parser.add_argument("--detailed", "-d", action="store_true", help="Dùng bộ ký tự chi tiết hơn")
    parser.add_argument("--no-audio", action="store_true", help="Tắt âm thanh")

    args = parser.parse_args()
    play_video(args.video, color=args.color, detailed=args.detailed, with_audio=not args.no_audio)

if __name__ == "__main__":
    main()
