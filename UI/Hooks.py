
import os
import re

def check_enemy_status(enemy):
    """Menampilkan status musuh berdasarkan persentase HP yang tersisa."""
    if enemy.hp <= 0:
        print(f"\n{enemy.name} akhirnya tumbang!")
        return

    hp_percentage = (enemy.hp / enemy.max_hp) * 100  # Menghitung persentase HP tersisa

    if hp_percentage <= 20:
        print(f"\n{enemy.name} hampir tumbang! ({hp_percentage:.0f}% HP tersisa)")
    elif hp_percentage <= 50:
        print(f"\n{enemy.name} mulai terlihat kelelahan! ({hp_percentage:.0f}% HP tersisa)")

def clear_screen():
    """Membersihkan layar cmd."""
    os.system('cls' if os.name == 'nt' else 'clear')

def naik_lantai(player, current_level):
    print("Apakah Anda ingin naik ke lantai berikutnya? (Y/N)")
    choice = input("\nPilih aksi (Y untuk naik, N untuk tetap): ").lower()
    if choice == 'y':
        player.floor_up()
    else:
        print(f"{player.name} memilih untuk tetap di lantai {current_level}.")

def get_stat_from_effect(effect_type):
    """Mencari stat dasar dari nama efek menggunakan pola regex"""
    patterns = {
        "attack": r"attack",     # Semua efek yang mengandung "attack"
        "defense": r"defense",   # Semua efek yang mengandung "defense"
        "speed": r"speed",       # Jika ada efek kecepatan
        "critical": r"crit|critical",  # Bisa menangkap "crit_up", "critical_increase"
        "hp": r"hp|health"  # Bisa menangkap "hp_boost", "health_regen"
    }

    for stat, pattern in patterns.items():
        if re.search(pattern, effect_type):
            return stat  # Kembalikan nama stat yang sesuai

    return None

class EventDispatcher:
    def __init__(self):
        self.event_handlers = {}
        self.triggered_events = set({"turn_end"})  # Menyimpan event yang sudah terjadi

    def register_event(self, event_type, handler):
        """Mendaftarkan handler untuk suatu event"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def dispatch_event(self, event_type, **kwargs):
        """Memicu semua handler untuk event tertentu"""
        self.triggered_events.add(event_type)  # Tandai event sudah terjadi
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                handler(**kwargs)

    def is_event_triggered(self, event_type):
        """Cek apakah event sudah terjadi"""
        return event_type in self.triggered_events
    def reset_events(self):
        """Reset semua event setelah pertarungan selesai"""
        self.triggered_events.clear()