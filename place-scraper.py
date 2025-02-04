import requests
import time
import json
import os
from datetime import datetime

# Configuration
OUTPUT_FILE = "Classic Games List.txt"
PROGRESS_FILE = "scan_progress.json"
USER_AGENT = "Roblox Vintage Game Finder/1.0 (+https://github.com/RaccoonWX/Roblox-Vintage-Game-Finder)"
START_ID = 1450
RATE_LIMIT_DELAY = 2.0
# End of Configuration

session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def get_universe_id(place_id):
    try:
        response = session.get(
            f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
            timeout=15
        )
        if response.status_code == 200:
            return response.json().get("universeId")
        return None
    except Exception as e:
        print(f"Universe ID error: {str(e)}")
        return None

def get_playability_status(place_id):
    """Get isPlayable status from multi-place-details endpoint"""
    try:
        response = session.post(
            "https://games.roblox.com/v1/games/multi-place-details",
            json={"placeIds": [place_id]},
            timeout=15
        )
        if response.status_code == 200:
            details = response.json()
            if details and isinstance(details, list) and len(details) > 0:
                return details[0].get("isPlayable", False)
        return False
    except Exception as e:
        print(f"Playability check error: {str(e)}")
        return False

def get_game_details(place_id):
    try:
        universe_id = get_universe_id(place_id)
        if not universe_id:
            return None

        # Get basic game info
        game_response = session.get(
            f"https://games.roblox.com/v1/games?universeIds={universe_id}",
            timeout=15
        )
        if game_response.status_code != 200:
            return None
            
        game_data = game_response.json().get("data", [{}])[0]
        
        # Get playability status
        game_data["isPlayable"] = get_playability_status(place_id) # I am aware of it saying "Private" when it is not, I am working on a fix for this.
        
        # Get copy permission status
        place_response = session.get(
            f"https://develop.roblox.com/v1/places/{place_id}",
            timeout=15
        )
        if place_response.status_code == 200:
            place_info = place_response.json()
            game_data["copyingAllowed"] = place_info.get("copyingAllowed", False) # This tells you whether the game can be copied to Studio or not.
        
        return game_data
    except Exception as e:
        print(f"Game detail error: {str(e)}")
        return None

def meets_criteria(game_data):
    try:
        created = datetime.fromisoformat(game_data["created"].rstrip("Z"))
        updated = datetime.fromisoformat(game_data["updated"].rstrip("Z"))
        visits = game_data.get("visits", 0)
        
        return (2006 <= created.year <= 2009 and
                (datetime.now().year - updated.year) >= 3 and
                visits >= 1000)
    except KeyError:
        return False

def get_access_status(game_data):
    """Determine game accessibility status"""
    status = []
    
    if not game_data.get("isPlayable", False):
        status.append("Private")
        
    status.append("Uncopylocked" if game_data.get("copyingAllowed", False) else "Copylocked")
        
    return " | ".join(status)

def save_progress(current_id, found_ids):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({
            "current_id": current_id,
            "found_ids": found_ids
        }, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"current_id": START_ID, "found_ids": []}

def save_game_entry(place_id, game_data):
    access_status = get_access_status(game_data)
    
    entry = f"""Place ID: {place_id}
URL: https://www.roblox.com/games/{place_id}/
Title: {game_data.get('name', 'N/A')}
Status: {access_status}
Created: {game_data.get('created', 'N/A')}
Last Updated: {game_data.get('updated', 'N/A')}
Visits: {game_data.get('visits', 'N/A')}
{"="*50}\n\n"""

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def main():
    progress = load_progress()
    current_id = progress["current_id"]
    found_ids = progress["found_ids"]
    
    try:
        while True:
            print(f"Checking ID: {current_id} | Found: {len(found_ids)}", end="\r")
            
            game_data = get_game_details(current_id)
            
            if game_data and meets_criteria(game_data):
                found_ids.append(current_id)
                access_status = get_access_status(game_data)
                save_game_entry(current_id, game_data)
                print(f"\n Found: {game_data.get('name', 'Unknown')} (ID: {current_id})")
                print(f"   Status: {access_status}")
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
