from telethon import TelegramClient, events
from datetime import datetime
import os

api_id =   # ← appid here
api_hash =   # api hash here
session_name = 'incoming_listener'

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_name = sender.username or sender.first_name or "Unknown"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if event.message.message:
        log_line = f"[{timestamp}] From {sender_name}: {event.message.message}\n"
        if not os.path.exists(f"{sender_name}/"): os.mkdir(f"{sender_name}")
        with open(f"{sender_name}/incoming_messages_live.txt", "a", encoding="utf-8") as file:
            file.write(log_line)
        print(log_line.strip())

    if event.message.media:
        if not os.path.exists(f"{sender_name}/"): os.mkdir(f"{sender_name}")
        file_path = await event.download_media(file=f"{sender_name}/media")
        log_line = f"[{timestamp}] From {sender_name}: [Media saved: {file_path}]\n"
        with open("incoming_messages_live.txt", "a", encoding="utf-8") as file:
            file.write(log_line)
        print(log_line.strip()) 

print("Wait")
client.start()
client.run_until_disconnected()
