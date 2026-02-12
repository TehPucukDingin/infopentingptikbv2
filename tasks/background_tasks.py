import discord
from discord.ext import tasks, commands
from controllers.reminder_controller import ReminderController
import config

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reminder_controller = ReminderController(bot)
        self.reminder_loop.start()
        self.cleanup_loop.start()
    
    def cog_unload(self):
        self.reminder_loop.cancel()
        self.cleanup_loop.cancel()
    
    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        """Loop utama untuk mengirim reminder"""
        channel = self.bot.get_channel(config.REMINDER_CHANNEL_ID)
        if not channel:
            print(f"Channel {config.REMINDER_CHANNEL_ID} tidak ditemukan!")
            return
        
        # Dapatkan reminder yang pending
        pending = self.reminder_controller.get_pending_reminders()
        
        for tugas, reminder_type, sisa in pending:
            try:
                await self.reminder_controller.send_reminder(tugas, reminder_type, channel)
                self.reminder_controller.mark_reminded(tugas, reminder_type)
                print(f"Reminder {reminder_type} dikirim untuk: {tugas.nama}")
            except Exception as e:
                print(f"Error sending reminder: {e}")
    
    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()
        print("Reminder loop siap!")
    
    @tasks.loop(minutes=1)
    async def cleanup_loop(self):
        """Loop untuk membersihkan tugas yang sudah expired"""
        try:
            deleted_count = self.reminder_controller.cleanup_expired()
            if deleted_count > 0:
                print(f"{deleted_count} tugas expired dihapus.")
        except Exception as e:
            print(f"Error cleanup: {e}")
    
    @cleanup_loop.before_loop
    async def before_cleanup_loop(self):
        await self.bot.wait_until_ready()
        print("Cleanup loop siap!")

async def setup(bot: commands.Bot):
    await bot.add_cog(BackgroundTasks(bot))