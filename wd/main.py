import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.command()
async def add(ctx, num: int, member: discord.Member):
    data = load_data()
    user_id = str(member.id)
    if user_id not in data:
        data[user_id] = 0
    data[user_id] += num
    save_data(data)
    await ctx.send(embed=discord.Embed(
        title="✅ Report Added",
        description=f"{member.mention} now has **{data[user_id]}** reports.",
        color=discord.Color.green()
    ))

@bot.command()
async def check(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    count = data.get(user_id, 0)
    embed = discord.Embed(
        title="📋 Report Stats",
        description=f"You have submitted **{count}** reports.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))
