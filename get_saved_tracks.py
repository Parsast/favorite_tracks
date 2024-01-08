import json
import requests
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_saved_tracks(access_token, url):
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching saved tracks: {e}")
    return None

def main():
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not access_token:
        logging.error("Access token not found. Set the SPOTIFY_ACCESS_TOKEN environment variable.")
        return

    url = 'https://api.spotify.com/v1/me/tracks?market=ca&limit=50'
    all_tracks = []
    while url:
        response = get_saved_tracks(access_token, url)
        if response:
            all_tracks.extend(response.get("items", []))
            url = response.get("next")
        else:
            break

    with open('saved_tracks.json', 'w') as file:
        json.dump(all_tracks, file, indent=4)
    logging.info("Saved tracks written to file.")

if __name__ == "__main__":
    main()
