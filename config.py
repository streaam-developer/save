import os

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7366608947:AAEZgQ8wJsPCn0Ki812QFSHFsVgpwuIusNg")

# Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", "904789"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "2262ef67ced426b9eea57867b11666a1")

# Your Owner / Admin Id For Broadcast 
ADMINS = int(os.environ.get("ADMINS", "6073523936"))

# Your Mongodb Database Url
DB_URI = os.environ.get("DB_URI", "mongodb+srv://lajihi2115:lgAEiuZHs917nZgy@cluster0.lx88eg8.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# If You Want Error Message In Your Personal Message Then Turn It True Else If You Don't Want Then Flase
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))
