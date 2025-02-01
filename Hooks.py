
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

def naik_lantai(player, current_level):
    print("Apakah Anda ingin naik ke lantai berikutnya? (Y/N)")
    choice = input("\nPilih aksi (Y untuk naik, N untuk tetap): ").lower()
    if choice == 'y':
        player.floor_up()
    else:
        print(f"{player.name} memilih untuk tetap di lantai {current_level}.")