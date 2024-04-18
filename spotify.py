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

# curl "https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n" ^
#   -H "accept: */*" ^
#   -H "accept-language: en-GB,en-US;q=0.9,en;q=0.8" ^
#   -H "authorization: Bearer BQAGbWA_13NgpocCS3R9Pgy0ja37kr1Is-nFZk4iGo3GTh0MEDtyJ9YVJ80lZXPk61-1RqxAaYRQm26tIHvKUkyL0LxCCgN91KeUpvZ5eNt0_HXDpn3KgHkgSa4XbwFc2XtcIpuvOWxaZN5-twSJ42KnTC-vs3fxenpgWoKb56sO7CRHJUqshGejvRlbamuOYQ2gQoN1vwKSkHDK2KOsfTFx9UcjvG8Hxu1m-E2zXLkI-QtBf0vbGyCzLGicX9grFz8G70lnbPYhF2VMisM0I2-lmEUZtSBV2cqpR-YK6EqTQHv4G9Cl1M1WxyazZhezlsSxz1sqF1JnexuxQnlwso0" ^
#   -H "origin: https://developer.spotify.com" ^
#   -H "referer: https://developer.spotify.com/" ^
#   -H ^"sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"123^\^", ^\^"Not:A-Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"123^\^"^" ^
#   -H "sec-ch-ua-mobile: ?0" ^
#   -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
#   -H "sec-fetch-dest: empty" ^
#   -H "sec-fetch-mode: cors" ^
#   -H "sec-fetch-site: same-site" ^
#   -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
import os
import requests
# https://open.spotify.com/track/1e6r9GfyjrTUqmKohbswQn?si=d725120f083f4c97
# id = "1e6r9GfyjrTUqmKohbswQn"


# session = requests.session()
# # response = requests.get(metadata_url.format(track_id=id), headers=headers)4

# query = "3cEYpjA9oz9GiPac4AsH4n"
# query2 = "413oJ4fRleVTs960hi5Iay"
# response = requests.get(f"https://api.spotifydown.com/trackList/playlist/54iRx6maCgstfBisLsUOSK", headers=headers)


# print(response.json())

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

# def download_from_link(link):
#     if "track" in url:
#         # await update.message.reply_text("Wait a moment.......")
#         # now = time.time()
#         id = url.split("/")[-1].split("?si")[0]
#         try:
#             # song_file, song_name = download_songs(id)
#             download_link, song_name = download_songs_1(id)
#             #

#             # Directly stream the file to the user
#             with requests.get(download_link, stream=True) as response:
#                 await update.message.reply_text("Almost done.....")
#                 # print(response.json())
#                 ca = time.time()
#                 await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
#                 await update.message.reply_text(f"ca - {time.time()-ca}")

#                 if response.status_code == 200:
#                     # Send the file to the user
#                     await context.bot.send_document(
#                         chat_id=update.effective_chat.id,
#                         document=response.raw,
#                         filename=f"{song_name}.mp3",
#                     )
#                     await update.message.reply_text(f"21 - {time.time()-now}")

#                 else:
#                     await update.message.reply_text("Error downloading file.")
#             #
#             # context.bot.send_document(chat_id, song_file, filename=f"{song_name}.mp3")
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             await context.bot.send_message(chat_id, f"Failed to download song")
#     elif "playlist" in url:
#         id = url.split("/")[-1].split("?si")[0]
#         update.message.reply_text("It may take some time, Come back later.....")
#         playlist_url = f"https://api.spotifydown.com/trackList/playlist/{id}"
#         count = 1
#         downloaded_files = []

#         offset = 0
#         while offset is not None:
#             playlist_response = requests.get(
#                 playlist_url, headers=headers, params={"offset": offset}
#             )
#             response_json = playlist_response.json()

#             if playlist_response.status_code == 200:
#                 tracks = response_json.get("trackList")

#                 for track in tracks:
#                     track_id = track["id"]
#                     name = track["title"]
#                     try:
#                         song_file, song_name = download_songs(track_id)
#                         context.bot.send_document(
#                             chat_id, song_file, filename=f"{song_name}.mp3"
#                         )

#                         count += 1
#                     except Exception as e:
#                         context.bot.send_message(
#                             chat_id, f"Error downloading {name}: {e}"
#                         )
#                         continue

#                 offset = response_json.get("nextOffset")
#             else:
#                 context.bot.send_message(chat_id, f"Error: {playlist_response.text}")
#                 break

#         update.message.reply_text(f"{count-1} songs are ready to be played....")
#     else:
#         context.bot.send_message(
#             chat_id, "Invalid URL. Please send a Spotify song or playlist URL."
#         )

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
