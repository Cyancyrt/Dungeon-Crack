import random
import json
from UI.interface import GameInterface
from Hooks.Hooks import clear_screen, naik_lantai
from Hooks.Event_Dispatch import EventDispatcher
from Core_Mechanics.Battle import BattleSystem
from Enemy.enemy_module import Enemy
from Core_Mechanics.SearchFight import Fight


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
