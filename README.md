# Roblox Vintage Game Finder

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)


A multithreaded Python script to discover vintage Roblox games from 2006–2009 that meet specific criteria.

> [!NOTE]
> **Disclaimer:** This project is not affiliated with Roblox Corporation. Use at your own risk. Please respect Roblox's terms of service and API usage guidelines.

---

## Features

- **Multithreaded Scanning**: Faster scanning with configurable worker threads
- **Vintage Game Filtering**:
  - Created between 2006–2009
  - Not updated in over 3 years
  - At least 1000+ visits
  - Must be uncopylocked
- **Game Details**:
  - Place ID, title, creation and update timestamps
  - Visit count
  - Copylocked status
  - Game Pass names
  - Thumbnail URL
- **Rate Limited Requests**: Follows API rate limits using a locking mechanism
- **Progress Saving**: Saves where it left off so you can resume scanning

---

## Requirements

- Python 3.8+
- `requests` library

Install it via:

```bash
pip install requests
```

---

## Installation

```bash
git clone https://github.com/NokaAngel/Roblox-Vintage-Game-Finder.git
cd Roblox-Vintage-Game-Finder
```

---

## Usage

Edit config values at the top of `game-scraper.py` if needed:

```python
OUTPUT_FILE = "Enhanced Games List.txt"
START_ID = 1450
RATE_LIMIT_DELAY = 2.0
MAX_WORKERS = 5
```

Run the script:

```bash
python game-scraper.py
```

Output will be written to: `Enhanced Games List.txt`

---

## Sample Output

```
Place ID: 1451
URL: https://www.roblox.com/games/1451/
Title: Rocket Mayhem
Status: Uncopylocked
Created: 2007-06-04T16:22:19.223Z
Updated: 2011-03-12T09:11:33.390Z
Visits: 12983
Thumbnail: https://tr.rbxcdn.com/...jpg
Game Passes: VIP Room, Gravity Coil
==================================================
```

---

## Configuration Options

| Setting            | Description                                | Default                 |
| ------------------ | ------------------------------------------ | ----------------------- |
| OUTPUT\_FILE       | File name to write results to              | Enhanced Games List.txt |
| START\_ID          | Initial Place ID to begin scan             | 1450                    |
| RATE\_LIMIT\_DELAY | Seconds between each API call (per thread) | 2.0                     |
| MAX\_WORKERS       | Number of concurrent threads to scan       | 5                       |

---

## Contributing

1. Fork this repository
2. Create a new branch: `git checkout -b user/YourFeature`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push your branch: `git push origin user/YourFeature`
5. Submit a Pull Request

---

## License

MIT License. See the `LICENSE` file for details.


