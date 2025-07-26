import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import re
import asyncio
import random
from flask import Flask
from discord import app_commands
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot intents and commands
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

current_count = 1
last_user = None
message_toggle = True
ALLOWED_CHANNELS = [1396575946105946174]
last_count_time = datetime.utcnow()
OWNER_ID = 1385289323628466216

# Predefined messages
message_templates = {
    "fixcount": "Count manually set to meow{number}. Don't mess it up!",
    "countspace": "Tch. You're not supposed to put a *space* idiot...",
    "nomeow": "Seriously? You didn't meow? How *boooorrrringggg*...",
    "sameperson": "{mention}, you can't count twice in a row, idiot!...",
    "wrongcount": "Wow. {mention} has *ruined* it at {number}. What a **loser**!...",
    "countdelete": "Tch, {mention} has deleted their number, meow{number}. How stupid...",
    "inactivitycount": "Hey losers, it's been *aaaagessss* since anyone counted... The next number is {number}, get working!..."
}

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    print(f"✅ Logged in as {bot.user}")
    check_counting_idle.start()

@bot.tree.command(name="flkmessageclist", description="List all message keys.")
async def flkmessageclist(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    msg = "Available message keys:\n" + "\n".join(f"- {k}" for k in message_templates.keys())
    await interaction.response.send_message(msg, ephemeral=True)

@bot.tree.command(name="flkmessagectest", description="Test a specific message.")
@app_commands.describe(message="The name of the message to test.")
async def flkmessagectest(interaction: discord.Interaction, message: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    template = message_templates.get(message)
    if not template:
        await interaction.response.send_message("Invalid message key.", ephemeral=True)
        return

    output = template.format(mention=interaction.user.mention, number=current_count)
    await interaction.response.send_message(output)

@bot.tree.command(name="flkmessagectestall", description="Test all messages.")
async def flkmessagectestall(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    for key, template in message_templates.items():
        await interaction.channel.send(f"**{key}**: {template.format(mention=interaction.user.mention, number=current_count)}")
    await interaction.response.send_message("All test messages sent.", ephemeral=True)

# Flask webserver for Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread

    bot_thread = Thread(target=lambda: bot.run(TOKEN))
    bot_thread.start()

    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
