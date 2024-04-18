import sys
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
from spotify import download_playlist, download_track, get_download_link, get_list_of_tracks, get_metadata, is_cached, is_spotify_url, sanitize_name, save_to_cache

load_dotenv()

TOKEN = os.getenv("TOKEN")

# Function to handle the /start command
async def start_command(update: Update, context):
    await update.message.reply_text("Enter url of a song or a playlist to download...")


# Function to handle the /help command
async def help_command(update: Update, context):
    await update.message.reply_text("Download Spotify songs or playlist...")

# Function to handle the /stop command
async def stop_command(update: Update, context):
    await update.message.reply_text("Stopping the bot...")
    context.bot.stop()

# Function to handle incoming messages
async def handle_message(update: Update, context):
    message = update.message
    message_type = message.chat.type
    text = message.text

    if is_spotify_url(text):
        await download_spotify(update, context)

async def download_spotify(update, context):
    url = update.message.text
    if "playlist" in url:
        playlist_id = url.split("/")[-1].split("?si")[0]
        tracks_list = get_list_of_tracks(playlist_id, "playlist")
        for track in tracks_list:
            await download_spotify_track(update, context, track['track_id'], track['title'])
    elif "album" in url:
        album_id = url.split("/")[-1].split("?si")[0]
        tracks_list = get_list_of_tracks(album_id, "album")
        for track in tracks_list:
            await download_spotify_track(update, context, track['track_id'], track['title'])
    elif "track" in url:
        track_id = url.split("/")[-1].split("?si")[0]
        await download_spotify_track(update, context, track_id)

async def download_spotify_track(update, context, track_id, title=None):
    await update.message.reply_text("Wait a moment.......")

    song_name = title or f"{sanitize_name(get_metadata(track_id)['title'])}.mp3"
    print(song_name)
        
    if is_cached(song_name):
        await update.message.reply_text("from cache on server")
        print(f"{song_name} is already in cache")
        await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=f"./cache/{song_name}",
                        filename=f"{song_name}",
                    )
        return
    try:
        download_link = get_download_link(track_id)
        print(download_link)
        # Directly stream the file to the user
        with requests.get(download_link, stream=True) as response:
            await update.message.reply_text("Almost done.....")
            # await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

            if response.status_code == 200:
                    # Send the file to the user
                await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=response.content,
                        filename=f"{song_name}",
                    )
                save_to_cache(f"{song_name}", response.content)

            else:
                await update.message.reply_text("Error downloading file.")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        await context.bot.send_message(update.effective_chat.id, f"Failed to download song")



if __name__ == "__main__":
    print("Starting Bot...")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))


    application.run_polling(allowed_updates=Update.ALL_TYPES)
