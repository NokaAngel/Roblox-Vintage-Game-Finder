import requests
import time
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import signal
import sys

# Configuration
OUTPUT_FILE = "Enhanced Games List.txt"
PROGRESS_FILE = "scan_progress.json"
USER_AGENT = "Roblox Enhanced Game Finder/2.0 (+https://github.com/NokaAngel/Roblox-Vintage-Game-Finder)"
START_ID = 1450
RATE_LIMIT_DELAY = 2.0  # Delay per request per thread
MAX_WORKERS = 5  # Number of concurrent threads

session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Content-Type": "application/json"
})

rate_limit_lock = Lock()
last_request_time = 0.0
interrupted = False

def rate_limited_request(func, *args, **kwargs):
    global last_request_time
    with rate_limit_lock:
        elapsed = time.time() - last_request_time
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)
        result = func(*args, **kwargs)
        last_request_time = time.time()
    return result

def get_universe_id(place_id):
    try:
        response = rate_limited_request(session.get, f"https://apis.roblox.com/universes/v1/places/{place_id}/universe", timeout=15)
        if response.status_code == 200:
            return response.json().get("universeId")
    except:
        pass
    return None

def get_game_metadata(universe_id):
    try:
        response = rate_limited_request(session.get, f"https://games.roblox.com/v1/games?universeIds={universe_id}", timeout=15)
        if response.status_code == 200:
            data = response.json().get("data", [{}])[0]
            return data
    except:
        pass
    return {}

def get_place_details(place_id):
    try:
        response = rate_limited_request(session.post, "https://games.roblox.com/v1/games/multiget-place-details", json={"placeIds": [place_id]}, timeout=15)
        if response.status_code == 200:
            details = response.json()
            return details[0] if isinstance(details, list) and details else {}
    except:
        pass
    return {}

def get_thumbnails(universe_id):
    try:
        response = rate_limited_request(session.get, f"https://games.roblox.com/v1/games/icons?universeIds={universe_id}", timeout=15)
        if response.status_code == 200:
            return response.json().get("data", [{}])[0].get("imageUrl")
    except:
        pass
    return ""

def get_gamepasses(universe_id):
    try:
        response = rate_limited_request(session.get, f"https://games.roblox.com/v1/games/{universe_id}/game-passes", timeout=15)
        if response.status_code == 200:
            return response.json().get("data", [])
    except:
        pass
    return []

def get_game_details(place_id):
    universe_id = get_universe_id(place_id)
    if not universe_id:
        return None

    game_data = get_game_metadata(universe_id)
    place_data = get_place_details(place_id)
    game_data.update(place_data)
    game_data["thumbnail"] = get_thumbnails(universe_id)
    game_data["gamepasses"] = get_gamepasses(universe_id)
    game_data["rootPlaceId"] = place_id

    return game_data

def meets_criteria(game_data):
    try:
        created = datetime.fromisoformat(game_data.get("created", "").rstrip("Z"))
        updated = datetime.fromisoformat(game_data.get("updated", "").rstrip("Z"))
        visits = game_data.get("visits", 0)

        return (2006 <= created.year <= 2009 and (datetime.now().year - updated.year) >= 3 and visits >= 1000)
    except:
        return False

def save_progress(current_id, found_ids):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"current_id": current_id, "found_ids": found_ids}, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"current_id": START_ID, "found_ids": []}

def save_game_entry(place_id, game_data):
    entry = f"""Place ID: {place_id}
URL: https://www.roblox.com/games/{place_id}/
Title: {game_data.get('name', 'N/A')}
Status: {'Uncopylocked' if game_data.get('copyingAllowed') else 'Copylocked'}
Created: {game_data.get('created')}
Updated: {game_data.get('updated')}
Visits: {game_data.get('visits')}
Thumbnail: {game_data.get('thumbnail')}
Game Passes: {', '.join([gp.get('name') for gp in game_data.get('gamepasses', [])])}
{"="*50}\n\n"""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def process_id(place_id):
    print(f"[Worker] Scanning Place ID: {place_id}")
    game_data = get_game_details(place_id)
    if game_data and meets_criteria(game_data):
        save_game_entry(place_id, game_data)
        print(f"[Worker] Found: {game_data.get('name')} (ID: {place_id})")
        return place_id
    return None

def signal_handler(sig, frame):
    global interrupted
    print("\nSession ending. Waiting for workers to finish...")
    interrupted = True

def main():
    signal.signal(signal.SIGINT, signal_handler)

    progress = load_progress()
    current_id = progress["current_id"]
    found_ids = progress["found_ids"]

    try:
        while not interrupted:
            new_ids = []
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {executor.submit(process_id, pid): pid for pid in range(current_id, current_id + MAX_WORKERS)}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        new_ids.append(result)
            found_ids.extend(new_ids)
            current_id += MAX_WORKERS
            save_progress(current_id, found_ids)

    finally:
        save_progress(current_id, found_ids)
        print("Saved current position, and found IDs.")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("Enhanced Roblox Games List\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("="*50 + "\n\n")
    print("Enhanced Roblox Vintage Game Finder")
    main()
