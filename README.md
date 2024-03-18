# spotify-data-request

## Introduction

This script is designed to help users fetch audio features for tracks from Spotify using their unique URLs. It interacts with the Spotify API to retrieve data on various attributes of each track, such as danceability, energy, tempo, etc.

Important Note: Before using this script, ensure you have obtained the necessary access credentials from the Spotify Developer Portal, as this script does not handle the authorization process.

## Requirements

Before using this script, ensure you have the following Python modules installed:

- **requests**: This module is used for making HTTP requests to the Spotify API to fetch data.
- **pandas**: Pandas is a powerful data manipulation library. It is used in this script for reading and processing data from CSV files.
- **csv**: The csv module provides functionality to read from and write to CSV files, which is essential for logging audio features data.

You can install these modules using pip. For example:

```bash
pip install requests pandas
```

## Functions

The script contains three main functions:

`get_spotify_access_token(client_id, client_secret)`: This function retrieves the access token required for interacting with the Spotify API, as suggested by their latest API document. It takes the client ID and client secret as input parameters.

`fetch_audio_features(url, access_token, output_csv_file)`: This function fetches the audio features for each track identified by its URL and logs the data into a CSV file. It requires the URL of the track, the access token obtained from Spotify, and the path to the output CSV file.

`get_authorization_code(client_id, redirect_uri, scope)`: This function assists in obtaining the authorization code required for accessing user data through the Spotify API.

## Usage

1. Ensure you have obtained your Client ID and Client Secret from the Spotify Developer Portal.

2. Replace the placeholders with your actual Client ID and Client Secret in the script:

```python
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
```

3. Make sure you have a CSV file named `data.csv` containing the URLs of the tracks you want to fetch audio features for.

4. Run the script. It will automatically handle the process of obtaining an access token, fetching audio features for each track, and logging the data into a CSV file named audio_features.csv.

## Steps

Step 1: Get the initial access token using client ID and client secret

Step 2: Read the data.csv file and get all unique URLs

Step 3: Fetch audio features and log into audio_features.csv file

Step 4: Write the header row to the CSV file

Step 5: Fetch audio features for each URL and log into the CSV file

## License
This script is licensed under the MIT License.
