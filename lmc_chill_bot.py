import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import datetime
import time
import logging

TOKEN = "MTM2NzgzMzc1NjAwNTU2ODU1Mg.Gd8yIi.urf2g2cqmGH80p6W_pd4mFSq9-1UeFlUrQBkhA"
APP_ID = 1367833756005568552
MOD_ROLE_ID = 1351601036879462521
ADMIN_ROLE_ID = 1373612375890202675

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="/", intents=intents, application_id=APP_ID)
bot.start_time = time.time()
blacklist = {}  # user_id: {channel_id: end_time}

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with pyro and 234t"))
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in blacklist:
        for chan_id in blacklist[message.author.id]:
            if message.channel.id == chan_id:
                if time.time() < blacklist[message.author.id][chan_id]:
                    await message.delete()
                    await message.channel.send(embed=discord.Embed(
                        description=f"🚫 Sorry {message.author.mention}, you are blacklisted from this channel for a while.",
                        color=discord.Color.red()
                    ))
                    return
    await bot.process_commands(message)

@bot.tree.command(name="linfo")
async def linfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🏝️ Welcome to Leone MC Chill Community",
        description=("We're a thriving community of over 300 members."
                     "\n✨ Features:\n- Strong moderation\n- Solid partnerships\n- Active chats and events\n\n"
                     "**Enjoy your stay and get involved!**"),
        color=discord.Color.teal()
    )
    embed.set_footer(text="- Managed by Pyro & 234t")
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="blacklist")
@app_commands.describe(user="User to blacklist", channel_id="Channel ID", duration="Time (e.g. 5H, 1m)")
async def blacklist_cmd(interaction: discord.Interaction, user: discord.Member, channel_id: str, duration: str):
    if MOD_ROLE_ID not in [r.id for r in interaction.user.roles]:
        return await interaction.response.send_message("You are not authorized 😂", ephemeral=True)

    seconds = 0
    duration = duration.upper()
    if "H" in duration:
        seconds = int(duration.replace("H", "")) * 3600
    elif "M" in duration:
        seconds = int(duration.replace("M", "")) * 60

    ch_id = int(channel_id)
    if user.id not in blacklist:
        blacklist[user.id] = {}
    blacklist[user.id][ch_id] = time.time() + seconds

    embed = discord.Embed(title="🔒 Blacklist Applied",
                          description=f"{user.mention} has been blacklisted from <#{ch_id}> for **{duration}**.",
                          color=discord.Color.red())
    await interaction.response.send_message(embed=embed)
    try:
        await user.send(f"🚫 You are blacklisted from <#{ch_id}> for {duration}. Your messages will be deleted if you speak.")
    except:
        pass

@bot.tree.command(name="whitelist")
@app_commands.describe(user="User to whitelist")
async def whitelist_cmd(interaction: discord.Interaction, user: discord.Member):
    if MOD_ROLE_ID not in [r.id for r in interaction.user.roles]:
        return await interaction.response.send_message("You are not authorized 😂", ephemeral=True)

    if user.id in blacklist:
        blacklist[user.id] = {}

    embed = discord.Embed(title="✅ Whitelisted",
                          description=f"{user.mention} can now speak freely again in all channels.",
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
    try:
        await user.send("✅ You are now whitelisted and free to talk again.")
    except:
        pass

@bot.tree.command(name="cmds", description="Show all bot commands")
async def cmds(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 LMC Bot Command List", color=discord.Color.blurple())
    embed.add_field(name="/linfo", value="Show server info", inline=False)
    embed.add_field(name="/ltimeout", value="Timeout a user", inline=False)
    embed.add_field(name="/lwarn", value="Warn a user", inline=False)
    embed.add_field(name="/dm", value="Send a DM to a user", inline=False)
    embed.add_field(name="/blacklist", value="Block a user from a channel", inline=False)
    embed.add_field(name="/whitelist", value="Unblock a user", inline=False)
    embed.add_field(name="/cmds", value="Show this command list", inline=False)
    embed.add_field(name="/botuptime", value="See bot uptime", inline=False)
    embed.add_field(name="/restart", value="Restart the bot", inline=False)
    embed.set_footer(text="Managed by LMC chill community mods Mods")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botuptime", description="Check bot uptime")
async def botuptime(interaction: discord.Interaction):
    if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        return await interaction.response.send_message("You are not authorized 😂", ephemeral=True)

    uptime = time.time() - bot.start_time
    mins, secs = divmod(int(uptime), 60)
    hours, mins = divmod(mins, 60)
    await interaction.response.send_message(embed=discord.Embed(
        title="🕒 Bot Uptime",
        description=f"⏱ {hours}h {mins}m {secs}s",
        color=discord.Color.gold()
    ))

@bot.tree.command(name="restart", description="Restart the bot")
async def restart(interaction: discord.Interaction):
    if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        return await interaction.response.send_message("You are not authorized 😂", ephemeral=True)

    await interaction.response.send_message(embed=discord.Embed(
        title="🔁 Restarting...",
        description="The bot is restarting. Please wait.",
        color=discord.Color.orange()
    ))
    await bot.close()

bot.run(TOKEN)
