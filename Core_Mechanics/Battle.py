from Player.Class.Passive_skill import PassiveSkillHandler
from Player.Class.Active_Skill import ActiveSkillHandler
import time
from UI.Hooks import clear_screen, naik_lantai


class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.event_dispatcher = player.event_dispatcher
        self.turn_count = 1  # Simpan turn count sebagai atribut
        self.passive_skill_handler = PassiveSkillHandler(player, player.event_dispatcher)
        self.active_skill_handler = ActiveSkillHandler(player, player.event_dispatcher)


    def start_battle(self, games, current_level):
        """Mulai pertempuran"""
        if self.turn_count == 1 and not self.event_dispatcher.is_event_triggered("game_start"):
            self.event_dispatcher.dispatch_event("game_start")
        while self.player.stats.hp > 0 and self.enemy.hp > 0:
            self.display_battle_status(self.turn_count)
            action =  self.handle_turn()
            if action == "exit_to_menu":
                break
            self.event_dispatcher.dispatch_event("turn_end")
            self.turn_count += 1  # Increment turn count tanpa reset

            if self.enemy.hp <= 0 or self.player.stats.hp <= 0:
                if self.enemy.name == games.game.dungeon_data[str(current_level)]['boss']:
                    games.defeated_boss()
                    self.player.world.boss_defeated = True
                self.event_dispatcher.dispatch_event("battle_end")  # 🔥 Trigger event sebelum keluar
                break  # Keluar dari loop untuk memproses akhir pertempuran
        
        
        # input("\nTekan Enter untuk melanjutkan...")  # Memberi jeda sebelum giliran berikutnya
        # clear_screen()
        
        if self.enemy.hp <= 0:
            self.enemy_defeated(games, current_level)
        elif self.player.stats.hp <= 0:
            self.player_defeated()

    def display_battle_status(self, turn_count):
        """Menampilkan status pertempuran saat ini"""
        print(f"Turn {turn_count}")
        print(f"Player:   {self.player.name} HP: {self.player.stats.hp}/{self.player.stats.max_hp}")
        print(f"enemy:    {self.enemy.name} HP: {self.enemy.hp}/{self.enemy.max_hp}")
        print("=" * 30)

    def display_fight_menu(self):
        print("\nPilih aksi:")
        print("1. Basic Attack")
        print("2. Gunakan Skill")
        print("3. Batalkan")

    def handle_turn(self):
        """Menangani logika setiap giliran"""
        if self.enemy.hp <= 0:
            return
        action_result = self.action_fight_menu(self.player, self.enemy)
        if action_result is False:
            return "exit_to_menu"   # Jika serangan dibatalkan, jangan lanjut ke serangan musuh

        self.enemy.attack_player(self.player)  # Serangan musuh setelah pemain
        input("\nTekan Enter untuk melanjutkan...")
        clear_screen()

        if self.player.stats.hp <= 0:
            return
        
        return True

    def enemy_defeated(self, games, current_level):
        """Penanganan saat musuh dikalahkan"""
        
        print(f"\n{self.enemy.name} telah mati!")
        self.event_dispatcher.dispatch_event("enemy_defeat")
        if self.enemy.name == games.game.dungeon_data[str(current_level)]['boss']:
            naik_lantai(self.player, current_level)
        self.player.gain_exp(self.enemy.level)
        self.event_dispatcher.reset_events()
        input("\nTekan Enter untuk melanjutkan...")
        clear_screen()

    def player_defeated(self):
        """Penanganan saat pemain kalah"""
        print(f"{self.player.name} telah dikalahkan... Game Over!")

    def action_fight_menu(self, player, enemy):  
        while True:  # Loop sampai pemain memilih aksi yang valid
            self.display_fight_menu()
            choice = input("Masukkan pilihan (1/2/3): ")

            if choice == "1":
                attack_type = "basic"
                attack_name = "Basic Attack"
                break  # Keluar dari loop pilihan
            elif choice == "2":
                attack_type = "skill"
                attack_name = player.active_skills.name
                confirm = input(f"\nApakah Anda yakin ingin menggunakan {attack_name}? (Y/N): ").lower()
                if confirm != "y":
                    print("❌ Serangan dibatalkan.")
                    return False  # Kembali dengan indikasi pembatalan
                break
            elif choice == "3":
                print("❌ Anda membatalkan serangan.")
                return False  # Kembali dengan indikasi pembatalan
            else:
                print("❌ Pilihan tidak valid!")

        # Melakukan serangan
        if attack_type == "basic":
            print(f"\n{player.name} menyerang {enemy.name} dengan Basic Attack!")
            player.basic_attack(enemy)
        elif attack_type == "skill":
            print(f"\n{player.name} menggunakan {player.active_skills.name}!")
            player.activate_skill_attack(enemy)
        

        return True  # Kembali dengan indikasi aksi berhasil