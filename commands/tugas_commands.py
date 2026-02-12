import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

from controllers.tugas_controller import TugasController
from models.tugas import Tugas
import config
from utils.helpers import format_deadline, parse_datetime

class TugasCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="tambah", description="Tambah tugas baru")
    @app_commands.describe(
        nama="Nama tugas",
        tanggal="Format: YYYY-MM-DD",
        jam="Format: HH:MM"
    )
    async def tambah(self, interaction: discord.Interaction, nama: str, tanggal: str, jam: str):
        try:
            deadline = config.TZ.localize(parse_datetime(tanggal, jam))
            
            tugas = Tugas(
                nama=nama,
                deadline=deadline.strftime("%Y-%m-%d %H:%M")
            )
            
            if TugasController.add(tugas):
                await interaction.response.send_message(
                    f"✅ **{nama}** berhasil ditambahkan!\n{format_deadline(deadline)}"
                )
            else:
                await interaction.response.send_message(
                    "❌ Gagal menambahkan tugas.",
                    ephemeral=True
                )
                
        except ValueError:
            await interaction.response.send_message(
                "❌ Format salah! Gunakan YYYY-MM-DD dan HH:MM",
                ephemeral=True
            )
    
    @app_commands.command(name="list", description="Lihat semua tugas")
    async def list_tugas(self, interaction: discord.Interaction):
        data = TugasController.load_all()
        
        if not data:
            await interaction.response.send_message("📂 Tidak ada tugas.")
            return
        
        pesan = "📌 **Daftar Tugas:**\n"
        
        for tugas in data:
            deadline = tugas.get_deadline_datetime()
            pesan += f"\n📝 {tugas.nama}\n{format_deadline(deadline)}\n"
        
        await interaction.response.send_message(pesan)
    
    @app_commands.command(name="hapus", description="Hapus tugas")
    @app_commands.describe(nama="Nama tugas yang akan dihapus")
    async def hapus(self, interaction: discord.Interaction, nama: str):
        if TugasController.delete(nama):
            await interaction.response.send_message(f"🗑 Tugas **{nama}** berhasil dihapus.")
        else:
            await interaction.response.send_message("❌ Tugas tidak ditemukan.", ephemeral=True)
    
    @app_commands.command(name="edit", description="Edit deadline tugas")
    @app_commands.describe(
        nama="Nama tugas",
        tanggal="Format: YYYY-MM-DD",
        jam="Format: HH:MM"
    )
    async def edit(self, interaction: discord.Interaction, nama: str, tanggal: str, jam: str):
        try:
            deadline = config.TZ.localize(parse_datetime(tanggal, jam))
            
            if TugasController.update_deadline(nama, deadline.strftime("%Y-%m-%d %H:%M")):
                await interaction.response.send_message(f"✏️ Deadline **{nama}** berhasil diperbarui.")
            else:
                await interaction.response.send_message("❌ Tugas tidak ditemukan.", ephemeral=True)
                
        except ValueError:
            await interaction.response.send_message(
                "❌ Format salah! Gunakan YYYY-MM-DD dan HH:MM",
                ephemeral=True
            )
    
    @app_commands.command(name="clear", description="Hapus semua tugas")
    async def clear(self, interaction: discord.Interaction):
        TugasController.clear_all()
        await interaction.response.send_message("🧹 Semua tugas berhasil dihapus.")
    
    @app_commands.command(name="besok", description="Lihat tugas deadline besok")
    async def besok(self, interaction: discord.Interaction):
        data = TugasController.load_all()
        now = datetime.now(config.TZ)
        besok_tanggal = (now + timedelta(days=1)).date()
        
        pesan = "📅 **Tugas Deadline Besok:**\n"
        ada = False
        
        for tugas in data:
            deadline = tugas.get_deadline_datetime()
            if deadline.date() == besok_tanggal:
                pesan += f"\n📝 {tugas.nama}\n⏰ {deadline.strftime('%H:%M')} WITA\n"
                ada = True
        
        if not ada:
            await interaction.response.send_message("🎉 Tidak ada tugas deadline besok.")
            return
        
        await interaction.response.send_message(pesan)
    
    @app_commands.command(name="helpbot", description="Lihat daftar command")
    async def helpbot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📌 INFO PENTING BOT - Command List",
            color=discord.Color.green()
        )
        
        commands_list = [
            ("/tambah", "Tambah tugas baru"),
            ("/list", "Lihat semua tugas"),
            ("/hapus", "Hapus tugas"),
            ("/edit", "Edit deadline tugas"),
            ("/besok", "Lihat tugas deadline besok"),
            ("/clear", "Hapus semua tugas")
        ]
        
        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(TugasCommands(bot))