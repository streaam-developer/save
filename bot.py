# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client
from pyrogram.errors import AuthBytesInvalid
from config import API_ID, API_HASH, BOT_TOKEN
import os

class Bot(Client):

    def __init__(self):
        super().__init__(
            "techvj login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=50,
            sleep_threshold=10,
            session_string=None,
            in_memory=False,
            device_model="TechVJ Bot",
            system_version="1.0",
            app_version="2.3.45",
            language_code="en"
        )

    async def start(self):
        # Delete old session if exists (fixes connection issues)
        session_file = "techvj login.session"
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                print("Removed old session file due to connection issues")
            except:
                pass
        
        try:
            await super().start()
            print('Bot Started Powered By @VJ_Botz')
        except AuthBytesInvalid as e:
            print("ERROR: Invalid API credentials! Please check your API_ID and API_HASH from my.telegram.org")
            raise e
        except Exception as e:
            print(f"Connection error: {e}")
            raise e

    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

Bot().run()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
