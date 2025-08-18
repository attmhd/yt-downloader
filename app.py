#!/usr/bin/env python3
"""
Simple YT-DLP GUI for Linux (CachyOS / Arch) using Tkinter
Features:
- Download Video (MP4) or Audio (MP3)
- Choose output folder
- Progress bar + speed/ETA
- Log panel
- Open folder when done

Requirements:
  pacman -S python tk yt-dlp ffmpeg
or (if you prefer pip for yt-dlp):
  pacman -S python tk ffmpeg
  pip install -U yt-dlp
"""
import os
import sys
import threading
import queue
from pathlib import Path
from datetime import timedelta

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import yt_dlp
except ImportError:
    messagebox.showerror("Missing dependency", "yt-dlp tidak terpasang. Install dengan: pip install -U yt-dlp atau pacman -S yt-dlp")
    raise

APP_TITLE = "YT-DLP GUI Downloader"
DEFAULT_DIR = str(Path.home() / "Downloads")

class YTDLPGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(760, 520)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # State
        self.stop_flag = threading.Event()
        self.msg_queue = queue.Queue()

        # URL
        frm_url = ttk.Frame(self)
        frm_url.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        frm_url.columnconfigure(1, weight=1)
        ttk.Label(frm_url, text="URL Video / Playlist").grid(row=0, column=0, sticky="w", padx=(0,8))
        self.var_url = tk.StringVar()
        self.ent_url = ttk.Entry(frm_url, textvariable=self.var_url)
        self.ent_url.grid(row=0, column=1, sticky="ew")
        ttk.Button(frm_url, text="Paste", command=self.paste_clipboard).grid(row=0, column=2, padx=(8,0))

        # Output dir
        frm_out = ttk.Frame(self)
        frm_out.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        frm_out.columnconfigure(1, weight=1)
        ttk.Label(frm_out, text="Output Folder").grid(row=0, column=0, sticky="w", padx=(0,8))
        self.var_dir = tk.StringVar(value=DEFAULT_DIR)
        self.ent_dir = ttk.Entry(frm_out, textvariable=self.var_dir)
        self.ent_dir.grid(row=0, column=1, sticky="ew")
        ttk.Button(frm_out, text="Browse", command=self.choose_dir).grid(row=0, column=2, padx=(8,0))

        # Format options
        frm_fmt = ttk.Frame(self)
        frm_fmt.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        self.format_var = tk.StringVar(value="video")
        ttk.Radiobutton(frm_fmt, text="Video (MP4, kualitas terbaik)", variable=self.format_var, value="video").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(frm_fmt, text="Audio (MP3)", variable=self.format_var, value="audio").grid(row=0, column=1, sticky="w", padx=(16,0))
        self.open_folder_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frm_fmt, text="Buka folder setelah selesai", variable=self.open_folder_var).grid(row=0, column=2, sticky="w", padx=(16,0))

        # Progress + controls
        frm_prog = ttk.Frame(self)
        frm_prog.grid(row=3, column=0, sticky="nsew", padx=12, pady=6)
        frm_prog.columnconfigure(0, weight=1)
        frm_prog.rowconfigure(2, weight=1)

        self.progress = ttk.Progressbar(frm_prog, mode="determinate")
        self.progress.grid(row=0, column=0, sticky="ew")

        self.var_status = tk.StringVar(value="Siap.")
        ttk.Label(frm_prog, textvariable=self.var_status).grid(row=1, column=0, sticky="w", pady=(6,6))

        self.txt_log = tk.Text(frm_prog, height=12, wrap="word", state="disabled")
        self.txt_log.grid(row=2, column=0, sticky="nsew")
        self.txt_log.tag_configure("INFO", foreground="#1f6feb")
        self.txt_log.tag_configure("ERROR", foreground="#d73a49")

        # Buttons
        frm_btn = ttk.Frame(self)
        frm_btn.grid(row=4, column=0, sticky="ew", padx=12, pady=(6,12))
        frm_btn.columnconfigure(0, weight=1)
        self.btn_download = ttk.Button(frm_btn, text="Download", command=self.start_download)
        self.btn_download.grid(row=0, column=0, sticky="w")
        self.btn_cancel = ttk.Button(frm_btn, text="Batal", command=self.cancel_download, state="disabled")
        self.btn_cancel.grid(row=0, column=1, sticky="w", padx=(8,0))

        # Periodic UI updater for messages
        self.after(100, self._drain_queue)

    # UI helpers
    def paste_clipboard(self):
        try:
            data = self.clipboard_get()
            self.var_url.set(data)
        except tk.TclError:
            pass

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.var_dir.get() or DEFAULT_DIR)
        if d:
            self.var_dir.set(d)

    def log(self, msg, tag="INFO"):
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", msg + "\n", tag)
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def set_status(self, msg):
        self.var_status.set(msg)

    def set_progress(self, fraction):
        self.progress.configure(value=max(0, min(100, fraction * 100)))

    # Download flow
    def start_download(self):
        url = self.var_url.get().strip()
        outdir = self.var_dir.get().strip()
        kind = self.format_var.get()

        if not url:
            messagebox.showwarning("Input kurang", "Masukkan URL YouTube/Video terlebih dahulu.")
            return
        if not outdir:
            messagebox.showwarning("Folder kosong", "Pilih output folder.")
            return
        Path(outdir).mkdir(parents=True, exist_ok=True)

        self.stop_flag.clear()
        self.btn_download.configure(state="disabled")
        self.btn_cancel.configure(state="normal")
        self.set_status("Mengunduh...")
        self.set_progress(0)
        self.log(f"Mulai download: {url}")

        thread = threading.Thread(target=self._download_worker, args=(url, outdir, kind), daemon=True)
        thread.start()

    def cancel_download(self):
        self.stop_flag.set()
        self.set_status("Membatalkan...")

    def _emit(self, fn, *args, **kwargs):
        # pass UI updates to main thread via queue, including kwargs
        self.msg_queue.put((fn, args, kwargs))

    def _drain_queue(self):
        try:
            while True:
                fn, args, kwargs = self.msg_queue.get_nowait()
                fn(*args, **kwargs)
        except queue.Empty:
            pass
        self.after(100, self._drain_queue)

    def _download_worker(self, url, outdir, kind):
        def hook(d):
            if self.stop_flag.is_set():
                raise KeyboardInterrupt
            if d.get('status') == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes') or 0
                speed = d.get('speed') or 0
                eta = d.get('eta')
                frac = downloaded / total if total else 0.0
                human_speed = f"{speed/1024/1024:.2f} MB/s" if speed else "?"
                eta_str = str(timedelta(seconds=int(eta))) if eta else "?"
                self._emit(self.set_progress, frac)
                self._emit(self.set_status, f"Mengunduh: {frac*100:5.1f}%  •  {human_speed}  •  ETA {eta_str}")
            elif d.get('status') == 'finished':
                self._emit(self.set_progress, 1.0)
                self._emit(self.set_status, "Mengonversi / Post-processing...")

        # Build options
        outtmpl = os.path.join(outdir, '%(title)s [%(id)s].%(ext)s')
        common_opts = {
            'outtmpl': outtmpl,
            'progress_hooks': [hook],
            'noprogress': True,
            'concurrent_fragment_downloads': 4,
            'merge_output_format': 'mp4',
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
        }

        if kind == 'audio':
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                    {'key': 'FFmpegMetadata'},
                ],
            }
        else:  # video
            # bestvideo+audio → mp4 fallback
            ydl_opts = {
                **common_opts,
                'format': 'bv*+ba/b',
                'postprocessors': [
                    {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                    {'key': 'FFmpegMetadata'},
                ],
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self._emit(self.log, "Selesai ✅")
            self._emit(self.set_status, "Selesai.")
        except KeyboardInterrupt:
            self._emit(self.log, "Dibatalkan pengguna", "ERROR")
            self._emit(self.set_status, "Dibatalkan.")
        except Exception as e:
            self._emit(self.log, f"Error: {e}", "ERROR")
            self._emit(self.set_status, "Gagal.")
        finally:
            self._emit(self.btn_download.configure, state="normal")
            self._emit(self.btn_cancel.configure, state="disabled")
            if self.open_folder_var.get() and not self.stop_flag.is_set():
                try:
                    # Linux: use xdg-open
                    folder = self.var_dir.get()
                    if sys.platform.startswith('linux'):
                        os.system(f'xdg-open "{folder}" >/dev/null 2>&1 &')
                except Exception:
                    pass


def main():
    app = YTDLPGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
