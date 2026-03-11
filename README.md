# 🚀 Pro Downloader (Universal Media GUI)

A premium, modern graphical user interface for [yt-dlp](https://github.com/yt-dlp/yt-dlp) built with **CustomTkinter**. This tool provides a clean and intuitive experience for downloading media from hundreds of sites including **YouTube, Instagram, TikTok, Facebook, and Twitter**.

## ✨ Features

- **Modern & Clean UI**: Minimalist design with **Light/Dark mode** support.
- **Universal Support**: One tool for YouTube, Instagram Reels, TikTok (no watermark), and more.
- **Fast Performance**: Powered by `yt-dlp` for high-speed, reliable downloads.
- **Progress Tracking**: Real-time status updates, progress bar, and logs.
- **Premium Aesthetics**: Using **Inter** font for a professional look and feel.
- **Cross-Platform**: Optimized for Linux and Windows distribution.

## 🛠️ Project Structure

```text
yt-downloader/
├── src/
│   ├── core/          # Business logic (yt-dlp downloader)
│   └── ui/            # Modern UI components (CustomTkinter)
├── main.py            # Entry point for the application
├── pyproject.toml     # Dependency management (uv)
└── build.spec         # PyInstaller configuration
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **FFmpeg**: Required for high-quality video merging and audio conversion.
  - **Linux**: `sudo apt install ffmpeg` or `sudo pacman -S ffmpeg`
  - **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html)

### Installation (using uv)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/attmhd/yt-downloader.git
   cd yt-downloader
   ```

2. **Run the application:**
   ```bash
   uv run main.py
   ```

## 📦 Building for Distribution

To create a standalone executable:

```bash
# Ensure build script is executable
chmod +x build.sh

# Run the build
./build.sh
```

The output will be in the `dist/` directory.

## 🧡 Support the Creator

If you find this tool useful, consider supporting the development through Saweria:
👉 **[saweria.co/attmhd](https://saweria.co/attmhd)**

## 📜 License

MIT © 2025 attmhd
