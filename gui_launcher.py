import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_SCRIPT = os.path.join(SCRIPT_DIR, "ascii_player.py")
PYTHON_EXE = sys.executable

class AsciiPlayerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video to ASCII Player - Cấu hình")
        self.root.geometry("520x480")
        self.root.resizable(False, False)

        # Cài đặt giao diện tối hiện đại
        self.bg_color = "#181825"
        self.card_bg = "#1e1e2e"
        self.text_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.green_btn = "#a6e3a1"
        self.green_btn_text = "#11111b"

        self.root.configure(bg=self.bg_color)

        # Style cho ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TLabel", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=self.bg_color, foreground=self.accent_color, font=("Segoe UI", 15, "bold"))
        self.style.configure("SubHeader.TLabel", background=self.card_bg, foreground=self.accent_color, font=("Segoe UI", 11, "bold"))
        self.style.configure("TRadiobutton", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TCheckbutton", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))

        self.video_path_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="color")      # 'color', 'matrix', 'mono'
        self.audio_var = tk.BooleanVar(value=True)       # True / False
        self.detailed_var = tk.BooleanVar(value=False)   # True / False

        # Tự động chọn file video demo nếu có sẵn trong thư mục
        demo_file = os.path.join(SCRIPT_DIR, "demo.mp4")
        if os.path.isfile(demo_file):
            self.video_path_var.set(demo_file)

        self.build_ui()

    def build_ui(self):
        # Header
        header = ttk.Label(self.root, text="🎬 VIDEO TO ASCII PLAYER", style="Header.TLabel")
        header.pack(pady=(15, 10))

        # Khung 1: Chọn file video
        file_frame = tk.LabelFrame(
            self.root, text=" 📁 1. Chọn Video ", bg=self.card_bg, fg=self.accent_color,
            font=("Segoe UI", 10, "bold"), padx=12, pady=10, relief="solid", bd=1
        )
        file_frame.pack(fill="x", padx=18, pady=6)

        entry_box = tk.Entry(
            file_frame, textvariable=self.video_path_var, font=("Segoe UI", 9),
            bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", relief="flat"
        )
        entry_box.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 8))

        browse_btn = tk.Button(
            file_frame, text="📂 Chọn tệp...", command=self.browse_video,
            bg="#45475a", fg="#ffffff", activebackground="#585b70", activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=8, pady=2
        )
        browse_btn.pack(side="right")

        # Khung 2: Tùy chọn chế độ hiển thị
        mode_frame = tk.LabelFrame(
            self.root, text=" 🎨 2. Chế độ màu sắc ", bg=self.card_bg, fg=self.accent_color,
            font=("Segoe UI", 10, "bold"), padx=12, pady=8, relief="solid", bd=1
        )
        mode_frame.pack(fill="x", padx=18, pady=6)

        r1 = ttk.Radiobutton(mode_frame, text="Màu sắc TrueColor sống động (RGB) [Khuyên dùng]", variable=self.mode_var, value="color")
        r1.pack(anchor="w", pady=2)

        r2 = ttk.Radiobutton(mode_frame, text="Phong cách Hacker Matrix (Xanh Neon Cyberpunk)", variable=self.mode_var, value="matrix")
        r2.pack(anchor="w", pady=2)

        r3 = ttk.Radiobutton(mode_frame, text="Đen trắng cổ điển (Monochrome ASCII)", variable=self.mode_var, value="mono")
        r3.pack(anchor="w", pady=2)

        # Khung 3: Tích chọn các tính năng
        opt_frame = tk.LabelFrame(
            self.root, text=" ⚙️ 3. Tùy chọn bổ sung ", bg=self.card_bg, fg=self.accent_color,
            font=("Segoe UI", 10, "bold"), padx=12, pady=8, relief="solid", bd=1
        )
        opt_frame.pack(fill="x", padx=18, pady=6)

        c1 = ttk.Checkbutton(opt_frame, text="🔊 Bật âm thanh đồng bộ (Audio)", variable=self.audio_var)
        c1.pack(anchor="w", pady=2)

        c2 = ttk.Checkbutton(opt_frame, text="💎 Dùng bộ ký tự siêu chi tiết (70 ký tự ASCII)", variable=self.detailed_var)
        c2.pack(anchor="w", pady=2)

        # Nút Bắt đầu phát video (Nút OK)
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=18, pady=(15, 10))

        start_btn = tk.Button(
            btn_frame, text="▶  BẮT ĐẦU PHÁT VIDEO (OK)", command=self.start_playback,
            bg=self.green_btn, fg=self.green_btn_text, activebackground="#94e2d5",
            font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2", pady=8
        )
        start_btn.pack(fill="x")

    def browse_video(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file video",
            filetypes=[
                ("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.video_path_var.set(os.path.abspath(file_path))

    def start_playback(self):
        video = self.video_path_var.get().strip("\"' ")
        if not video or not os.path.isfile(video):
            messagebox.showwarning("Chưa chọn video", "Vui lòng chọn một file video hợp lệ trước khi bắt đầu!")
            return

        cmd_flags = []
        mode = self.mode_var.get()
        if mode == "matrix":
            cmd_flags.append("--matrix")
        elif mode == "mono":
            cmd_flags.append("--mono")

        if self.detailed_var.get():
            cmd_flags.append("--detailed")

        if not self.audio_var.get():
            cmd_flags.append("--no-audio")

        # Khởi chạy trong một cửa sổ PowerShell mới độc lập với xử lý encoding UTF-8
        cmd = [
            "powershell.exe",
            "-NoExit",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; & '{PYTHON_EXE}' '{PLAYER_SCRIPT}' '{video}' " + " ".join(cmd_flags)
        ]

        try:
            subprocess.Popen(
                cmd,
                cwd=SCRIPT_DIR,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            messagebox.showerror("Lỗi khởi chạy", f"Không thể khởi chạy trình phát video:\n{e}")

def main():
    root = tk.Tk()
    app = AsciiPlayerLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
