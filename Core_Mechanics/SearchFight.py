import random
import json
import time
from UI.interface import GameInterface
from UI.Hooks import clear_screen, EventDispatcher, naik_lantai
from Core_Mechanics.Battle import BattleSystem
from Enemy.enemy_module import Enemy

# Game class for handling gameplay


import time

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
class Game:
    def __init__(self, enemy_file, dungeon_file):
        # Memuat data musuh dan dungeon
        self.enemy_data = self.load_enemy_data(enemy_file)
        self.dungeon_data = self.load_dungeon_data(dungeon_file)

    # Memuat data musuh dari file JSON
    def load_enemy_data(self, enemy_file):
        with open(enemy_file, 'r') as file:
            data = json.load(file)
        return data['enemies']

    # Memuat data dungeon dari file JSON
    def load_dungeon_data(self, dungeon_file):
        with open(dungeon_file, 'r') as file:
            data = json.load(file)
        return data['levels']

    # Pilih musuh acak berdasarkan level dungeon
    def choose_random_enemy(self, level):
        # Pilih musuh berdasarkan level yang diberikan
        enemies_at_level = self.dungeon_data[str(level)]['enemies']
        boss = self.dungeon_data[str(level)]['boss']
        enemy_name = random.choice(enemies_at_level)

        if boss and random.random() < 0.005:  # 5% chance
            print("⚠️ Anda bertemu dengan BOSS LEVEL! ⚠️")
            enemy_name = boss
        else:
            enemy_name = random.choice(enemies_at_level)

        
        # Mencocokkan nama musuh dan mengembalikan data musuh lengkap
        enemy = next((enemy for enemy in self.enemy_data if enemy['name'] == enemy_name), None)  
        enemy = Enemy(**enemy)
        enemy.set_level()
        enemy.set_attributes()
        # Pilih nilai acak untuk atribut lain yang berupa range    
        
        return enemy

    def start(self, player):
        while True:
            print("\n=== GAME MENU ===")
            print("Tekan 'B' untuk membuka Inventory")
            print("Tekan 'G' untuk masuk ke dungeon")
            print("Tekan 'Q' untuk keluar dari game")
            choice = input("Pilih aksi: ")

            if choice.lower() == 'b':
                print("\n=== INVENTORY ===")
                if player.inventory:
                    for item in player.inventory:
                        print(item)
                else:
                    print("Inventory kosong.")
            elif choice.lower() == 'g':
                clear_screen() 
                self.enter_dungeon(player)
                


            elif choice.lower() == 'q':
                print("Keluar dari game...")
                break

            else:
                print("Pilihan tidak valid! Coba lagi.")

    def enter_dungeon(self, player):
        # Mulai dari level 1
        current_level = player.world.current_level 
        print(f"\n=== DUNGEON ===")
        print(f"Anda memasuki dungeon level {current_level}...")

        while player.stats.hp > 0:  # Selama player masih hidup
            # Buat objek Fight untuk memulai pertarungan
            fight = Fight(self)  # Pass the current Game instance to Fight
            result = fight.start(player, current_level)  # Mulai pertarungan dengan player yang diberikan
            if result == "exit_to_menu":
                return "exit_to_menu"  # Memastikan game kembali ke menu
            # Jika player menang, lanjutkan ke pertarungan selanjutnya
            print(f"{player.name} melanjutkan ke pertarungan selanjutnya...")

