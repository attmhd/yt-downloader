import os
import sys
import threading
from pathlib import Path
from datetime import timedelta
import yt_dlp

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # Specific for PyInstaller
        return sys._MEIPASS
    return None

class Downloader:
    def __init__(self, progress_callback=None, status_callback=None, log_callback=None):
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.log_callback = log_callback
        self.stop_flag = threading.Event()

    def cancel(self):
        self.stop_flag.set()

    def download(self, url, outdir, kind, cookies_file=None):
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
                
                if self.progress_callback:
                    self.progress_callback(frac)
                if self.status_callback:
                    self.status_callback(f"Downloading: {frac*100:5.1f}% • {human_speed} • ETA {eta_str}")
            
            elif d.get('status') == 'finished':
                if self.progress_callback:
                    self.progress_callback(1.0)
                if self.status_callback:
                    self.status_callback("Converting / Post-processing...")

        outtmpl = os.path.join(outdir, '%(title)s [%(id)s].%(ext)s')
        ffmpeg_path = get_ffmpeg_path()
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

        if ffmpeg_path:
            common_opts['ffmpeg_location'] = ffmpeg_path

        if cookies_file:
            common_opts['cookiefile'] = cookies_file

        if kind == 'audio':
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                    {'key': 'FFmpegMetadata'},
                ],
            }
        else:
            ydl_opts = {
                **common_opts,
                'format': 'bv*+ba/b',
                'postprocessors': [
                    {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                    {'key': 'FFmpegMetadata'},
                ],
            }

        try:
            self.stop_flag.clear()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if self.log_callback:
                self.log_callback("Finished ✅")
            if self.status_callback:
                self.status_callback("Done.")
            return True
        except KeyboardInterrupt:
            if self.log_callback:
                self.log_callback("Cancelled by user", "ERROR")
            if self.status_callback:
                self.status_callback("Cancelled.")
            return False
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"Error: {e}", "ERROR")
            if self.status_callback:
                self.status_callback("Failed.")
            return False
