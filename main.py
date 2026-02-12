import discord
from discord.ext import commands
import config

# =========================
# INTENTS & BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# EVENTS
# =========================

@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    
    # Load extensions (cogs)
    extensions = [
        "commands.tugas_commands",
        "tasks.background_tasks"
    ]
    
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"📦 Loaded: {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Slash command tersinkron: {len(synced)} commands")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    print("=" * 40)

# =========================
# ERROR HANDLING
# =========================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {error}")

# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
    if not config.TOKEN:
        print("❌ TOKEN tidak ditemukan! Set environment variable TOKEN.")
        exit(1)
    
    bot.run(config.TOKEN)