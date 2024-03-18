############################################################################################################
# Three helper functions to fetch audio features from Spotify API #
############################################################################################################

import requests
import pandas as pd
import time
import csv

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(auth_url, data=auth_data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        expiration_time = time.time() + response.json()['expires_in']
        return access_token, expiration_time
    else:
        print("Error fetching access token:", response.json())
        return None, None


def fetch_audio_features(url, access_token, output_csv_file):
    track_id = url.split('/')[-1]
    audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(audio_features_url, headers=headers)
    if response.status_code == 200:
        audio_features = response.json()
        if audio_features:
            audio_feature = audio_features
            # Log each available audio feature in the column, or log placeholder if feature is missing
            audio_feature_values = [
                audio_feature.get('id', None) if audio_feature else None,
                audio_feature.get('danceability', None) if audio_feature else None,
                audio_feature.get('energy', None) if audio_feature else None,
                audio_feature.get('key', None) if audio_feature else None,
                audio_feature.get('loudness', None) if audio_feature else None,
                audio_feature.get('mode', None) if audio_feature else None,
                audio_feature.get('speechiness', None) if audio_feature else None,
                audio_feature.get('acousticness', None) if audio_feature else None,
                audio_feature.get('instrumentalness', None) if audio_feature else None,
                audio_feature.get('liveness', None) if audio_feature else None,
                audio_feature.get('valence', None) if audio_feature else None,
                audio_feature.get('tempo', None) if audio_feature else None,
            ]
            # Write the audio feature values to the CSV file
            with open(output_csv_file, 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(audio_feature_values)
            return True
        else:
            print(f"No audio features found for URL: {url}")
            return False
    else:
        print(f"Error fetching audio features for {url}: {response.json()}")
        return False


def get_authorization_code(client_id, redirect_uri, scope):
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
    }
    response = requests.get(auth_url, params=params)

    if response.status_code == 200:
        # The user should log in and grant permission. The authorization code will be in the URL after the redirect.
        print("Redirect the user to the following URL to grant permission:")
        print(response.url)
        authorization_code = input("Enter the authorization code from the redirected URL: ")
        return authorization_code
    else:
        print(f"Error getting authorization code. Status code: {response.status_code}")
        print(f"Response content: {response.json()}")
        return None


############################################################################################################
# Replace the following with your client ID and client secret #
############################################################################################################

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

# Step 1: Get the initial access token using client ID and client secret
ACCESS_TOKEN, EXPIRATION_TIME = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)
if not ACCESS_TOKEN or not EXPIRATION_TIME:
    print("Failed to get the access token.")
    exit()

# Step 2: Read the data.csv file and get all unique URLs
data = pd.read_csv('data.csv')
data_us = data[data['Region'] == 'us']
unique_urls_us = set(data_us['URL'])


# # Step 3: Fetch audio features and log into audio_features.csv file
output_csv_file = 'audio_features.csv'  # Specify the CSV file path for logging

columns = [
    'track_id',
    'danceability',
    'energy',
    'key',
    'loudness',
    'mode',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
]

# Write the header row to the CSV file
with open(output_csv_file, 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(columns)

# Fetch audio features for each URL and log into the CSV file
for i, url in enumerate(unique_urls_us):
    success = fetch_audio_features(url, ACCESS_TOKEN, output_csv_file)
    time.sleep(1)  # Introduce a delay of 1 second between each request

    # Print progress every 100 URLs
    if (i + 1) % 100 == 0:
        print(f"Fetched audio features for {i + 1}/{len(unique_urls_us)} tracks.")

    # Auto-refresh the token every 3600 seconds (1 hour)
    if time.time() >= EXPIRATION_TIME:
        print("Access token has expired. Refreshing...")
        new_access_token, new_expiration_time = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)
        if new_access_token and new_expiration_time:
            ACCESS_TOKEN = new_access_token
            EXPIRATION_TIME = new_expiration_time
            print("Access token refreshed successfully.")
        else:
            print("Failed to refresh the access token.")
            break

print("All tracks fetched and logged to CSV file. Done!")