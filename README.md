# Roblox Vintage Game Finder

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python script that scans for classic Roblox games from 2006-2009 based on activity, visit count, and other metadata.

> [!WARNING]
> **Disclaimer** This project is not affiliated with Roblox Corporation. Use responsibly and respect Roblox's terms of service.

---

## Features

- **Vintage Game Detection**: Targets games created between 2006 and 2009
- **Visit and Inactivity Filtering**: Requires 1,000+ visits and no updates for 3+ years
- **Game Metadata Extraction**: Pulls title, visit count, creation/update dates, thumbnails, and game passes
- **Concurrency Support**: Uses multithreading with rate limiting to scan faster
- **Progress Tracking**: Saves the last scanned ID and found games
- **Graceful Exit**: Handles Ctrl+C interrupts, waits for workers to complete, and saves progress cleanly

---

## Requirements

- Python 3.8+
- `requests` library (install via `pip install requests`)

---

## Installation

```bash
git clone https://github.com/NokaAngel/Roblox-Vintage-Game-Finder.git
cd Roblox-Vintage-Game-Finder
pip install requests
```

---

## Usage

Edit the top of the script if needed:

```python
START_ID = 1450
RATE_LIMIT_DELAY = 2.0
MAX_WORKERS = 5
```

Then run it:

```bash
python place-scraper.py
```

Output is saved to `Enhanced Games List.txt`

---

## Output Format Example

```
Place ID: 12345678
URL: https://www.roblox.com/games/12345678/
Title: Classic Tycoon
Status: Uncopylocked
Created: 2008-03-04T19:20:31.563Z
Updated: 2011-05-12T08:34:19.267Z
Visits: 123456
Thumbnail: https://.../thumbnail.png
Game Passes: VIP Shirt, Golden Sword
==================================================
```

---

## Configuration Options

| Setting            | Description                                    | Default                   |
| ------------------ | ---------------------------------------------- | ------------------------- |
| `OUTPUT_FILE`      | Output file path                               | `Enhanced Games List.txt` |
| `START_ID`         | Starting Place ID                              | `1450`                    |
| `RATE_LIMIT_DELAY` | Delay between requests per thread (in seconds) | `2.0`                     |
| `MAX_WORKERS`      | Number of concurrent threads                   | `5`                       |

---

## Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature-branch`)
5. Open a pull request

---

## License

MIT License. See `LICENSE` file for full terms.
