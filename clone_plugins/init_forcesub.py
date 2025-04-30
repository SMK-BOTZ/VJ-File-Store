import asyncio
from clone_plugins.dbusers import clonedb

# Replace with your actual force-subscribe channel IDs
INITIAL_CHANNELS = ["-1001234567890", "-1009876543210"]  # Add your channel IDs here

async def insert_forcesub_channels():
    await clonedb.update_one(
        "forcesub",
        {"_id": "force_sub_channels"},
        {"$set": {"channels": INITIAL_CHANNELS}},
        upsert=True
    )
    print("✅ ForceSub channels inserted successfully.")

if __name__ == "__main__":
    asyncio.run(insert_forcesub_channels())
