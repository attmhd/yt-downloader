#!/bin/bash
# Build script untuk YT-Downloader GUI

echo "Building YT-Downloader GUI..."

# # Install dependencies jika belum ada
# pip install -r requirements.txt
# pip install pyinstaller

# # Clean previous builds
# rm -rf build/ dist/

# Build executable
uv run pyinstaller build.spec --clean

# Check if build successful
if [ -f "dist/Modern-YT-Downloader" ]; then
    echo "✅ Build successful!"
    echo "Executable created: dist/Modern-YT-Downloader"
    echo ""
    echo "Dependencies yang dibutuhkan di sistem target:"
    echo "- ffmpeg (untuk konversi video/audio)"
    echo ""
    echo "Cara menjalankan:"
    echo "./dist/Modern-YT-Downloader"
else
    echo "❌ Build failed!"
    exit 1
fi
