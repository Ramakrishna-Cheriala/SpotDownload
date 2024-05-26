import requests
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


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
downloaded_songs_folder = "Songs"

if not os.path.exists(downloaded_songs_folder):
    os.makedirs(downloaded_songs_folder)


def download_songs(id):

    session = requests.session()
    download_url = f"https://api.spotifydown.com/download/{id}"
    download_response = session.get(download_url, headers=headers)

    if download_response.status_code == 200:
        response_json = download_response.json()

        # Extract the download link
        download_link = response_json.get("link")
        song_name = response_json.get("metadata")["title"]
        cover_url = response_json.get("metadata").get("cover")
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

                if cover_url:
                    add_cover_image_to_mp3(song_file_path, cover_url, session)
                return song_download.content, sanitized_track_id
    else:
        return None


def add_cover_image_to_mp3(file_path, cover_url, session):
    try:
        # Download the cover image
        image_response = session.get(cover_url, headers=headers)
        if image_response.status_code == 200:
            # Load the MP3 file
            audio = MP3(file_path, ID3=ID3)

            # Add ID3 tag if not present
            try:
                audio.add_tags()
            except error:
                pass

            # Add the cover image
            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime="image/jpeg",  # image mime type
                    type=3,  # 3 is for the cover image
                    desc="Cover",
                    data=image_response.content,
                )
            )

            # Save the updated tags
            audio.save()
            print(f"Cover image added to {file_path}")

    except Exception as e:
        print(f"Error adding cover image: {e}")


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
