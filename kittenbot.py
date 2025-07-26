import discord  
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import re
import asyncio
import random
from flask import Flask
from discord import app_commands  # Added for slash commands
from datetime import datetime, timedelta

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
message_toggle = True  # Toggle for aito/raylen messages
ALLOWED_CHANNELS = [1396575946105946174]

# Track last valid count timestamp
last_count_time = datetime.utcnow()

# 🔧 Message map for testing
MESSAGE_MAP = {
    "fixcount": "Count manually set to meow{number}. Don't mess it up!",
    "countspace": "Tch. You're not supposed to put a *space* idiot. That's just boring. Like, come *on*, who cares about a space? We're literally counting by meowing. I'm not going to count that, because it looks ugly.",
    "nomeow": "Seriously? You didn't meow? How *boooorrrringggg*. Go be boring in another server, go on, shoo. Why would you even think that would count? Like, *seriously*, the whole point is that you *count* in __meows__. Or maybe you think Ky was 'cringe' for suggesting this bot? If so, get lost, you stupid prick. Your number doesn't count, loser!",
    "sameperson": "{mention}, you can't count twice in a row, idiot! That wouldn't be fair to the other nerds who want to count. Not that I care. But it *is* a bit selfish, so if you do, I'll just __ignore your message and not count it__. So there! Ha! Take that, *asshole*!",
    "wrongcount": "Wow. {mention} has *ruined* it at {{number}}. What a **loser**! Now we have to start **all over again** from __1__. How *embarrassing*! You should be ashamed of yourself. I mean, really, how hard is it to count to *{number}*? It's not rocket science! But noooo, you had to mess it up. So now we have to start over. Thanks a lot, *jerk*!",
    "countdelete": "Tch, {mention} has deleted their number, meow{number}. How stupid. What even makes a person delete their number? Clearly, it wasn't a mistake, or I'd be telling you start over. You're lucky I don't make you start over, but I won't. So just keep counting, okay? The next number is {number}. Don't mess it up again!",
    "inactivitycount": "Hey losers, it's been *aaaagessss* since anyone counted. It gets boring when no one counts, I'm so *loonely*. Do you guys really want me to just sit here and do nothing? I mean, come on, I have feelings too! I should have never left DedS3c, not when everyone here is losers! The next number is {number}, get working! Or I'll start doing dumb shit in other channels."
}

# ⏱️ Task to check for idle time
@tasks.loop(minutes=5)
async def check_counting_idle():
    now = datetime.utcnow()
    time_passed = (now - last_count_time).total_seconds()

    threshold = getattr(check_counting_idle, "next_delay", random.randint(2700, 10800))  # 45-180 mins

    if time_passed > threshold:
        check_counting_idle.next_delay = random.randint(2700, 10800)  # set next threshold
        channel = bot.get_channel(ALLOWED_CHANNELS[0])
        if channel:
            await channel.send(MESSAGE_MAP["inactivitycount"].format(number=current_count))
        global last_count_time
        last_count_time = now

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

@bot.tree.command(name="flkcountfix", description="Manually set the current count.")
@app_commands.describe(number="The number to set the count to.")
async def flkcountfix(interaction: discord.Interaction, number: int):
    global current_count
    current_count = number
    await interaction.response.send_message(MESSAGE_MAP["fixcount"].format(number=current_count))

@bot.tree.command(name="flkmessagetoggle", description="Toggle aito/raylen auto-replies on or off.")
async def flkmessagetoggle(interaction: discord.Interaction):
    global message_toggle
    message_toggle = not message_toggle
    status = "enabled" if message_toggle else "disabled"
    await interaction.response.send_message(f"Aito/Raylen replies are now **{status}**.")

@bot.tree.command(name="flkmessageclist", description="List all available message types.")
async def flkmessageclist(interaction: discord.Interaction):
    if interaction.user.id != 1385289323628466216:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    msg = "**Available message keys:**\n" + "\n".join(f"- {key}" for key in MESSAGE_MAP)
    await interaction.response.send_message(msg)

@bot.tree.command(name="flkmessagectest", description="Test a single message type.")
@app_commands.describe(message="The message key to test.")
async def flkmessagectest(interaction: discord.Interaction, message: str):
    if interaction.user.id != 1385289323628466216:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    if message not in MESSAGE_MAP:
        await interaction.response.send_message("Invalid message key.", ephemeral=True)
        return
    await interaction.response.send_message(MESSAGE_MAP[message].format(number=current_count, mention=interaction.user.mention))

@bot.tree.command(name="flkmessagectestall", description="Test all message types.")
async def flkmessagectestall(interaction: discord.Interaction):
    if interaction.user.id != 1385289323628466216:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    for key, msg in MESSAGE_MAP.items():
        await interaction.channel.send(f"[{key}]\n" + msg.format(number=current_count, mention=interaction.user.mention))

@bot.event
async def on_message(message):
    global current_count, last_user, message_toggle, last_count_time

    if message.author.bot:
        return

    content = message.content.strip()

    if message_toggle:
        lowered = content.lower()
        if "aito" in lowered:
            await asyncio.sleep(1)
            await message.reply("<:LionApple:1396221280168050730> 🫳 🧒")
            await message.channel.send(
                f"Aito mention? Ew. He touches kids. Beware of him. He's an ableist *pervert*. We talk shit about people like him in this server. He needs a reality check, but unfortunately, reality is too big for his little brain to comprehend."
            )
            return
        if "raylen" in lowered:
            await asyncio.sleep(1)
            await message.reply("Raylen mention? Ugh. She *clearly* doesn't care for the safety of other people, or maybe she would actually ban Aito, who is *clearly* a __**pervert**__. She can't even admit when she is in the wrong! She is *not* fit to run a server of __over *1000* people__!")
            return

    if message.channel.id not in ALLOWED_CHANNELS:
        return

    if re.fullmatch(r"meow\s+\d+", content.lower()):
        await message.reply(MESSAGE_MAP["countspace"])
        return

    if re.fullmatch(r"\d+", content):
        await message.reply(MESSAGE_MAP["nomeow"])
        return

    match = re.fullmatch(r"meow(\d+)", content.lower())
    if match:
        number = int(match.group(1))

        if message.author.id == last_user:
            await asyncio.sleep(1)
            await message.add_reaction("⚠️")
            await message.reply(MESSAGE_MAP["sameperson"].format(mention=message.author.mention))
            return

        if number == current_count:
            await asyncio.sleep(1)
            await message.add_reaction("✅")
            current_count += 1
            last_user = message.author.id
            last_count_time = datetime.utcnow()
        else:
            await asyncio.sleep(1)
            await message.add_reaction("❌")
            await message.reply(MESSAGE_MAP["wrongcount"].format(mention=message.author.mention, number=number))
            current_count = 1
            last_user = None
    else:
        await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))
        next_number = current_count
        await message.channel.send(MESSAGE_MAP["countdelete"].format(mention=message.author.mention, number=number))

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

    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
