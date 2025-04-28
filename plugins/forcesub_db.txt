from plugins.dbusers import db  # use your existing database connection

forcesub_col = db.db.forcesub  # use 'forcesub' collection

async def get_forcesub_channels():
    data = await forcesub_col.find_one({"_id": 1})
    if data:
        return data.get("channels", [])
    else:
        return []

async def add_forcesub_channel(channel_id):
    data = await forcesub_col.find_one({"_id": 1})
    if data:
        if channel_id not in data["channels"]:
            await forcesub_col.update_one({"_id": 1}, {"$push": {"channels": channel_id}})
    else:
        await forcesub_col.insert_one({"_id": 1, "channels": [channel_id]})

async def remove_forcesub_channel(channel_id):
    await forcesub_col.update_one({"_id": 1}, {"$pull": {"channels": channel_id}})
