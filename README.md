# Markdown (Obsidian) Speed Reader

Run to install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## Installation

### Windows
Run to install:
```bash
pyinstaller --onefile --noconsole  --icon=.\icon_assets\png_logo.ico Obsidian_Reader.py
```

Once the executable is built, just copy/paste some text in, hit play, and adjust the speed with the slider.

### Linux Version Features
The Linux version (`linux/obsidian_reader_linux.py`) includes additional features:

- RSS Feed Support: Read articles from RSS feeds directly
  ```bash
  python3 obsidian_reader_linux.py --rss https://example.com/feed.xml
  ```
- Directory Reading: Process all markdown files in a directory
  ```bash
  python3 obsidian_reader_linux.py --directory /path/to/markdown/files
  ```
- Single File Reading
  ```bash
  python3 obsidian_reader_linux.py --file /path/to/file.md
  ```