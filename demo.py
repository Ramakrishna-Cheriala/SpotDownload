import requests
import os

# Define headers
headers = {
    "method": "GET",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-fetch-mode": "cors",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}

vides_folder = "dowenloaded_videos"

youtube_url = input("Enter youtube url: ")

url = f"https://yt-cw.fabdl.com/youtube/get?url={youtube_url}&mp3_task=2"

# Send request with headers
res = requests.get(url, headers=headers)

if res.status_code == 200:
    res_json = res.json()
    title = res_json.get("result").get("title").split("|")[0]
    videos = res_json.get("result").get("videos")

    sanitized_track_id = "".join(
        x for x in title if x.isalnum() or x in [" ", "_", "-"]
    )

    # print(sanitized_track_id)
    if videos:
        download_url = videos[0].get("cdn_url")
        type = videos[0].get("type")
        # print(download_url)
        if download_url:
            print("1")
            print("Download started")

            video_download = requests.get(download_url, headers=headers)
            print("2")
            path = os.path.join(vides_folder, f"{sanitized_track_id}.{type}")
            if os.path.exists(path):
                print(
                    f"The file {sanitized_track_id}.{type} already exists in the folder."
                )
            else:
                print("3")
                if video_download.status_code == 200:
                    with open(path, "wb") as file:
                        file.write(video_download.content)
                    print("Download finished")
        else:
            print("No download url specified")

    else:
        print("No video found in the response.")
else:
    print("Failed to fetch data from the server.")
