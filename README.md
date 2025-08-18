# YT-DLP GUI Downloader

A simple graphical user interface (GUI) for [yt-dlp](https://github.com/yt-dlp/yt-dlp) built with Tkinter for Linux (Debian, Ubuntu, and derivatives).
Download YouTube videos or audio easily, with progress bar, log panel, and output folder selection.

## Features

- Download YouTube videos (MP4, best quality) or audio (MP3)
- Choose output folder
- Progress bar with speed and ETA
- Log panel for download status and errors
- Option to open output folder after download
- Cancel ongoing downloads

## Requirements

### Linux (Debian, Ubuntu, and derivatives)

Install dependencies via apt:

```sh
sudo apt update
sudo apt install python3 python3-tk ffmpeg
pip install -U yt-dlp
```

- `python3-tk` is required for the Tkinter GUI.
- `ffmpeg` is required for audio/video conversion.
- `yt-dlp` can be installed via pip for the latest version.

### Linux (Arch, Manjaro, EndeavourOS, and derivatives)

Install dependencies via pacman:

```sh
sudo pacman -S python tk ffmpeg yt-dlp
```

Or, if you prefer to install yt-dlp via pip for the latest version:

```sh
sudo pacman -S python tk ffmpeg
pip install -U yt-dlp
```

## Usage

1. Clone this repository:

    ```sh
    git clone https://github.com/attmhd/yt-downloader.git
    cd yt-downloader
    ```

2. Run the application:

    ```sh
    python app.py
    ```

3. Paste the YouTube video or playlist URL.
4. Choose the output folder.
5. Select format: **Video (MP4)** or **Audio (MP3)**.
6. Click **Download**.
7. Monitor progress, speed, and ETA.
8. Optionally, open the output folder automatically when done.

## Notes

- This app is designed for Linux (Debian/Ubuntu and derivatives).
- The app uses `xdg-open` to open the output folder after download.
- All downloads are saved with the format:
  `<title> [<id>].<ext>` in the chosen output folder.
- If dependencies are missing, you will see an error message.

## License

MIT
