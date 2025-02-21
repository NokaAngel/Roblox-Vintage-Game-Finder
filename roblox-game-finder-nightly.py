import requests
import time
import json
import os
from datetime import datetime

# Configuration
OUTPUT_FILE = "Classic Games List.txt"
PROGRESS_FILE = "scan_progress.json"
USER_AGENT = "Roblox Vintage Game Finder/2.0 (+https://github.com/NokaAngel/Roblox-Vintage-Game-Finder)"
START_ID = 1450
RATE_LIMIT_DELAY = 2.0

session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def get_universe_id(place_id):
    """Fetch the universe ID for a given place ID."""
    try:
        response = session.get(
            f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
            timeout=15
        )
        if response.status_code == 200:
            return response.json().get("universeId")
        print(f"Failed to get universe ID for place {place_id}: {response.status_code} {response.text}")
        return None
    except Exception as e:
        print(f"Universe ID error: {str(e)}")
        return None

def get_game_details(place_id):
    """Retrieve game information including creator and copy status."""
    try:
        universe_id = get_universe_id(place_id)
        if not universe_id:
            return None

        # Get basic game info including creator
        game_response = session.get(
            f"https://games.roblox.com/v1/games?universeIds={universe_id}",
            timeout=15
        )
        if game_response.status_code != 200:
            print(f"Failed to get game info for universe {universe_id}: {game_response.status_code} {game_response.text}")
            return None
            
        game_data = game_response.json().get("data", [{}])[0]
        
        # Get copy permission status
        place_response = session.get(
            f"https://develop.roblox.com/v1/places/{place_id}",
            timeout=15
        )
        if place_response.status_code == 200:
            place_info = place_response.json()
            game_data["copyingAllowed"] = place_info.get("copyingAllowed", False)
        else:
            game_data["copyingAllowed"] = None  # Default to None if not retrievable
        
        return game_data
    except Exception as e:
        print(f"Game detail error: {str(e)}")
        return None

def meets_criteria(game_data):
    """Check if the game meets the vintage criteria."""
    try:
        created = datetime.fromisoformat(game_data["created"].rstrip("Z"))
        updated = datetime.fromisoformat(game_data["updated"].rstrip("Z"))
        visits = game_data.get("visits", 0)
        
        return (2006 <= created.year <= 2009 and
                (datetime.now().year - updated.year) >= 3 and
                visits >= 1000)
    except KeyError:
        return False

def get_copy_status(game_data):
    """Determine game copy status (copylocked or uncopylocked)."""
    return "Uncopylocked" if game_data.get("copyingAllowed", False) else "Copylocked"

def save_progress(current_id, found_ids):
    """Save the current scan progress to a JSON file."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump({
            "current_id": current_id,
            "found_ids": found_ids
        }, f)

def load_progress():
    """Load the scan progress from a JSON file, or return default values."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"current_id": START_ID, "found_ids": []}

def save_game_entry(place_id, game_data):
    """Save a game entry to the output file with creator information."""
    copy_status = get_copy_status(game_data)
    creator_name = game_data.get("creator", {}).get("name", "Unknown")
    
    entry = f"""Place ID: {place_id}
URL: https://www.roblox.com/games/{place_id}/
Title: {game_data.get('name', 'N/A')}
Creator: {creator_name}
Copy Status: {copy_status}
Created: {game_data.get('created', 'N/A')}
Last Updated: {game_data.get('updated', 'N/A')}
Visits: {game_data.get('visits', 'N/A')}
{"="*50}\n\n"""

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def main():
    """Main function to run the vintage game finder."""
    progress = load_progress()
    current_id = progress["current_id"]
    found_ids = progress["found_ids"]
    
    try:
        while True:
            print(f"Checking ID: {current_id} | Found: {len(found_ids)}", end="\r")
            
            game_data = get_game_details(current_id)
            
            if game_data and meets_criteria(game_data):
                found_ids.append(current_id)
                copy_status = get_copy_status(game_data)
                creator_name = game_data.get("creator", {}).get("name", "Unknown")
                save_game_entry(current_id, game_data)
                print(f"\n Found: {game_data.get('name', 'Unknown')} (ID: {current_id})")
                print(f"   Creator: {creator_name}")
                print(f"   Copy Status: {copy_status}")
                print(f"   Visits: {game_data.get('visits', 'N/A')}")
                print(f"   Last Updated: {game_data.get('updated', 'N/A')}")
                
            save_progress(current_id + 1, found_ids)
            current_id += 1
            time.sleep(RATE_LIMIT_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n Scan paused. Progress saved.")
    finally:
        save_progress(current_id, found_ids)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("Vintage Roblox Games List\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("="*50 + "\n\n")
    
    print("Roblox Vintage Game Finder")
    print(f"Starting from ID: {START_ID}")
    print(f"User Agent: {USER_AGENT}")
    print("Press Ctrl+C to pause/exit\n")
    main()
