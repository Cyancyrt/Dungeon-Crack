import time
from Hooks.Hooks import clear_screen
def print_sword_in_center(screen_width=30, sword_symbol="⚔️⚔️⚔️"):
    padding = (screen_width - len(sword_symbol)) // 2
    loading_animation()
    print(" " * padding + sword_symbol + " " * padding)
    # Mencetak garis pembatas bawah
    loading_animation()
    time.sleep(0.5)  # Waktu tunggu 0.5 detik untuk efek


def loading_animation():
    print("\n", end="")
    for _ in range(30):  # Jumlah karakter "=" yang akan dicetak
        print("=", end="", flush=True)
        time.sleep(0.1)  # Jeda 0.1 detik antar setiap karakter
    print()  # Pindah ke baris baru setelah selesai


class BattleUI:
    @staticmethod
    def display_battle_intro(enemy):
        intro_text = f"\n⚔️ Anda bertemu dengan {enemy.name}! ⚔️"
        border = "═" * len(intro_text)
        enemy_status = f"\n🔥 Level {enemy.level} | ❤️ HP: {enemy.stats.hp} | ⚔️ ATK: {enemy.stats.attack}"
        
        print(f"\n{border}")
        print(f"\n{intro_text}")
        print(f"\n{border}")
        for char in enemy_status:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(1)

    @staticmethod
    def display_start_fight(enemy):
        print("\n=== PERTARUNGAN ===")
        print(f"\n{enemy.name} bersiap untuk menyerang dengan penuh amarah!")

    @staticmethod
    def display_exit_text(player):
        text = f"{player.name} memilih untuk keluar dari pertarungan..."
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        clear_screen()
        time.sleep(0.5)

    @staticmethod
    def display_status_menu(player):
        player.display_stats()
        print("\nPilihan:")
        print("1. Upgrade Stat")
        print("2. Info Skill")
        print("3. Kembali ke Pertarungan")

    @staticmethod
    def display_action_menu(player):
        print("\nApa yang akan Anda lakukan?")
        print("1. Serang musuh")
        print("2. Informasi Musuh")
        print("3. Naik Lantai" if player.world.boss_defeated else "3. Keluar Dari Pertarungan")            
        print("4. Lihat Status Player")
        print("5. Kembali ke Menu")

    @staticmethod
    def display_enemy_info(enemy):
        print(f"\n=== DETAIL INFO {enemy.name} ===")
        enemy.display_full_info()

    @staticmethod
    def display_invalid_choice():
        print("❌ Pilihan tidak valid, coba lagi.")

    @staticmethod
    def display_boss_defeated():
        print("ANDA TELAH MENGALAHKAN BOSS!!!")
        print_sword_in_center()
        input("Tekan Enter untuk melanjutkan...")

    @staticmethod
    def display_cancelled():
        print("❌ Anda membatalkan serangan.")
