import sys
import os
import time
import shutil
import tempfile
import subprocess
import threading
import numpy as np
import cv2
import pygame

# Ẩn cửa sổ Tkinter gốc khi dùng hộp thoại chọn file
import tkinter as tk
from tkinter import filedialog

CHAR_SET_70 = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
CHAR_SET_10 = " .:-=+*#%@"

class AsciiVideoPlayerApp:
    def __init__(self, initial_video=None):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)

        # Cửa sổ ứng dụng
        self.width = 1100
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("🎬 Video to ASCII Player - Cyberpunk Edition")

        # Cài đặt Icon
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "icon.ico")
        if os.path.exists(icon_path):
            try:
                icon_surf = pygame.image.load(icon_path)
                pygame.display.set_icon(icon_surf)
            except Exception:
                pass

        # Font giao diện & font ký tự ASCII
        self.font_name = "Consolas"
        self.ascii_font_size = 14
        self.setup_fonts()

        # Tạo Glyph Atlas (cho cả bộ 70 ký tự và 10 ký tự)
        self.atlas_70 = self.build_glyph_atlas(CHAR_SET_70)
        self.atlas_10 = self.build_glyph_atlas(CHAR_SET_10)

        # Trạng thái người dùng
        self.mode = "color"          # "color", "matrix", "mono"
        self.detailed = True         # True (70 chars), False (10 chars)
        self.with_audio = True       # True / False
        self.is_playing = False
        self.is_fullscreen = False

        # Quản lý video
        self.video_path = None
        self.cap = None
        self.total_frames = 0
        self.fps = 30.0
        self.duration = 0.0
        self.current_frame_idx = 0
        self.video_w = 0
        self.video_h = 0
        self.temp_audio_file = None
        self.audio_loaded = False

        # Đồng bộ thời gian
        self.start_play_time = 0.0
        self.start_frame_idx = 0

        # UI & Kéo thả
        self.is_scrubbing = False
        self.hover_btn = None
        self.clock = pygame.time.Clock()

        # Animation trang chủ
        self.matrix_rain = self.init_matrix_rain()

        if initial_video and os.path.isfile(initial_video):
            self.load_video(initial_video)

    def setup_fonts(self):
        try:
            self.ascii_font = pygame.font.SysFont(self.font_name, self.ascii_font_size)
        except Exception:
            self.ascii_font = pygame.font.Font(None, self.ascii_font_size)

        self.ui_font = pygame.font.SysFont("Segoe UI", 13, bold=True)
        self.ui_font_small = pygame.font.SysFont("Segoe UI", 11)
        self.title_font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.gw, self.gh = self.ascii_font.size("M")
        if self.gw == 0: self.gw = 8
        if self.gh == 0: self.gh = 14

    def build_glyph_atlas(self, charset):
        masks = []
        base_surf = pygame.Surface((self.gw, self.gh), 0, 32)
        for c in charset:
            base_surf.fill((0, 0, 0))
            rendered = self.ascii_font.render(c, False, (255, 255, 255))
            base_surf.blit(rendered, (0, 0))
            arr = pygame.surfarray.array3d(base_surf)[:, :, 0].T
            masks.append((arr > 40).astype(np.uint8))
        return np.stack(masks, axis=0)  # Shape: (N, gh, gw)

    def init_matrix_rain(self):
        cols = self.width // 16
        return [{"x": i * 16, "y": np.random.randint(-500, 0), "speed": np.random.randint(3, 8), "len": np.random.randint(8, 20)} for i in range(cols)]

    def open_file_dialog(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Chọn video để phát dạng ASCII",
                filetypes=[
                    ("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm"),
                    ("All Files", "*.*")
                ]
            )
            root.destroy()
            if file_path and os.path.isfile(file_path):
                self.load_video(file_path)
        except Exception as e:
            print(f"[!] Lỗi mở hộp thoại file: {e}")

    def load_video(self, file_path):
        if self.cap:
            self.cap.release()
        pygame.mixer.music.stop()

        self.video_path = file_path
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            print(f"[!] Không thể mở video: {file_path}")
            self.cap = None
            return

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.duration = (self.total_frames / self.fps) if self.fps > 0 else 0.0
        self.video_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.current_frame_idx = 0

        # Trích xuất âm thanh nền qua ffmpeg (nếu có)
        self.extract_audio(file_path)

        # Bắt đầu phát
        self.is_playing = True
        self.start_play_time = time.perf_counter()
        self.start_frame_idx = 0

        if self.audio_loaded and self.with_audio:
            try:
                pygame.mixer.music.play()
            except Exception:
                pass

    def extract_audio(self, file_path):
        self.audio_loaded = False
        if not shutil.which("ffmpeg"):
            return

        def _do_extract():
            try:
                temp_dir = tempfile.gettempdir()
                out_wav = os.path.join(temp_dir, f"ascii_audio_{int(time.time())}.wav")
                cmd = ["ffmpeg", "-y", "-i", file_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", out_wav]
                proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000 if sys.platform == "win32" else 0)
                if proc.returncode == 0 and os.path.isfile(out_wav):
                    self.temp_audio_file = out_wav
                    pygame.mixer.music.load(out_wav)
                    self.audio_loaded = True
                    if self.is_playing and self.with_audio:
                        cur_sec = self.current_frame_idx / self.fps if self.fps > 0 else 0
                        pygame.mixer.music.play(start=cur_sec)
            except Exception as e:
                print(f"[!] Không thể trích xuất audio: {e}")

        threading.Thread(target=_do_extract, daemon=True).start()

    def seek_to_ratio(self, ratio):
        if not self.cap or self.total_frames <= 0:
            return
        ratio = max(0.0, min(1.0, ratio))
        target_frame = int(ratio * self.total_frames)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame_idx = target_frame
        self.start_frame_idx = target_frame
        self.start_play_time = time.perf_counter()

        if self.audio_loaded and self.with_audio:
            target_sec = target_frame / self.fps
            try:
                pygame.mixer.music.play(start=target_sec)
                if not self.is_playing:
                    pygame.mixer.music.pause()
            except Exception:
                pass

    def toggle_play(self):
        if not self.cap:
            return
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.start_frame_idx = self.current_frame_idx
            self.start_play_time = time.perf_counter()
            if self.audio_loaded and self.with_audio:
                try:
                    pygame.mixer.music.unpause()
                except Exception:
                    pass
        else:
            if self.audio_loaded:
                try:
                    pygame.mixer.music.pause()
                except Exception:
                    pass

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1100, 720), pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.matrix_rain = self.init_matrix_rain()

    def run(self):
        running = True
        while running:
            # 1. Xử lý sự kiện (Events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.width, self.height = event.size
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                        self.matrix_rain = self.init_matrix_rain()

                elif event.type == pygame.DROPFILE:
                    # Kéo thả file video trực tiếp vào cửa sổ ứng dụng!
                    dropped_file = event.file
                    if os.path.isfile(dropped_file):
                        self.load_video(dropped_file)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.is_fullscreen:
                            self.toggle_fullscreen()
                        else:
                            running = False
                    elif event.key == pygame.K_SPACE:
                        self.toggle_play()
                    elif event.key == pygame.K_F11 or (event.key == pygame.K_f and (event.mod & pygame.KMOD_ALT)):
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_1:
                        self.mode = "color"
                    elif event.key == pygame.K_2:
                        self.mode = "matrix"
                    elif event.key == pygame.K_3:
                        self.mode = "mono"
                    elif event.key == pygame.K_d:
                        self.detailed = not self.detailed
                    elif event.key == pygame.K_m:
                        self.with_audio = not self.with_audio
                        if not self.with_audio and self.audio_loaded:
                            pygame.mixer.music.pause()
                        elif self.with_audio and self.audio_loaded and self.is_playing:
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_LEFT:
                        if self.cap and self.fps > 0:
                            ratio = max(0.0, (self.current_frame_idx - self.fps * 5) / self.total_frames)
                            self.seek_to_ratio(ratio)
                    elif event.key == pygame.K_RIGHT:
                        if self.cap and self.fps > 0:
                            ratio = min(1.0, (self.current_frame_idx + self.fps * 5) / self.total_frames)
                            self.seek_to_ratio(ratio)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = event.pos
                        self.handle_click(mx, my)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_scrubbing = False

                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    if self.is_scrubbing:
                        self.handle_scrub(mx)

            # 2. Cập nhật Frame Video
            if self.is_playing and self.cap:
                elapsed = time.perf_counter() - self.start_play_time
                target_frame = self.start_frame_idx + int(elapsed * self.fps)

                if target_frame >= self.total_frames:
                    # Video kết thúc -> loop lại đầu
                    self.seek_to_ratio(0.0)
                else:
                    # Đọc frame nếu bị lệch quá nhiều
                    if abs(target_frame - self.current_frame_idx) > 1:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                    ret, frame = self.cap.read()
                    if ret:
                        self.current_frame = frame
                        self.current_frame_idx = target_frame
                    else:
                        self.seek_to_ratio(0.0)

            # 3. Vẽ toàn bộ giao diện
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(60)

        # Thoát dọn dẹp
        if self.cap:
            self.cap.release()
        pygame.mixer.quit()
        if self.temp_audio_file and os.path.exists(self.temp_audio_file):
            try:
                os.remove(self.temp_audio_file)
            except Exception:
                pass
        pygame.quit()

    def draw_all(self):
        # Nền tối phong cách Catppuccin Cyberpunk
        self.screen.fill((24, 24, 37))

        top_h = 52
        bottom_h = 60
        player_y = top_h
        player_h = self.height - top_h - bottom_h

        if self.cap and hasattr(self, 'current_frame') and self.current_frame is not None:
            self.draw_ascii_frame(player_y, player_h)
        else:
            self.draw_welcome_screen(player_y, player_h)

        # Vẽ thanh công cụ trên cùng & thanh điều khiển dưới cùng
        self.draw_top_bar(top_h)
        self.draw_bottom_bar(bottom_h)

    def draw_ascii_frame(self, player_y, player_h):
        player_w = self.width
        # Tính kích thước lưới ASCII dựa trên khung hình video để giữ đúng tỷ lệ
        aspect = (self.video_w / self.video_h) if self.video_h > 0 else (16 / 9)
        # Font consolas tỷ lệ cao/rộng ~ 14/8 = 1.75
        font_aspect = self.gh / self.gw

        max_cols = player_w // self.gw
        max_rows = player_h // self.gh

        # Tính cols và rows sao cho vừa khít khung hiển thị
        cols = max_cols
        rows = int(cols / (aspect * font_aspect))
        if rows > max_rows:
            rows = max_rows
            cols = int(rows * aspect * font_aspect)

        cols = max(10, cols)
        rows = max(10, rows)

        display_w = cols * self.gw
        display_h = rows * self.gh

        offset_x = (player_w - display_w) // 2
        offset_y = player_y + (player_h - display_h) // 2

        # 1. Resize frame với OpenCV
        small_frame = cv2.resize(self.current_frame, (cols, rows), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        # 2. Chọn atlas
        atlas = self.atlas_70 if self.detailed else self.atlas_10
        n_chars = atlas.shape[0]

        char_indices = (gray * (n_chars - 1) // 255).astype(np.int32)
        full_mask = atlas[char_indices].swapaxes(1, 2).reshape(rows * self.gh, cols * self.gw)

        # 3. Tạo hình ảnh theo chế độ màu sắc
        if self.mode == "color":
            upscaled = cv2.resize(small_frame, (display_w, display_h), interpolation=cv2.INTER_NEAREST)
            colored = cv2.bitwise_and(upscaled, upscaled, mask=full_mask)
            rgb = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)

        elif self.mode == "matrix":
            green_bright = cv2.resize(gray, (display_w, display_h), interpolation=cv2.INTER_NEAREST)
            matrix_g = cv2.bitwise_and(green_bright, green_bright, mask=full_mask)
            # Tông xanh neon cyberpunk
            rgb = np.zeros((rows * self.gh, cols * self.gw, 3), dtype=np.uint8)
            rgb[:, :, 1] = matrix_g
            rgb[:, :, 0] = (matrix_g * 0.15).astype(np.uint8)
            rgb[:, :, 2] = (matrix_g * 0.35).astype(np.uint8)

        else: # mono
            mono_bright = cv2.resize(gray, (display_w, display_h), interpolation=cv2.INTER_NEAREST)
            mono_val = cv2.bitwise_and(mono_bright, mono_bright, mask=full_mask)
            rgb = cv2.merge([mono_val, mono_val, mono_val])

        # Chuyển đổi sang Pygame Surface
        frame_surf = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
        self.screen.blit(frame_surf, (offset_x, offset_y))

    def draw_welcome_screen(self, player_y, player_h):
        # Hiệu ứng Matrix mưa ký tự nhẹ ở nền
        for drop in self.matrix_rain:
            drop["y"] += drop["speed"]
            if drop["y"] > player_h:
                drop["y"] = np.random.randint(-200, 0)
                drop["speed"] = np.random.randint(3, 8)
            for j in range(drop["len"]):
                cy = player_y + drop["y"] - j * 14
                if player_y <= cy <= player_y + player_h:
                    alpha = int(255 * (1 - j / drop["len"]))
                    color = (0, min(255, alpha), min(80, alpha // 2))
                    char = CHAR_SET_70[hash((drop['x'], j, int(drop['y']))) % len(CHAR_SET_70)]
                    ts = self.ascii_font.render(char, True, color)
                    self.screen.blit(ts, (drop["x"], cy))

        # Khung hộp trung tâm
        box_w, box_h = 560, 260
        bx = (self.width - box_w) // 2
        by = player_y + (player_h - box_h) // 2

        # Card nền mờ bóng bẩy
        card_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (30, 30, 46, 235), (0, 0, box_w, box_h), border_radius=16)
        pygame.draw.rect(card_surf, (137, 180, 250, 150), (0, 0, box_w, box_h), 2, border_radius=16)
        self.screen.blit(card_surf, (bx, by))

        # Tiêu đề
        title = self.title_font.render("🎬 VIDEO TO ASCII PLAYER", True, (166, 227, 161))
        self.screen.blit(title, (bx + (box_w - title.get_width()) // 2, by + 28))

        sub = self.ui_font.render("Phát video trực tiếp dạng ký tự ASCII - 60 FPS Mượt Mà", True, (205, 214, 244))
        self.screen.blit(sub, (bx + (box_w - sub.get_width()) // 2, by + 72))

        # Nút Chọn Video Lớn
        btn_w, btn_h = 280, 46
        btn_x = bx + (box_w - btn_w) // 2
        btn_y = by + 120
        self.open_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        mx, my = pygame.mouse.get_pos()
        is_hover = self.open_btn_rect.collidepoint(mx, my)
        btn_color = (180, 240, 175) if is_hover else (166, 227, 161)
        pygame.draw.rect(self.screen, btn_color, self.open_btn_rect, border_radius=10)

        btn_text = self.ui_font.render("📂 CHỌN VIDEO TỪ MÁY...", True, (17, 17, 27))
        self.screen.blit(btn_text, (btn_x + (btn_w - btn_text.get_width()) // 2, btn_y + 13))

        # Hướng dẫn kéo thả
        drag_hint = self.ui_font_small.render("Hoặc Kéo & Thả file video (.mp4, .mkv, .avi) thẳng vào đây", True, (166, 173, 200))
        self.screen.blit(drag_hint, (bx + (box_w - drag_hint.get_width()) // 2, by + 185))

        key_hint = self.ui_font_small.render("Phím tắt: [Space]: Tạm dừng | [1, 2, 3]: Đổi chế độ | [F11]: Toàn màn hình", True, (108, 112, 134))
        self.screen.blit(key_hint, (bx + (box_w - key_hint.get_width()) // 2, by + 215))

    def draw_top_bar(self, bar_h):
        # Thanh Top Bar phong cách Mac/Cyberpunk
        top_surf = pygame.Surface((self.width, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(top_surf, (30, 30, 46, 245), (0, 0, self.width, bar_h))
        pygame.draw.line(top_surf, (49, 50, 68), (0, bar_h - 1), (self.width, bar_h - 1), 1)
        self.screen.blit(top_surf, (0, 0))

        mx, my = pygame.mouse.get_pos()
        x_cursor = 16

        # 1. Nút Mở File
        btn_open = pygame.Rect(x_cursor, 10, 110, 32)
        self.top_btn_open = btn_open
        is_h = btn_open.collidepoint(mx, my)
        pygame.draw.rect(self.screen, (69, 71, 90) if is_h else (49, 50, 68), btn_open, border_radius=6)
        txt = self.ui_font.render("📂 Mở Video", True, (255, 255, 255))
        self.screen.blit(txt, (btn_open.x + (btn_open.w - txt.get_width()) // 2, btn_open.y + 7))
        x_cursor += 125

        # 2. Phân cách
        pygame.draw.line(self.screen, (69, 71, 90), (x_cursor, 14), (x_cursor, 38), 1)
        x_cursor += 15

        # 3. Các nút chọn chế độ: TrueColor, Matrix, Mono
        modes = [
            ("color", "🎨 TrueColor", (137, 180, 250)),
            ("matrix", "🟢 Matrix", (166, 227, 161)),
            ("mono", "📺 Đen Trắng", (205, 214, 244)),
        ]
        self.mode_rects = {}
        for m_id, label, active_col in modes:
            is_active = (self.mode == m_id)
            r = pygame.Rect(x_cursor, 10, 115, 32)
            self.mode_rects[m_id] = r
            is_h = r.collidepoint(mx, my)

            if is_active:
                pygame.draw.rect(self.screen, (45, 53, 72), r, border_radius=6)
                pygame.draw.rect(self.screen, active_col, r, 2, border_radius=6)
                t_col = active_col
            else:
                pygame.draw.rect(self.screen, (49, 50, 68) if is_h else (30, 30, 46), r, border_radius=6)
                t_col = (166, 173, 200)

            t_surf = self.ui_font.render(label, True, t_col)
            self.screen.blit(t_surf, (r.x + (r.w - t_surf.get_width()) // 2, r.y + 7))
            x_cursor += 123

        # 4. Phân cách
        pygame.draw.line(self.screen, (69, 71, 90), (x_cursor, 14), (x_cursor, 38), 1)
        x_cursor += 15

        # 5. Ký tự chi tiết (70 ký tự vs 10 ký tự)
        self.detail_btn = pygame.Rect(x_cursor, 10, 110, 32)
        is_h = self.detail_btn.collidepoint(mx, my)
        bg = (45, 53, 72) if self.detailed else (30, 30, 46)
        pygame.draw.rect(self.screen, bg, self.detail_btn, border_radius=6)
        if self.detailed:
            pygame.draw.rect(self.screen, (249, 226, 175), self.detail_btn, 1, border_radius=6)
        d_lbl = "💎 70 Ký tự" if self.detailed else "⚙️ 10 Ký tự"
        d_txt = self.ui_font.render(d_lbl, True, (249, 226, 175) if self.detailed else (147, 153, 178))
        self.screen.blit(d_txt, (self.detail_btn.x + (self.detail_btn.w - d_txt.get_width()) // 2, self.detail_btn.y + 7))
        x_cursor += 120

        # 6. Âm thanh ON/OFF
        self.audio_btn = pygame.Rect(x_cursor, 10, 110, 32)
        is_h = self.audio_btn.collidepoint(mx, my)
        pygame.draw.rect(self.screen, (49, 50, 68) if is_h else (30, 30, 46), self.audio_btn, border_radius=6)
        a_lbl = "🔊 Âm thanh" if self.with_audio else "🔇 Đã tắt"
        a_col = (166, 227, 161) if self.with_audio else (243, 139, 168)
        a_txt = self.ui_font.render(a_lbl, True, a_col)
        self.screen.blit(a_txt, (self.audio_btn.x + (self.audio_btn.w - a_txt.get_width()) // 2, self.audio_btn.y + 7))

        # Bên phải cùng: Tên file đang phát (nếu có)
        if self.video_path:
            filename = os.path.basename(self.video_path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            f_txt = self.ui_font_small.render(f"🎬 {filename}", True, (166, 173, 200))
            self.screen.blit(f_txt, (self.width - f_txt.get_width() - 16, 18))

    def draw_bottom_bar(self, bar_h):
        bar_y = self.height - bar_h
        bot_surf = pygame.Surface((self.width, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(bot_surf, (30, 30, 46, 245), (0, 0, self.width, bar_h))
        pygame.draw.line(bot_surf, (49, 50, 68), (0, 0), (self.width, 0), 1)
        self.screen.blit(bot_surf, (0, bar_y))

        mx, my = pygame.mouse.get_pos()

        # 1. Nút Play / Pause
        self.play_btn_rect = pygame.Rect(16, bar_y + 14, 38, 34)
        is_h = self.play_btn_rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, (69, 71, 90) if is_h else (49, 50, 68), self.play_btn_rect, border_radius=6)
        sym = "⏸" if self.is_playing else "▶"
        p_txt = self.ui_font.render(sym, True, (166, 227, 161) if self.is_playing else (205, 214, 244))
        self.screen.blit(p_txt, (self.play_btn_rect.x + (self.play_btn_rect.w - p_txt.get_width()) // 2, self.play_btn_rect.y + 6))

        # 2. Thanh tua tiến độ (Scrubber Progress Bar)
        scrub_x = 70
        scrub_w = self.width - 250
        scrub_y = bar_y + 24
        scrub_h = 8
        self.scrub_rect = pygame.Rect(scrub_x, scrub_y - 8, scrub_w, scrub_h + 16)

        # Track nền
        pygame.draw.rect(self.screen, (49, 50, 68), (scrub_x, scrub_y, scrub_w, scrub_h), border_radius=4)

        # Tiến trình đã chạy
        ratio = (self.current_frame_idx / self.total_frames) if self.total_frames > 0 else 0.0
        ratio = max(0.0, min(1.0, ratio))
        fill_w = int(ratio * scrub_w)
        if fill_w > 0:
            pygame.draw.rect(self.screen, (166, 227, 161), (scrub_x, scrub_y, fill_w, scrub_h), border_radius=4)

        # Con trỏ tròn (Thumb)
        thumb_x = scrub_x + fill_w
        pygame.draw.circle(self.screen, (245, 245, 245), (thumb_x, scrub_y + scrub_h // 2), 7)

        # 3. Bộ đếm thời gian
        cur_sec = int(self.current_frame_idx / self.fps) if self.fps > 0 else 0
        tot_sec = int(self.duration)
        cur_str = f"{cur_sec // 60:02d}:{cur_sec % 60:02d}"
        tot_str = f"{tot_sec // 60:02d}:{tot_sec % 60:02d}"
        time_txt = self.ui_font.render(f"{cur_str} / {tot_str}", True, (205, 214, 244))
        self.screen.blit(time_txt, (scrub_x + scrub_w + 14, bar_y + 19))

        # 4. Nút Toàn màn hình
        self.fs_btn_rect = pygame.Rect(self.width - 48, bar_y + 14, 34, 34)
        is_h_fs = self.fs_btn_rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, (69, 71, 90) if is_h_fs else (49, 50, 68), self.fs_btn_rect, border_radius=6)
        fs_sym = "🗗" if self.is_fullscreen else "⛶"
        fs_txt = self.ui_font.render(fs_sym, True, (205, 214, 244))
        self.screen.blit(fs_txt, (self.fs_btn_rect.x + (self.fs_btn_rect.w - fs_txt.get_width()) // 2, self.fs_btn_rect.y + 6))

    def handle_click(self, mx, my):
        # 1. Nút mở video ở top bar
        if hasattr(self, 'top_btn_open') and self.top_btn_open.collidepoint(mx, my):
            self.open_file_dialog()
            return

        # 2. Nút mở video ở màn hình chờ
        if not self.cap and hasattr(self, 'open_btn_rect') and self.open_btn_rect.collidepoint(mx, my):
            self.open_file_dialog()
            return

        # 3. Chọn chế độ màu
        if hasattr(self, 'mode_rects'):
            for m_id, r in self.mode_rects.items():
                if r.collidepoint(mx, my):
                    self.mode = m_id
                    return

        # 4. Chọn mật độ ký tự
        if hasattr(self, 'detail_btn') and self.detail_btn.collidepoint(mx, my):
            self.detailed = not self.detailed
            return

        # 5. Bật tắt âm thanh
        if hasattr(self, 'audio_btn') and self.audio_btn.collidepoint(mx, my):
            self.with_audio = not self.with_audio
            if not self.with_audio and self.audio_loaded:
                pygame.mixer.music.pause()
            elif self.with_audio and self.audio_loaded and self.is_playing:
                pygame.mixer.music.unpause()
            return

        # 6. Nút Play / Pause
        if hasattr(self, 'play_btn_rect') and self.play_btn_rect.collidepoint(mx, my):
            self.toggle_play()
            return

        # 7. Nhấp tua thanh tiến độ
        if hasattr(self, 'scrub_rect') and self.scrub_rect.collidepoint(mx, my):
            self.is_scrubbing = True
            self.handle_scrub(mx)
            return

        # 8. Nút Fullscreen
        if hasattr(self, 'fs_btn_rect') and self.fs_btn_rect.collidepoint(mx, my):
            self.toggle_fullscreen()
            return

    def handle_scrub(self, mx):
        if not self.cap or self.total_frames <= 0:
            return
        scrub_x = 70
        scrub_w = self.width - 250
        ratio = (mx - scrub_x) / scrub_w
        self.seek_to_ratio(ratio)

def main(video_arg=None):
    if not video_arg and len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        video_arg = sys.argv[1]
    app = AsciiVideoPlayerApp(initial_video=video_arg)
    app.run()

if __name__ == "__main__":
    main()