class Fight:
    def __init__(self, game):
        self.game = game
        self.interface = GameInterface()
        self.action = None
    
    def defeated_boss(self):
        clear_screen()
        print("ANDA TELAH MENGALAHKAN BOSS!!!")
        print_sword_in_center()
        input("Tekan Enter untuk melanjutkan...")
    
    def status_menu(self, player):
        while True:
            player.display_stats()
            print("\nPilihan:")
            print("1. Upgrade Stat")
            print("2. Info Skill")
            print("3. Kembali ke Pertarungan")

            choice = input("Pilih opsi (1/2/3): ").strip()
            
            if choice == '1':
                player.allocate_stat_points()
            elif choice == '2':
                player.stat_handler.display_class_info()
                input("\nTekan Enter untuk kembali...")
                clear_screen()
            elif choice == '3':
                break  # Kembali ke pertarungan
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    
    def action_menu(self, player, enemy):
        print("\nApa yang akan Anda lakukan?")
        print("1. Serang musuh")
        print("2. Informasi Musuh")
        print("3. Naik Lantai" if player.world.boss_defeated else "3. Keluar Dari Pertarungan")            
        print("4. Lihat Status Player")
        print("5. Kembali ke Menu")
    
    def handle_player_action(self, player, enemy, current_level, input_key):
        if input_key == "1":
            self.display_start_fight(enemy)
            clear_screen()
            self.action.start_battle(self, current_level)
        elif input_key == "2":
            print(f"\n=== DETAIL INFO {enemy.name} ===")
            Enemy.display_full_info(enemy)
        elif input_key == "3":
            self.handle_escape_or_next_floor(player, current_level)
            return "exit_to_menu"
        elif input_key == "4":
            clear_screen()
            self.status_menu(player)
        elif input_key == "5":
            if self.confirm_exit():
                clear_screen()
                return "exit_to_menu"
        else:
            print("Aksi tidak valid, coba lagi.")
        return None
    

    def display_exit_text(self, player):
        text = f"{player.name} memilih untuk keluar dari pertarungan..."
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        clear_screen()

    def handle_escape_or_next_floor(self, player, current_level):
        if player.world.boss_defeated:
            naik_lantai(player, current_level)
        else:
            confirm = input(f"\nApakah {player.name} yakin ingin keluar dari pertarungan? (y/n): ").strip().lower()
            if confirm != 'y':
                print(f"{player.name} membatalkan aksi keluar.")
                return
            if player.stats.stamina >= 10:
                player.stats.stamina -= 5
                
                print(f"Stamina {player.name} berkurang menjadi {player.stats.stamina}\n")
                self.display_exit_text(player)
                new_enemy = self.game.choose_random_enemy(current_level)
                if new_enemy:
                    self.start(player, current_level)  # Restart battle dengan musuh baru
            else:
                print(f"{player.name} tidak memiliki cukup stamina untuk keluar dari pertarungan.")
    
    def confirm_exit(self):
        confirm = input("Anda yakin ingin keluar? Ini akan menghilangkan proses Anda! (y/n): ").strip().lower()
        return confirm == 'y'
    
    def display_start_fight(self,enemy):
        print("\n=== PERTARUNGAN ===")
        print(f"\n{enemy.name} bersiap untuk menyerang dengan penuh amarah!")

    def battle_intro(self,enemy):
        intro_text = f"\n⚔️ Anda bertemu dengan {enemy.name}! ⚔️"
        border = "═" * len(intro_text)
        enemy_status = f"\n🔥 Level {enemy.level} | ❤️ HP: {enemy.hp} | ⚔️ ATK: {enemy.atk}"
        
        print(f"\n{border}")
        print(f"\n{intro_text}")
        print(f"\n{border}")
        for char in enemy_status:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(1)

    def start(self, player, current_level):
        enemy = self.game.choose_random_enemy(current_level)
        if enemy is None:
            print("Tidak ada musuh yang ditemukan di dungeon. Game berakhir.")
            return
        
        self.battle_intro(enemy)
        self.action = BattleSystem(player, enemy)

        while enemy.hp > 0 and player.stats.hp > 0:
            self.display_start_fight(enemy)
            self.action_menu(player, enemy)
            
            input_key = self.interface.get_user_input("Pilih aksi (1-5): ")
            result = self.handle_player_action(player, enemy, current_level, input_key)
            
            if result == "exit_to_menu":
                return result
            
            if player.stats.hp <= 0:
                print(f"{player.name} kalah dalam pertarungan!")
                return "exit_to_menu"

