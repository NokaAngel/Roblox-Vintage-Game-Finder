# Roblox Vintage Game Finder

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python script to discover and catalog classic Roblox games from 2006-2009 that meet specific criteria.

## Features
> [!IMPORTANT]
> Identifying private games is still unavailable, while it's in the code it is not properly setting the identity if the game is public or private.
> a fix is in the works, but the rest of the features work smooth.

- **Vintage Game Detection**: Finds games created between 2006-2009
- **Activity Filtering**: Only includes games with 1000+ visits
- **Inactivity Check**: Filters games not updated in 3+ years
- **Access Status**:
  -  Identifies private games
  - Detects uncopylocked/copylocked status
- **Progress Tracking**: Saves scan progress for resuming
- **Detailed Output**: Generates a formatted text file with game details

## Requirements

- Python 3.8+
- `requests` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RaccoonWX/Roblox-Vintage-Game-Finder.git
   cd Roblox-Vintage-Game-Finder
   ```

   2. Install dependencies:
   ``pip install requests``

## Usage

1. Configure settings in the script:
```
#Configuration
OUTPUT_FILE = "Classic Games List.txt"
START_ID = 1450  # Starting Place ID
RATE_LIMIT_DELAY = 2.0  # Seconds between requests
```

2. Run the script:
   ``python place-scraper.py``

3. View results in ``Classic Games List.txt``
