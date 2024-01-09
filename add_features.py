import json
import requests
import time
import logging
import os
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
access_token = None
token_expiry_time = None
def request_spotify_access_token(client_id,client_secret):
    global access_token, token_expiry_time
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    data = response.json()
    access_token = data['access_token']
    # Refresh token every 50 minutes (3000 seconds)
    token_expiry_time = time.time() + 3000

def check_token_refresh():
    global access_token, token_expiry_time
    if not access_token or time.time() > token_expiry_time:
        logging.info("Refreshing Spotify access token...")
        request_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))

def get_audio_analysis(track_id):
    
    check_token_refresh()
    url = f'https://api.spotify.com/v1/audio-analysis/{track_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error retrieving audio analysis for track {track_id}: {e}")
        return None

def get_audio_features_track(track_id):
    
    check_token_refresh()
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error retrieving audio features for track {track_id}: {e}")
        return None
def get_recommended_tracks(seed_artists, seed_tracks, access_token, limit=5):
    
    seed_artists = ",".join(seed_artists)
    seed_tracks = ",".join(seed_tracks)
    url = f'https://api.spotify.com/v1/recommendations?limit={limit}&seed_artists={seed_artists}&seed_tracks={seed_tracks}'
    
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            # Handle rate limit exceeded
            retry_after = int(response.headers.get("Retry-After", 60))
            logging.info(f"Rate limit reached. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return get_recommended_tracks(seed_artists, seed_tracks, access_token)
        else:
            logging.error(f"Error fetching recommended tracks: {e}")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
    return []

def process_tracks(tracks):
    batch_to_save = []
    
    for index, track in enumerate(tracks):

        

        check_token_refresh()  
        random_index = random.randint(2,4)
        if index % random_index == 0 and index > 0:
            logging.info('Waiting to manage API rate limit...')
            api_rate_limit_delay = random.randint(180, 700)
            time.sleep(api_rate_limit_delay)
        
        track_id = track['track']["id"]
        artist_id = track['track']['artists'][0]["id"]
        recommendations = get_recommended_tracks([artist_id], [track_id], access_token)
        track['recommendations'] = recommendations
        
        batch_to_save.append(track)  # Add the processed track to the batch

        # Save the batch every 50 tracks
        if (index + 1) % 50 == 0 or (index + 1) == len(tracks):
            with open('saved_tracks_progress1.json', 'a') as file:
                json.dump(batch_to_save, file, indent=4)
            logging.info(f"Progress saved after processing {index + 1} tracks.")
            batch_to_save.clear()  # Clear the batch for the next set of tracks

    return tracks




def main():
    request_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
    with open("saved_tracks.json", 'r') as file:
        tracks = json.load(file)
    processed_tracks = process_tracks(tracks)
    with open('saved_tracks.json', 'w') as file:
        json.dump(processed_tracks, file, indent=4)

if __name__ == "__main__":
    main()

