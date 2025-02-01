import random
import json
import time
from interface import GameInterface
from enemy import Enemy
from Hooks import clear_screen, naik_lantai
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

        if boss and random.random() < 0.001:  # 5% chance
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
        # Menyimpan instance game yang diteruskan
        self.game = game
        self.interface = GameInterface()
    
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
            print("2. info skill")
            print("3. Kembali ke Pertarungan")

            choice = input("Pilih opsi (1/2/3): ").strip()
            
            if choice == '1':
                player.allocate_stat_points()  # Pastikan Anda memiliki metode ini dalam kelas Player
            elif choice == '2':
                player.display_class_info()
                input("\nTekan Enter untuk kembali...")
                clear_screen()
            elif choice == '3':
                print("Kembali ke pertarungan...")
                break  # Keluar dari loop dan kembali ke pertarungan
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def action_menu(self, player, enemy):
        # Menampilkan menu aksi dan memilih aksi
        print("\nApa yang akan Anda lakukan?")
        print("1. Serang musuh")
        print("2. Informasi Musuh")
        print("3. Keluar Dari Pertarungan" if not player.world.boss_defeated else "3. Naik Lantai")            
        print("4. Lihat Status Player")
        print("5. Kembali ke Menu")

    def action_fight_menu(self, player, enemy, current_level):
        while True:  # Loop sampai pemain memilih aksi yang valid
            print("\nPilih aksi:")
            print("1. Basic Attack")
            print("2. Gunakan Skill")
            print("3. Batalkan")

            choice = input("Masukkan pilihan (1/2/3): ")

            if choice == "1":
                attack_type = "basic"
                attack_name = "Basic Attack"
                break  # Keluar dari loop pilihan
            elif choice == "2":
                attack_type = "skill"
                attack_name = player.active_skill().get('name')
                confirm = input(f"\nApakah Anda yakin ingin menggunakan {attack_name}? (Y/N): ").lower()
                if confirm != "y":
                    print("❌ Serangan dibatalkan.")
                    input("\nTekan Enter untuk melanjutkan...")
                    return False  # Kembali dengan indikasi pembatalan
                break
            elif choice == "3":
                print("❌ Anda membatalkan serangan.")
                input("\nTekan Enter untuk melanjutkan...")
                return False  # Kembali dengan indikasi pembatalan
            else:
                print("❌ Pilihan tidak valid!")

        # Konfirmasi sebelum menyerang (diletakkan di luar loop)
        
        # Melakukan serangan
        if attack_type == "basic":
            print(f"\n{player.name} menyerang {enemy.name} dengan Basic Attack!")
            player.basic_attack(enemy)
        elif attack_type == "skill":
            print(f"\n{player.name} menggunakan {player.active_skill().get('name')}!")
            player.skill_attack(enemy)

        return True  # Kembali dengan indikasi aksi berhasil

 
    
    def action_fight(self, player, enemy, current_level):
        turn = "player"  # Pemain mulai lebih dulu
        turn_count = 1  # Menghitung giliran total dalam pertempuran

        # Aktifkan skill pasif di awal pertarungan
        # player.player_class.activate_passive()
        clear_screen()
        while player.stats.hp > 0 and enemy.hp > 0:
            print(f"Turn {turn_count}")
            print(f"{player.name} HP: {player.stats.hp}/{player.stats.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            print("=" * 30)

            # Update cooldown skill aktif & pasif setiap giliran
            # player.player_class.update_passive()
            # player.player_class.active_skill.reduce_cooldown()

            if turn == "player":
                action_result = self.action_fight_menu(player, enemy, current_level)

                if action_result is False:  # Jika serangan dibatalkan, jangan lanjut ke serangan musuh
                    break

                # Enemy's action (langsung setelah player menyerang)
                print(f"\n{enemy.name} membalas serangan!")
                enemy.attack_player(player)

                if player.stats.hp <= 0:
                    print(f"{player.name} telah dikalahkan... Game Over!")
                    break  # Keluar dari loop karena pemain kalah

                turn = "player"  # Kembali ke giliran pemain untuk turn berikutnya

            # **Peningkatan Turn Counter**
            turn_count += 1
            input("\nTekan Enter untuk melanjutkan...")  # Memberi jeda sebelum giliran berikutnya
            clear_screen()

    def start(self, player, current_level):
        # Memilih musuh secara acak menggunakan metode choose_random_enemy dari Game
        enemy = self.game.choose_random_enemy(current_level)
        enemy = Enemy(**enemy)

        if enemy is None:
            print("Tidak ada musuh yang ditemukan di dungeon. Game berakhir.")
            return
        
        print(f"\nAnda bertemu dengan {enemy.name}!")
        print(f"HP: {enemy.hp}, Level: {enemy.level_range}")
        # Mulai pertarungan
        while enemy.hp > 0 and player.stats.hp > 0:
            print("\n=== PERTARUNGAN ===")
            print(f"\n{enemy.name} bersiap untuk menyerang dengan penuh amarah!")
            print(f"HP musuh: {enemy.hp} | level musuh: {enemy.atk}")
            # check_enemy_status(enemy)
            self.action_menu(player, enemy)

            input_key = self.interface.get_user_input("Pilih aksi (1-5): ")

            if input_key == "1":
                # Pemain menyerang musuh
                self.action_fight(player, enemy, current_level)
            elif input_key == "2":
                # Menampilkan detail informasi musuh
                print(f"\n=== DETAIL INFO {enemy.name} ===")
                Enemy.display_full_info(enemy)
                
            elif input_key == '3':  # Keluar dari pertarungan
                if player.world.boss_defeated:
                    naik_lantai(player, current_level)
                    break  # Keluar dari loop pertarungan
                else:
                    print(f"{player.name} memilih untuk keluar dari pertarungan...")
                    # Kurangi stamina player ketika keluar
                    if player.stats.stamina >= 10:
                        player.stats.stamina -= 5  # Gantilah angka 10 dengan nilai stamina yang sesuai
                        print(f"Stamina {player.name} sekarang: {player.stats.stamina}")
                        break  # Keluar dari pertarungan dan kembali ke dungeon atau menu utama
                    else:
                        print(f"{player.name} tidak memiliki cukup stamina untuk keluar dari pertarungan.")
                    
            elif input_key == '4':  # Lihat status player
                clear_screen()
                self.status_menu(player)
                    

            elif input_key == '5':  # Kembali ke menu utama
                confirm = input("Anda yakin ingin keluar? Ini akan menghilangkan proses Anda! (y/n): ").strip().lower()
                if confirm == 'y':
                        clear_screen()
                        return "exit_to_menu"  # Keluar dari pertarungan dan kembali ke dungeon atau menu utama
                else:
                    print("Anda tetap bertahan dalam pertarungan.")

            else:
                print("Aksi tidak valid, coba lagi.")

            # Cek status HP pemain setelah aksi
            if player.stats.hp <= 0:
                print(f"{player.name} kalah dalam pertarungan!")
                return "exit_to_menu"
