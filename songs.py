import requests
from zipfile import ZipFile
from io import BytesIO
from dowenload_func import download_songs, headers, download_songs_1
import time


url = input("Enter a URL: ")
if "track" in url:

    id = url.split("/")[-1].split("?si")[0]
    try:
        song_file, song_name = download_songs(id)

        print(f"{song_name} downloaded successfully")
    except Exception as e:
        print(e)


elif "playlist" in url:
    id = url.split("/")[-1].split("?si")[0]
    playlist_url = f"https://api.spotifydown.com/trackList/playlist/{id}"
    count = 1

    downloaded_files = []

    offset = 0
    while offset is not None:
        playlist_response = requests.get(
            playlist_url, headers=headers, params={"offset": offset}
        )
        response_json = playlist_response.json()

        if playlist_response.status_code == 200:
            tracks = response_json.get("trackList")

            for track in tracks:
                track_id = track["id"]
                name = track["title"]
                try:
                    song_file, song_name = download_songs(track_id)

                    count += 1
                    print(f"{count}. {song_name} downloaded successfully")

                except Exception as e:
                    print(e)
                    continue

            offset = response_json.get("nextOffset")
        else:
            print("error")
            break


elif "album" in url:
    print("Album")
    id = url.split("/")[-1].split("?si")[0]
    album_url = f"https://api.spotifydown.com/trackList/album/{id}"
    count = 1

    album_results = requests.get(album_url, headers=headers)

    if album_results.status_code == 200:
        album_res = album_results.json()
        album_tracklist = album_res.get("trackList")
        # print(album_tracklist)

        for track in album_tracklist:

            track_id = track["id"]
            name = track["title"]
            print(name)
            try:
                song_file, song_name = download_songs(track_id)

                count += 1
                print(f"{count}. {song_name} downloaded successfully")
            except Exception as e:
                print(e)
                continue

    else:
        print("Error")
