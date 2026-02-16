import os

# IMPORTANT: Get your API credentials from https://my.telegram.org/apps
# The values below are PLACEHOLDERS - replace with real values!
DEST_CHANNEL_ID = -1003735599360

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7234321564:AAELvfc6WGXEdTap0NwIcSB3o_kxvp9mHPY")

# Your API ID from my.telegram.org (must be a valid number)
# Get from https://my.telegram.org/apps
API_ID = int(os.environ.get("API_ID", "904789"))

# Your API Hash from my.telegram.org (32 character string)
# Get from https://my.telegram.org/apps
API_HASH = os.environ.get("API_HASH", "2262ef67ced426b9eea57867b11666a1")

# Your Owner / Admin Id For Broadcast 
ADMINS = int(os.environ.get("ADMINS", "1845582481"))

# Your Mongodb Database Url
# Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_URI = os.environ.get("DB_URI", "mongodb+srv://sonukumarkrbbu60:lfkTvljnt25ehTt9@cluster0.2wrbftx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# If You Want Error Message In Your Personal Message Then Turn It True Else If You Don't Want Then Flase
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))
