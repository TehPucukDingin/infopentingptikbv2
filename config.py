import os
import pytz

# =========================
# KONFIGURASI BOT
# =========================

TOKEN = os.getenv("TOKEN")
REMINDER_CHANNEL_ID = 1471544410364842166
ROLE_ID = 1428267266222460948
DATA_FILE = "tugas.json"

# Timezone
TZ = pytz.timezone("Asia/Makassar")

# Reminder thresholds (dalam detik)
REMINDER_THRESHOLDS = {
    "24h": 86400,    # 24 jam
    "3h": 10800,     # 3 jam
    "1h": 3600,      # 1 jam
    "deadline": 0    # deadline
}

# Warna embed untuk setiap reminder
REMINDER_COLORS = {
    "24h": 0x3498db,      # Biru
    "3h": 0xe67e22,       # Oranye
    "1h": 0xe74c3c,       # Merah
    "deadline": 0x992d22  # Merah tua

}
