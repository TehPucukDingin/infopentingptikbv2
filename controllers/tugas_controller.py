import json
import os
from typing import List, Optional
from models.tugas import Tugas
import config

class TugasController:
    @staticmethod
    def load_all() -> List[Tugas]:
        """Load semua tugas dari file JSON"""
        if not os.path.exists(config.DATA_FILE):
            return []
        
        with open(config.DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Tugas.from_dict(item) for item in data]
    
    @staticmethod
    def save_all(tugas_list: List[Tugas]):
        """Simpan semua tugas ke file JSON"""
        data = [tugas.to_dict() for tugas in tugas_list]
        with open(config.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def add(tugas: Tugas) -> bool:
        """Tambah tugas baru"""
        try:
            data = TugasController.load_all()
            data.append(tugas)
            TugasController.save_all(data)
            return True
        except Exception as e:
            print(f"Error adding tugas: {e}")
            return False
    
    @staticmethod
    def delete(nama: str) -> bool:
        """Hapus tugas berdasarkan nama"""
        data = TugasController.load_all()
        original_len = len(data)
        data = [t for t in data if t.nama.lower() != nama.lower()]
        
        if len(data) == original_len:
            return False
        
        TugasController.save_all(data)
        return True
    
    @staticmethod
    def update_deadline(nama: str, new_deadline: str) -> bool:
        """Update deadline tugas dan reset reminder"""
        data = TugasController.load_all()
        
        for tugas in data:
            if tugas.nama.lower() == nama.lower():
                tugas.deadline = new_deadline
                tugas.reset_reminders()
                TugasController.save_all(data)
                return True
        
        return False
    
    @staticmethod
    def clear_all():
        """Hapus semua tugas"""
        TugasController.save_all([])
    
    @staticmethod
    def find_by_name(nama: str) -> Optional[Tugas]:
        """Cari tugas berdasarkan nama"""
        data = TugasController.load_all()
        for tugas in data:
            if tugas.nama.lower() == nama.lower():
                return tugas
        return None
    
    @staticmethod
    def get_upcoming() -> List[Tugas]:
        """Ambil tugas yang belum lewat deadline"""
        from datetime import datetime
        import config
        
        data = TugasController.load_all()
        now = datetime.now(config.TZ)
        
        upcoming = []
        for tugas in data:
            if tugas.get_deadline_datetime() > now:
                upcoming.append(tugas)
        
        return upcoming