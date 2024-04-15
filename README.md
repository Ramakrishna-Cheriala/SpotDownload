## Prerequisites
```
python -m venv .venv
source ./.venv/bin/activate
pip install requirements.txt
```

## How to Run

```
python bot.py
```

## TODOS:
1. Create 2 files spotify.py & telegram_bot.py with clear responsibilites
    
    > spotify.py - code specific to downloading files, sending requests etc.
    >
    > telegram_bot.py - code specific to run the bot.

2. Find a better way to streamline files to reduce load on server.

3. Find a way to save the files to specific folder in user's device ex. /Downloads/Telegram/Spot/

4. Add handler "/download_new <play_list_link>" which downloads only newly added songs 