import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
import asyncio
from flask import Flask

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot intents and commands
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Enable message delete events
bot = commands.Bot(command_prefix="!", intents=intents)

current_count = 1
last_user = None  # Track the last user who counted

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

ALLOWED_CHANNELS = [1396575946105946174]  

@bot.event
async def on_message(message):
    global current_count, last_user

    if message.author.bot:
        return

    # Check for the keyword "aito" and reply with the server emoji in any channel
    if "aito" in message.content.lower():
        await asyncio.sleep(1) 
        await message.reply("<:LionApple:1396221280168050730> 🫳 🧒")  # Replace emoji_id with the actual ID of :LionApple:
        await message.channel.send(
                f"Aito mention? Ew. He touches kids. Beware of him. He's an ableist *pervert*. We  talk shit about people like him in this server. He needs a reality check, but unfortunately, reality is too big for his little brain to comprehend."
            )
        return

    # Ensure the message is in the allowed channel for counting
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    # Match messages that look like "meow1", "meow2", etc.
    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))

        # Prevent the same user from counting twice consecutively
        if message.author.id == last_user:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("⚠️")  # Add the yellow exclamation mark emoji
            await message.reply(
                f"{message.author.mention}, you can't count twice in a row, idiot! That wouldn't be fair to the other nerds who want to count. Not that I care. But it *is* a bit selfish, so if you do, I'll just __ignore your message and not count it__. So there! Ha! Take that, *asshole*!"
            )
            return

        if number == current_count:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("✅")
            current_count += 1
            last_user = message.author.id  # Update the last user
        else:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("❌")
            await message.reply(
                f"Wow. {message.author.mention} has *ruined* it at {number}. What a **loser**! Now we have to start **all over again** from __1__. How *embarrassing*! You should be ashamed of yourself. I mean, really, how hard is it to count to *{current_count}*? It's not rocket science! But noooo, you had to mess it up. So now we have to start over. Thanks a lot, *jerk*!"
            )
            current_count = 1
            last_user = None  # Reset the last user
    else:
        await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    # Ensure the message is in the allowed channel for counting
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    # Match messages that look like "meow1", "meow2", etc.
    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))
        next_number = current_count  # The next expected number
        await message.channel.send(
            f"Tch, {message.author.mention} has deleted their number, meow{number}. How stupid. What even makes a person delete their number? Clearly, it wasn't a mistake, or I'd be telling you start over. You're lucky I don't make you start over, but I won't. So just keep counting, okay? The next number is {next_number}. Don't mess it up again!"
        )

# Create a simple HTTP server for Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread

    # Run the bot in a separate thread
    bot_thread = Thread(target=lambda: bot.run(TOKEN))
    bot_thread.start()

    # Get the port from the environment variable
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)