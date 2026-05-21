import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load environment variables from the .env file
load_dotenv()

# Fetch credentials from environment variables
# API_ID must be cast to an integer for Telethon
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
DESTINATION = os.getenv('DESTINATION')

raw_keywords = os.getenv('KEYWORDS', '')
KEYWORDS = [k.strip().lower() for k in raw_keywords.split(',') if k.strip()] 
print(f"Scouting this keywords: {KEYWORDS}")

# Create the client. 'my_session' will create a .session file locally
client = TelegramClient('my_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def monitor_groups(event):
    if event.is_group:
        text = event.raw_text.lower()
        print(text)
        
        if any(keyword in text for keyword in KEYWORDS):
            chat = await event.get_chat()
            group_name = chat.title
            
            alert = (
                f"🚨 **Keyword Alert!**\n"
                f"Found in group: **{group_name}**\n\n"
                f"Original message below:"
            )
            
            await client.send_message(DESTINATION, alert)
            await event.forward_to(DESTINATION)

print(f"Starting Userbot... Alerts will be sent to {DESTINATION}")
print("Press Ctrl+C to stop.")

client.start()
client.run_until_disconnected()