import os
import logging
from urllib.parse import urlencode

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_authorization_url(client_id, redirect_uri, scope, auth_url):
    
    auth_data = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri
    }
    return f"{auth_url}?{urlencode(auth_data)}"

def main():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    if not client_id:
        logging.error("Client ID not found. Set the SPOTIFY_CLIENT_ID environment variable.")
        return

    redirect_uri = 'http://localhost:8080/callback'
    scope = "user-library-read"
    auth_url = 'https://accounts.spotify.com/authorize'
    
    authorization_url = get_authorization_url(client_id, redirect_uri, scope, auth_url)
    logging.info(f"Authorization URL: {authorization_url}")

if __name__ == "__main__":
    main()


