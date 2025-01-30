import random
import json
from enemy import Enemy
from Player import Player

# Game class for handling gameplay
class Game:
    def __init__(self, enemy_file, dungeon_file):
        # Memuat data musuh dan dungeon
        self.enemy_data = self.load_enemy_data(enemy_file)
        self.dungeon_data = self.load_dungeon_data(dungeon_file)
        self.enemies = [Enemy(**enemy) for enemy in self.enemy_data]

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

        if boss and random.random() < 0.05:  # 5% chance
            print("⚠️ Anda bertemu dengan BOSS LEVEL! ⚠️")
            enemy_name = boss
        else:
            enemy_name = random.choice(enemies_at_level)

        
        # Mencocokkan nama musuh dan mengembalikan data musuh lengkap
        enemy = next((enemy for enemy in self.enemy_data if enemy['name'] == enemy_name), None)
        
        if enemy:
            # Pilih nilai acak untuk atribut yang berupa range
            enemy['level_range'] = random.randint(enemy['level_range'][0], enemy['level_range'][1]) if isinstance(enemy['level_range'], list) else enemy['level_range'] # Menetapkan level yang dipilih
            enemy['hp'] = random.randint(enemy['hp'][0], enemy['hp'][1]) if isinstance(enemy['hp'], list) else enemy['hp']
            enemy['atk'] = random.randint(enemy['atk'][0], enemy['atk'][1]) if isinstance(enemy['atk'], list) else enemy['atk']
            enemy['defense'] = random.randint(enemy['defense'][0], enemy['defense'][1]) if isinstance(enemy['defense'], list) else enemy['defense']
            enemy['agility'] = random.randint(enemy['agility'][0], enemy['agility'][1]) if isinstance(enemy['agility'], list) else enemy['agility']
        
        return enemy

    def start(self, player):
        while True:
            print("\n=== GAME MENU ===")
            print("Tekan 'B' untuk membuka Inventory")
            print("Tekan 'S' untuk melihat Status Player")
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

            elif choice.lower() == 's':
                print("\n=== STATUS PLAYER ===")
                stats = player.display_stats()
                for key, value in stats.items():
                    print(f"{key.capitalize()}: {value}")

            elif choice.lower() == 'g':
                self.enter_dungeon(player)


            elif choice.lower() == 'q':
                print("Keluar dari game...")
                break

            else:
                print("Pilihan tidak valid! Coba lagi.")

    def enter_dungeon(self, player):
        # Mulai dari level 1
        current_level = 1  
        print(f"\n=== DUNGEON ===")
        print(f"Anda memasuki dungeon level {current_level}...")

        while player.hp > 0:  # Selama player masih hidup
            # Buat objek Fight untuk memulai pertarungan
            fight = Fight(self)  # Pass the current Game instance to Fight
            result = fight.start(player, current_level)  # Mulai pertarungan dengan player yang diberikan
            if result == "exit_to_menu":
                return "exit_to_menu"  # Memastikan game kembali ke menu
            # Jika player menang, lanjutkan ke pertarungan selanjutnya
            print(f"{player.name} melanjutkan ke pertarungan selanjutnya...")

class Fight:
    def __init__(self, game):
        # Menyimpan instance game yang diteruskan
        self.game = game

    def start(self, player, current_level):
        # Memilih musuh secara acak menggunakan metode choose_random_enemy dari Game
        enemy = self.game.choose_random_enemy(current_level)
        enemy = Enemy(**enemy)

        if enemy is None:
            print("Tidak ada musuh yang ditemukan di dungeon. Game berakhir.")
            return
        
        print(f"\nAnda bertemu dengan {enemy.name}!")
        print(f"HP: {enemy.hp}, ATK: {enemy.atk}, Level: {enemy.level_range}")
        # Mulai pertarungan
        while enemy.hp > 0 and player.hp > 0:
            print("\nApa yang akan Anda lakukan?")
            print("1. Serang musuh")
            print("2. Informasi Musuh")
            print("3. Keluar Dari Pertarungan")
            print("4. Lihat Status Player")
            print("5. Kembali ke Menu")

            input_key = input("Pilih aksi (1-5): ")

            if input_key == "1":
                # Pemain menyerang musuh
                print(f"{player.name} menyerang {enemy.name}!")
                player.attack_enemy(enemy)
                
                if enemy.hp <= 0:
                    print(f"{enemy.name} telah dikalahkan!")
                    player.gain_exp(enemy.level_range)
                    break  # Musuh kalah, keluar dari loop

                # Musuh membalas serangan
                enemy.attack_player(player)
                print(f"{enemy.name} membalas serangan!")

            elif input_key == "2":
                # Menampilkan detail informasi musuh
                print(f"\n=== DETAIL INFO {enemy.name} ===")
                Enemy.display_full_info(enemy)
                
            elif input_key == '3':  # Keluar dari pertarungan
                print(f"{player.name} memilih untuk keluar dari pertarungan...")
                # Kurangi stamina player ketika keluar
                if player.stamina >= 10:
                    player.stamina -= 5  # Gantilah angka 10 dengan nilai stamina yang sesuai
                    print(f"Stamina {player.name} sekarang: {player.stamina}")
                    break  # Keluar dari pertarungan dan kembali ke dungeon atau menu utama
                else:
                    print(f"{player.name} tidak memiliki cukup stamina untuk keluar dari pertarungan.")
                    
            elif input_key == '4':  # Lihat status player
                print(f"\n=== STATUS PLAYER ===")
                player.display_stats()
            elif input_key == '5':  # Kembali ke menu utama
                if player.stamina >= 10:
                    player.stamina -= 5  # Gantilah angka 10 dengan nilai stamina yang sesuai
                    print(f"Stamina {player.name} sekarang: {player.stamina}")
                    return "exit_to_menu"  # Keluar dari pertarungan dan kembali ke dungeon atau menu utama
                else:
                    print(f"{player.name} tidak memiliki cukup stamina untuk keluar dari pertarungan.")
                
            else:
                print("Aksi tidak valid, coba lagi.")

            # Cek status HP pemain setelah aksi
            if player.hp <= 0:
                print(f"{player.name} kalah dalam pertarungan!")
                return "exit_to_menu"

# # Contoh penggunaan
# if __name__ == "__main__":
#     player = Player(name="Hero", hp=100, atk=15, stamina=50)
#     game = Game('data_enemy.json', 'dungeon.json')
#     game.start(player)
