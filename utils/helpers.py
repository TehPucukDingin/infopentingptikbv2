from datetime import datetime, timedelta
import config

def format_deadline(deadline_dt: datetime) -> str:
    """Format datetime untuk tampilan user"""
    return (
        f"🗓 {deadline_dt.strftime('%A, %d %B %Y')}\n"
        f"⏰ {deadline_dt.strftime('%H:%M')} WITA"
    )

def parse_datetime(tanggal: str, jam: str) -> datetime:
    """Parse string tanggal dan jam menjadi datetime"""
    return datetime.strptime(f"{tanggal} {jam}", "%Y-%m-%d %H:%M")

def get_time_remaining(deadline_dt: datetime, now_dt: datetime = None) -> timedelta:
    """Hitung sisa waktu hingga deadline"""
    if now_dt is None:
        now_dt = datetime.now(config.TZ)
    return deadline_dt - now_dt

def format_duration(seconds: int) -> str:
    """Format detik menjadi string yang readable"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours} jam {minutes} menit"
    return f"{minutes} menit"

def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """Cek apakah dua datetime berada di hari yang sama"""
    return dt1.date() == dt2.date()