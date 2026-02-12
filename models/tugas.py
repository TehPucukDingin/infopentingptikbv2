from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any
import config

@dataclass
class Tugas:
    nama: str
    deadline: str  # Format: "%Y-%m-%d %H:%M"
    reminded: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.reminded is None:
            self.reminded = {
                "24h": False,
                "3h": False,
                "1h": False,
                "deadline": False
            }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tugas':
        return cls(
            nama=data["nama"],
            deadline=data["deadline"],
            reminded=data.get("reminded", {
                "24h": False,
                "3h": False,
                "1h": False,
                "deadline": False
            })
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nama": self.nama,
            "deadline": self.deadline,
            "reminded": self.reminded
        }
    
    def get_deadline_datetime(self) -> datetime:
        """Convert deadline string to datetime object dengan timezone"""
        deadline_naive = datetime.strptime(self.deadline, "%Y-%m-%d %H:%M")
        return config.TZ.localize(deadline_naive)
    
    def reset_reminders(self):
        """Reset semua status reminder"""
        for key in self.reminded:
            self.reminded[key] = False
    
    def mark_reminded(self, key: str):
        """Tandai reminder tertentu sudah dikirim"""
        if key in self.reminded:
            self.reminded[key] = True