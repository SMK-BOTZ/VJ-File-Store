# © Telegram : @KingVJ01 , GitHub : @VJBots

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import requests
import json
from motor.motor_asyncio import AsyncIOMotorClient
from config import CLONE_DB_URI, DB_NAME

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

client = AsyncIOMotorClient(CLONE_DB_URI)
db = client[DB_NAME]
col = db["users"]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_short_link(user, link):
    api_key = user["shortener_api"]
    base_site = user["base_site"]
    print(user)
    response = requests.get(f"https://{base_site}/api?api={api_key}&url={link}")
    data = response.json()
    if data["status"] == "success" or response.status_code == 200:
        return data["shortenedUrl"]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_user(user_id):
    user_id = int(user_id)

    user = await col.find_one({"user_id": user_id})

    if not user:
        res = {
            "user_id": user_id,
            "shortener_api": None,
            "base_site": None,
            "clone_bot": None,  # Initialize the clone bot field
        }

        await col.insert_one(res)
        user = await col.find_one({"user_id": user_id})

    return user

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def update_user_info(user_id, value: dict):
    user_id = int(user_id)
    myquery = {"user_id": user_id}
    newvalues = {"$set": value}
    await col.update_one(myquery, newvalues)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def total_users_count():
    count = await col.count_documents({})
    return count

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def get_all_users():
    all_users = col.find({})
    return all_users

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def delete_user(user_id):
    await col.delete_one({'user_id': int(user_id)})

# Clone Bot Management Functions

# Add a clone bot for a user
async def add_clone(user_id, bot_token):
    user_id = int(user_id)
    clone_data = {"bot_token": bot_token}
    await update_user_info(user_id, {"clone_bot": clone_data})

# Get the clone bot for a user
async def get_clone(user_id):
    user_id = int(user_id)
    user = await get_user(user_id)
    return user.get("clone_bot")  # Returns None if no clone exists

# Delete the clone bot for a user
async def delete_clone(user_id):
    user_id = int(user_id)
    await update_user_info(user_id, {"clone_bot": None})

