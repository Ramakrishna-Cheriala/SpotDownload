import os
from fuzzywuzzy import fuzz


def search_song(song_name):
    # List all files in the folder
    files = os.listdir("downloaded_songs")

    # Calculate similarity score for each file name
    scores = [(file, fuzz.ratio(song_name.lower(), file.lower())) for file in files]

    # Sort files by similarity score
    scores.sort(key=lambda x: x[1], reverse=True)

    # Filter files with similarity score above a threshold
    threshold = 70  # Adjust threshold as needed
    filtered_files = [file for file, score in scores if score > threshold]

    return filtered_files


# Example usage:
song_name = input("Enter the name of the song: ")
matched_songs = search_song(song_name)

if matched_songs:
    print("Matching songs found:")
    for song in matched_songs:
        print(song)
else:
    print("No matching songs found.")
