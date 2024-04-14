import requests
from zipfile import ZipFile
from io import BytesIO
from telegram.constants import ChatAction
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from dowenload_func import download_songs, headers, download_songs_1
import os
from dotenv import load_dotenv

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


def download_new_command(update: Update, context):
    # Extract the link from the command arguments
    link = " ".join(context.args)

    # Send "typing" action to indicate bot is processing
    # context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Directly stream the file to the user
    with requests.get(link, stream=True) as response:
        if response.status_code == 200:
            # Send the file to the user
            context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=response.raw,
                filename="filename.extension",
            )
        else:
            update.message.reply_text("Error downloading file.")


async def download_from_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    chat_id = update.message.chat_id

    if "track" in url:
        await update.message.reply_text("Wait a moment.......")
        id = url.split("/")[-1].split("?si")[0]
        try:
            # song_file, song_name = download_songs(id)
            download_link, song_name = download_songs_1(id)
            #

            # Directly stream the file to the user
            with requests.get(download_link, stream=True) as response:
                await update.message.reply_text("Almost done.....")
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

                if response.status_code == 200:
                    # Send the file to the user
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=response.raw,
                        filename=f"{song_name}.mp3",
                    )
                else:
                    await update.message.reply_text("Error downloading file.")
            #
            # context.bot.send_document(chat_id, song_file, filename=f"{song_name}.mp3")
        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id, f"Failed to download song")
    elif "playlist" in url:
        id = url.split("/")[-1].split("?si")[0]
        update.message.reply_text("It may take some time, Come back later.....")
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
                        context.bot.send_document(
                            chat_id, song_file, filename=f"{song_name}.mp3"
                        )

                        count += 1
                    except Exception as e:
                        context.bot.send_message(
                            chat_id, f"Error downloading {name}: {e}"
                        )
                        continue

                offset = response_json.get("nextOffset")
            else:
                context.bot.send_message(chat_id, f"Error: {playlist_response.text}")
                break

        update.message.reply_text(f"{count-1} songs are ready to be played....")

    else:
        context.bot.send_message(
            chat_id, "Invalid URL. Please send a Spotify song or playlist URL."
        )


# Function to handle incoming messages
async def handle_message(update: Update, context):
    message = update.message
    message_type = message.chat.type
    text = message.text.lower()

    # if text.startswith("/start"):
    #     start_command(update, context)
    # elif text.startswith("/help"):
    #     help_command(update, context)
    # elif text.startswith("/stop"):
    #     start_command(update, context)
    # elif text.startswith("/download_new"):
    #     start_command(update, context)
    # else:
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

    # Get the dispatcher to register handlers
    # dispatcher = updater.dispatcher

    # Register command handlers
    # dispatcher.add_handler(CommandHandler("start", start_command))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(
    #     CommandHandler("download_new", download_new_command, pass_args=True)
    # )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
