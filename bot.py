import requests
from zipfile import ZipFile
from io import BytesIO
from telegram.constants import ChatAction
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
)
from dowenload_func import download_songs, headers, download_songs_1
import os
from dotenv import load_dotenv
import time

load_dotenv()

TOKEN = os.getenv("TOKEN")


# Function to handle the /start command
async def start_command(update: Update, context):
    await update.message.reply_text("Enter url of a song or a playlist to download...")


# Function to handle the /help command
async def help_command(update: Update, context):
    await update.message.reply_text("Download Spotify songs or playlist...")


async def stop_command(update: Update, context):
    await update.message.reply_text("Stopping the bot...")
    context.bot.stop()


async def download_from_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    chat_id = update.message.chat_id

    if "track" in url:
        await update.message.reply_text("Wait a moment.......")
        id = url.split("/")[-1].split("?si")[0]
        start_time = time.time()
        try:
            song_file, song_name = download_songs(id)

            await context.bot.send_document(
                chat_id, song_file, filename=f"{song_name}.mp3"
            )
            end_time = time.time()
            print(f"Time taken to send the file: {(end_time - start_time)} seconds")
        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id, f"Failed to download song")

    elif "playlist" in url:
        id = url.split("/")[-1].split("?si")[0]
        await update.message.reply_text("It may take some time, Come back later.....")
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
                        await context.bot.send_document(
                            chat_id, song_file, filename=f"{song_name}.mp3"
                        )

                        count += 1
                    except Exception as e:
                        await context.bot.send_message(
                            chat_id, f"Error downloading {name}: {e}"
                        )
                        continue

                offset = response_json.get("nextOffset")
            else:
                await context.bot.send_message(
                    chat_id, f"Error: {playlist_response.text}"
                )
                break

        await update.message.reply_text(f"{count-1} songs are ready to be played....")

    elif "album" in url:
        print("Album")
        id = url.split("/")[-1].split("?si")[0]
        await update.message.reply_text("It may take some time, Come back later.....")
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
                    await context.bot.send_document(
                        chat_id, song_file, filename=f"{song_name}.mp3"
                    )

                    count += 1
                except Exception as e:
                    await context.bot.send_message(
                        chat_id, f"Error downloading {name}: {e}"
                    )
                    continue

        else:
            print("Error")

        await update.message.reply_text(f"{count-1} songs are ready to be played....")

    else:
        context.bot.send_message(
            chat_id, "Invalid URL. Please send a Spotify song or playlist URL."
        )


# Function to handle incoming messages
async def handle_message(update: Update, context):
    message = update.message
    message_type = message.chat.type
    text = message.text.lower()
    await download_from_url(update, context)


if __name__ == "__main__":
    print("Starting Bot...")
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


"""
https://music.apple.com/in/album/rangasthalam-original-motion-picture-soundtrack/1359132636
"""
