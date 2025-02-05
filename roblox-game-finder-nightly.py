import requests
import time
import json
import os
from datetime import datetime

# Configuration
OUTPUT_FILE = "Classic Games List.txt"
PROGRESS_FILE = "scan_progress.json"
USER_AGENT = "Roblox Vintage Game Finder/2.0 (+https://github.com/RaccoonWX/Roblox-Vintage-Game-Finder)"
START_ID = 1450  # Test with known classic game ID
RATE_LIMIT_DELAY = 5.0  # Increased delay to prevent rate limiting

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
    """Get playability status from multiget-place-details endpoint"""
    try:
        response = session.post(
            "https://games.roblox.com/v1/games/multiget-place-details",
            json={"placeIds": [place_id]},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            for detail in data.get("placeDetails", []):
                if str(detail.get("placeId")) == str(place_id):
                    return {
                        "isPlayable": detail.get("isPlayable", False),
                        "reason": detail.get("reasonProhibited", "None")
                    }
        return {"isPlayable": False, "reason": "Not Found"}
    except Exception as e:
        print(f"Playability check error: {str(e)}")
        return {"isPlayable": False, "reason": "Error"}

def get_game_details(place_id):
    try:
        # First get basic playability status
        playability = get_playability_status(place_id)
        
        # Get universe ID
        universe_id = get_universe_id(place_id)
        
        # Get game info
        game_data = {"isPlayable": playability["isPlayable"]}
        
        if universe_id:
            # Get detailed game information including copying status
            game_response = session.get(
                f"https://games.roblox.com/v2/games?universeIds={universe_id}",
                timeout=15
            )
            if game_response.status_code == 200:
                game_info = game_response.json().get("data", [{}])[0]
                game_data.update({
                    "name": game_info.get("name"),
                    "created": game_info.get("created"),
                    "updated": game_info.get("updated"),
                    "visits": game_info.get("visits", 0),
                    "copyingAllowed": game_info.get("allowCopying", False)  # Updated field name
                })

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
    """Determine game accessibility status with detailed reasons"""
    status = []
    
    if game_data.get("isPlayable", False):
        status.append("Public")
    else:
        reason = game_data.get("reason", "Unknown")
        status.append(f"Private ({reason})")
    
    if "allowCopying" in game_data:
        status.append("Uncopylocked" if game_data["allowCopying"] else "Copylocked")
    else:
        status.append("Copy Status Unknown")
        
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
                print(f"\nFound: {game_data.get('name', 'Unknown')} (ID: {current_id})")
                print(f"   Status: {access_status}")
                print(f"   Visits: {game_data.get('visits', 'N/A')}")
                print(f"   Last Updated: {game_data.get('updated', 'N/A')}")
                
            save_progress(current_id + 1, found_ids)
            current_id += 1
            time.sleep(RATE_LIMIT_DELAY)
            
    except KeyboardInterrupt:
        print("\n\nScan paused. Progress saved.")
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