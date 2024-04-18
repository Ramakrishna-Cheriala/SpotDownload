import os
import requests


base_url = "https://api.spotifydown.com/"

download_url = base_url + "download/{track_id}"
metadata_url = base_url + "metadata/track/{track_id}"
playlist_url = "https://api.spotifydown.com/trackList/playlist/{playlist_id}"
album_url = "https://api.spotifydown.com/trackList/album/{album_id}"
headers = {
    "authority": "api.spotifydown.com",
    "method": "GET",
    "origin": "https://spotifydown.com",
    "referer": "https://spotifydown.com/",
    # "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    # "sec-fetch-mode": "cors",
}



headers2 =  {
    # "accept: */*",
    # "accept-language: en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": "Bearer BQA9zpbhygl6XO8Ro1E4FXUypIZyw_f_xzR6IDFhK-3xdG7GPrrxu6vK_uuHFqrV_OmetdUYxYTQTCjk5nwDjWfBt9ujwXnLuE-Tb9yGwFgd3Dheaa0_gy_Gsa4JmYEn7xzYx9y8HyIPWwe3tHn1CwIdK7BJiwgMPcNy43WKIgNObDks2fHctHj8goRd742lcTvAmLNFSc78WLCepEEPzimZJB_KA23eKws6uDsuGjKM2wfh3lo9HL1CZZKuPDgTCglvWIC50cjCFwrO4lBz0Gz2ThPVCnRr3bNqoW_1wyOIW_KxmcN4YqFbGfiLSuJ1MMTBOWKLufr10y9vrBO4Jz0",
    "origin": "https://developer.spotify.com",
    "referer": "https://developer.spotify.com/",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}


# dataclass
# class Track:
#     id
#     title
#     artists
#     album
#     spotify_link
#     amazon_link
#     apple_link

def is_spotify_url(text):
    if "spotify" in text and ("track" in text or "playlist" in text or "album" in text):
        return True
    return False


def get_metadata(track_id):
    response = requests.get(metadata_url.format(track_id=track_id),headers=headers)
    metadata = dict(response.json())

    del metadata['cache']
    del metadata['success']

    return metadata

def get_download_link(track_id):
    download_response = requests.get(download_url.format(track_id=track_id), headers=headers)

    if download_response.status_code == 200:
        response_json = download_response.json()

        # Extract the download link
        download_link = response_json.get("link")
        song_name = response_json.get("metadata")["title"]
        print(response_json)
        return download_link
    else:
        return None


def get_list_of_tracks(id, type="playlist"):
    if type == "playlist":
        url = playlist_url.format(playlist_id=id)
    elif type == "album":
        url = album_url.format(album_id=id)
    
    track_list = []
    offset = 0
    while offset is not None:
        playlist_response = requests.get(
            url, headers=headers, params={"offset": offset}
        )
        response_json = playlist_response.json()

        if playlist_response.status_code == 200:
            tracks = response_json.get("trackList")

            for track in tracks:
                track_id = track["id"]
                name = f"{sanitize_name(track["title"])}.mp3"
                track_list.append({"track_id": track_id, "title": name})

            offset = response_json.get("nextOffset")
        else:
            print("Error: get tracks from playlist failed")
            break
    
    return track_list

def download_track(track_id):
    pass

def download_playlist(playlist_id):
    pass

def save_to_cache(file_name, contents, folder="./cache/"):
    with open(os.path.join(folder, file_name), 'w+b') as f:
        f.write(contents)

def is_cached(file_name, folder="./cache/"):
    if os.path.exists(os.path.join(folder, file_name)):
        print("File already present:", file_name)
        return True
    return False

def sanitize_name(file_name):
    # Replace invalid characters with underscores
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        file_name = file_name.replace(char, '_')
    return file_name
