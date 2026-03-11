import os
import sys
import threading
import queue
import webbrowser
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.core.downloader import Downloader

# App Constants
APP_TITLE = "Pro Downloader v1"
VERSION = "1.0.1"
DEFAULT_DIR = str(Path.home() / "Downloads")
DONATION_LINK = "https://saweria.co/attmhd"

# Font Configuration
FONT_FAMILY = "Inter" if sys.platform.startswith("linux") else "Segoe UI"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Window Config
        self.title(f"{APP_TITLE} - Multi-Platform")
        self.geometry("950x650")
        
        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # State
        self.msg_queue = queue.Queue()
        self.downloader = Downloader(
            progress_callback=self._update_progress_safe,
            status_callback=self._update_status_safe,
            log_callback=self._log_safe
        )

        # UI Components
        self._setup_sidebar()
        self._setup_main_content()

        # Update loop
        self.after(100, self._drain_queue)

    def _setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PRO DOWNLOADER", 
                                      font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        self.sublog_label = ctk.CTkLabel(self.sidebar_frame, text="Fast & Reliable", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=12), 
                                        text_color=("gray40", "gray60"))
        self.sublog_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # Sidebar Buttons
        self.dl_btn = ctk.CTkButton(self.sidebar_frame, text="Downloader", 
                                   font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                   hover_color=("gray70", "gray30"), anchor="w")
        self.dl_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.donation_btn = ctk.CTkButton(self.sidebar_frame, text="Support Creator", 
                                         font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                                         fg_color="#f97316", hover_color="#ea580c",
                                         text_color="white", anchor="center",
                                         command=self.open_donation)
        self.donation_btn.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Exit Button
        self.exit_btn = ctk.CTkButton(self.sidebar_frame, text="Exit Application", 
                                     font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                     fg_color=("gray80", "gray25"), hover_color="#d73a49",
                                     text_color=("gray10", "gray90"),
                                     command=self.quit)
        self.exit_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Bottom Sidebar Info
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", 
                                                 font=ctk.CTkFont(family=FONT_FAMILY, size=12), anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 20))

        self.copyright_label = ctk.CTkLabel(self.sidebar_frame, text=f"© 2025 Natta Std\nVersion {VERSION}", 
                                           font=ctk.CTkFont(family=FONT_FAMILY, size=10), 
                                           text_color=("gray40", "gray60"))
        self.copyright_label.grid(row=9, column=0, padx=20, pady=(0, 20))

    def _setup_main_content(self):
        self.main_container = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)

        # Header Info - Using dynamic colors for contrast
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color=("gray85", "gray14"), corner_radius=15)
        self.header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        
        self.header_title = ctk.CTkLabel(self.header_frame, text="Universal Media Downloader", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold"),
                                        text_color=("gray10", "gray95"))
        self.header_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.header_desc = ctk.CTkLabel(self.header_frame, 
                                        text="Download from YouTube, Instagram, TikTok, Facebook, and more.", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=14), 
                                        text_color=("gray30", "gray70"))
        self.header_desc.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # URL Section
        self.content_card = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_card.grid(row=1, column=0, padx=30, pady=0, sticky="ew")
        self.content_card.grid_columnconfigure(0, weight=1)

        self.url_label = ctk.CTkLabel(self.content_card, text="Media URL:", 
                                     font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
                                     text_color=("gray10", "gray90"))
        self.url_label.grid(row=0, column=0, padx=5, pady=(0, 8), sticky="w")
        
        self.url_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.url_frame.grid(row=1, column=0, pady=0, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="Paste your link here...", 
                                     height=48, border_width=2, font=ctk.CTkFont(family=FONT_FAMILY, size=14),
                                     fg_color=("white", "gray20"), text_color=("black", "white"))
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        
        self.paste_btn = ctk.CTkButton(self.url_frame, text="Paste", width=100, height=48, 
                                      font=ctk.CTkFont(family=FONT_FAMILY, size=14),
                                      fg_color=("gray80", "gray30"), text_color=("gray10", "gray90"),
                                      command=self.paste_clipboard)
        self.paste_btn.grid(row=0, column=1)

        # Settings
        self.settings_frame = ctk.CTkFrame(self.content_card, fg_color=("gray90", "gray12"), corner_radius=12)
        self.settings_frame.grid(row=2, column=0, pady=25, sticky="ew")
        self.settings_frame.grid_columnconfigure((0, 1), weight=1)

        # Output Folder
        self.out_label = ctk.CTkLabel(self.settings_frame, text="Download Directory", 
                                     font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                                     text_color=("gray10", "gray90"))
        self.out_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.out_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.out_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.out_frame.grid_columnconfigure(0, weight=1)
        
        self.out_entry = ctk.CTkEntry(self.out_frame, height=35, font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                     fg_color=("white", "gray20"), text_color=("black", "white"))
        self.out_entry.insert(0, DEFAULT_DIR)
        self.out_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.browse_btn = ctk.CTkButton(self.out_frame, text="Browse", width=70, height=35, 
                                       font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                                       fg_color=("gray75", "gray25"), text_color=("gray10", "gray90"),
                                       command=self.choose_dir)
        self.browse_btn.grid(row=0, column=1)

        # Format
        self.format_label = ctk.CTkLabel(self.settings_frame, text="Output Format", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                                        text_color=("gray10", "gray90"))
        self.format_label.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")
        
        self.format_option = ctk.CTkSegmentedButton(self.settings_frame, values=["Video (MP4)", "Audio (MP3)"], 
                                                   height=38, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
        self.format_option.set("Video (MP4)")
        self.format_option.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")

        # Progress / Status
        self.status_container = ctk.CTkFrame(self.content_card, fg_color=("gray90", "gray12"), corner_radius=12)
        self.status_container.grid(row=3, column=0, pady=(0, 25), sticky="ew")
        self.status_container.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.status_container, text="Ready", 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                        text_color=("gray20", "gray80"))
        self.status_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.progress_bar = ctk.CTkProgressBar(self.status_container, height=12)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progress_bar.set(0)

        # Log Panel
        self.log_label = ctk.CTkLabel(self.content_card, text="Status Logs:", 
                                     font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                                     text_color=("gray20", "gray80"))
        self.log_label.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")
        
        self.log_text = ctk.CTkTextbox(self.content_card, height=120, fg_color=("white", "black"), 
                                      border_width=1, border_color=("gray70", "gray30"),
                                      text_color=("black", "gray90"),
                                      font=ctk.CTkFont(family="Courier", size=12))
        self.log_text.grid(row=5, column=0, pady=(0, 25), sticky="ew")
        self.log_text.configure(state="disabled")

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.btn_frame.grid(row=6, column=0, pady=(0, 40), sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)

        self.download_btn = ctk.CTkButton(self.btn_frame, text="START DOWNLOAD", height=58, 
                                          font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"), 
                                          command=self.start_download)
        self.download_btn.grid(row=0, column=0, sticky="ew", padx=(0, 15))

        self.cancel_btn = ctk.CTkButton(self.btn_frame, text="Cancel", width=120, height=58, 
                                        font=ctk.CTkFont(family=FONT_FAMILY, size=14),
                                        fg_color="transparent", border_width=2, border_color="#d73a49",
                                        text_color="#d73a49", hover_color=("#f8d7da", "#2d1b1b"),
                                        state="disabled", command=self.cancel_download)
        self.cancel_btn.grid(row=0, column=1)

    def open_donation(self):
        webbrowser.open(DONATION_LINK)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def paste_clipboard(self):
        try:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, self.clipboard_get())
        except:
            pass

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.out_entry.get() or DEFAULT_DIR)
        if d:
            self.out_entry.delete(0, "end")
            self.out_entry.insert(0, d)

    def log(self, msg, tag="INFO"):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{tag}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_download(self):
        url = self.url_entry.get().strip()
        outdir = self.out_entry.get().strip()
        kind = "audio" if "MP3" in self.format_option.get() else "video"

        if not url or not outdir:
            messagebox.showwarning("Input Error", "Please provide a valid URL and Output Folder.")
            return

        Path(outdir).mkdir(parents=True, exist_ok=True)

        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.log(f"Starting job for: {url}")
        
        thread = threading.Thread(target=self._worker, args=(url, outdir, kind), daemon=True)
        thread.start()

    def cancel_download(self):
        self.downloader.cancel()
        self.status_label.configure(text="Cancelling job...")

    def _worker(self, url, outdir, kind):
        success = self.downloader.download(url, outdir, kind)
        self._emit(self._on_complete, success)

    def _on_complete(self, success):
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        if success:
            messagebox.showinfo("Success", "Download Task Completed Successfully!")
            if sys.platform.startswith('linux'):
                 os.system(f'xdg-open "{self.out_entry.get()}" &')

    def _update_progress_safe(self, value):
        self._emit(self.progress_bar.set, value)

    def _update_status_safe(self, text):
        self._emit(self.status_label.configure, text=text)

    def _log_safe(self, msg, tag="INFO"):
        self._emit(self.log, msg, tag)

    def _emit(self, fn, *args, **kwargs):
        self.msg_queue.put((fn, args, kwargs))

    def _drain_queue(self):
        try:
            while True:
                fn, args, kwargs = self.msg_queue.get_nowait()
                fn(*args, **kwargs)
        except queue.Empty:
            pass
        self.after(100, self._drain_queue)

if __name__ == "__main__":
    app = App()
    app.mainloop()
