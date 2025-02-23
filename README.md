# Roblox Vintage Game Finder

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python script to discover and catalog classic Roblox games from 2006-2009 that meet specific criteria.

>[!CAUTION]
> ## Disclaimer
> This project is not affiliated with Roblox Corporation. Use at your own risk. Please respect Roblox's terms of service and API usage policies.

## Features

- **Vintage Game Detection**: Finds games created between 2006-2009
- **Activity Filtering**: Only includes games with 1000+ visits
- **Inactivity Check**: Filters games not updated in 3+ years
- **Access Status**:
  - Identifies private games **(Due to APIs, this feature does not work and will be removed in the next update.)**
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

## Output Format Examples
```
Place ID: 123456789
URL: https://www.roblox.com/games/123456789/
Title: Roblox Vintage Game Finder
Status: Public | Uncopylocked
Created: 2008-02-26T22:51:20.61Z
Last Updated: 2012-02-17T13:40:33.783Z
Visits: 1234567890
==================================================
```
```
Place ID: 123456789
URL: https://www.roblox.com/games/123456789/
Title: Roblox Vintage Game Finder
Status: Private | Uncopylocked
Created: 2008-02-26T22:51:20.61Z
Last Updated: 2012-02-17T13:40:33.783Z
Visits: 1234567890
==================================================
```
```
Place ID: 123456789
URL: https://www.roblox.com/games/123456789/
Title: Roblox Vintage Game Finder
Status: Public | Copylocked
Created: 2008-02-26T22:51:20.61Z
Last Updated: 2012-02-17T13:40:33.783Z
Visits: 1234567890
==================================================
```
```
Place ID: 123456789
URL: https://www.roblox.com/games/123456789/
Title: Roblox Vintage Game Finder
Status: Private | Copylocked
Created: 2008-02-26T22:51:20.61Z
Last Updated: 2012-02-17T13:40:33.783Z
Visits: 1234567890
==================================================
```
## Configuration

| Setting  |  Description  | Default Value |
| :------------ |:---------------| :-----|
| OUTPUT_FILE   | Output Text File Name | ``Classic Games List.txt`` |
| START_ID      | Starting Place ID for scanning |   ``1450`` |
| RATE_LIMIT_DELAY | Delay between API requests (seconds) |    ``2.0`` |

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (``git checkout -b user/YourRepositoryName``)
3. Commit your changes (``git commit -m 'Add some fixes or features.'``)
4. Push to the branch (``git push origin user/YourRepositoryName``)
5. Open a pull request

  ## License
  Distributed under the MIT License. See ``LICENSE`` for more information.
