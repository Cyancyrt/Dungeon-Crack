
import os

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

def tampilkan_riwayat(riwayat):
    """Menampilkan riwayat terbaru dan menghapus riwayat lama."""
    clear_screen()  # Bersihkan layar sebelum menampilkan riwayat baru
    print("batas aktivitas terbaru =================================")
    print(riwayat)  # Tampilkan riwayat terbaru
    print("\n")  # Beri jarak untuk aktivitas selanjutnya