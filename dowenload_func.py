import requests
import os
import time


headers = {
    "authority": "api.spotifydown.com",
    "method": "GET",
    "path": f"/download/{id}",
    "origin": "https://spotifydown.com",
    "referer": "https://spotifydown.com/",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-fetch-mode": "cors",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}


# Define the path to the downloaded songs folder
downloaded_songs_folder = "downloaded_songs"


def download_songs(id):

    session = requests.session()
    download_url = f"https://api.spotifydown.com/download/{id}"
    download_response = session.get(download_url, headers=headers)

    if download_response.status_code == 200:
        response_json = download_response.json()

        # Extract the download link
        download_link = response_json.get("link")
        song_name = response_json.get("metadata")["title"]
        # print(response_json)
        sanitized_track_id = "".join(
            x for x in song_name if x.isalnum() or x in [" ", "_", "-"]
        )

        # Check if the song file already exists in the downloaded songs folder
        song_file_path = os.path.join(
            downloaded_songs_folder, f"{sanitized_track_id}.mp3"
        )
        if os.path.exists(song_file_path):
            print("song is already downloaded")
            with open(song_file_path, "rb") as file:
                song_content = file.read()

            return song_content, sanitized_track_id
        else:
            song_download = session.get(download_link, headers=headers)

            if song_download.status_code == 200:
                # Save the downloaded song to the downloaded songs folder
                with open(song_file_path, "wb") as file:
                    file.write(song_download.content)
                return song_download.content, sanitized_track_id
    else:
        return None


def download_songs_1(id):

    session = requests.session()
    download_url = f"https://api.spotifydown.com/download/{id}"
    download_response = session.get(download_url, headers=headers)

    if download_response.status_code == 200:
        response_json = download_response.json()

        # Extract the download link
        download_link = response_json.get("link")
        song_name = response_json.get("metadata")["title"]
        # print(response_json)
        sanitized_track_id = "".join(
            x for x in song_name if x.isalnum() or x in [" ", "_", "-", "?"]
        )

        return download_link, sanitized_track_id
    else:
        return None
