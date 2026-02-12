from datetime import datetime
from typing import List, Tuple, Optional
import discord
from models.tugas import Tugas
from controllers.tugas_controller import TugasController
import config

class ReminderController:
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    def get_pending_reminders(self) -> List[Tuple[Tugas, str, int]]:
        """
        Cek tugas yang perlu diremind sekarang
        Returns: List of (tugas, reminder_type, seconds_remaining)
        """
        data = TugasController.load_all()
        now = datetime.now(config.TZ)
        pending = []
        
        for tugas in data:
            deadline = tugas.get_deadline_datetime()
            sisa = (deadline - now).total_seconds()
            
            # Cek setiap threshold
            for key, threshold in config.REMINDER_THRESHOLDS.items():
                if key == "deadline":
                    if sisa <= 0 and not tugas.reminded.get(key, False):
                        pending.append((tugas, key, sisa))
                else:
                    if threshold >= sisa > 0 and not tugas.reminded.get(key, False):
                        pending.append((tugas, key, sisa))
        
        return pending
    
    async def send_reminder(self, tugas: Tugas, reminder_type: str, channel: discord.TextChannel):
        """Kirim embed reminder ke channel"""
        mention_role = f"<@&{config.ROLE_ID}>"
        
        titles = {
            "24h": "⏰ REMINDER H-1",
            "3h": "⚠️ REMINDER 3 JAM LAGI",
            "1h": "🔥 REMINDER 1 JAM LAGI",
            "deadline": "🚨 DEADLINE SEKARANG!"
        }
        
        embed = discord.Embed(
            title=titles.get(reminder_type, "⏰ REMINDER"),
            description=f"📌 **{tugas.nama}**",
            color=config.REMINDER_COLORS.get(reminder_type, discord.Color.blue())
        )
        
        deadline = tugas.get_deadline_datetime()
        embed.add_field(
            name="Deadline",
            value=deadline.strftime("%A, %d %B %Y\n%H:%M WITA")
        )
        embed.timestamp = deadline if reminder_type != "deadline" else datetime.now(config.TZ)
        embed.set_footer(text="INFO PENTING BOT")
        
        await channel.send(content=mention_role, embed=embed)
    
    def mark_reminded(self, tugas: Tugas, reminder_type: str):
        """Tandai reminder sudah dikirim dan simpan ke file"""
        data = TugasController.load_all()
        for t in data:
            if t.nama == tugas.nama and t.deadline == tugas.deadline:
                t.mark_reminded(reminder_type)
                break
        TugasController.save_all(data)
    
    def cleanup_expired(self) -> int:
        """Hapus tugas yang sudah lewat deadline, return jumlah yang dihapus"""
        data = TugasController.load_all()
        now = datetime.now(config.TZ)
        
        original_count = len(data)
        valid_data = [t for t in data if t.get_deadline_datetime() > now]
        
        if len(valid_data) < original_count:
            TugasController.save_all(valid_data)
        
        return original_count - len(valid_data)