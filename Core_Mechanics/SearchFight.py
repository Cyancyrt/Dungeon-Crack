
from UI.interface import GameInterface
from UI.Search_fightUI import BattleUI  # Tambahkan import BattleUI di bagian atas file
from Hooks.Hooks import clear_screen, naik_lantai
from Core_Mechanics.Battle import BattleSystem
import time
from Enemy.enemy_passive_handler import Enemy_passive


class Fight:
    def __init__(self, game):
        self.game = game
        self.interface = GameInterface()
        self.action = None
    

    def add_to_battle_history(self, enemy, floor):
        self._battle_history.append({
            "enemy_name": enemy.name,
            "enemy_id": getattr(enemy, "id", None),
            "defeated": False,
            "floor": floor,
            "timestamp": time.time()
        })

    def defeated_boss(self):
        try:
            BattleUI.display_boss_defeated()
        except Exception as e:
            print(f"[ERROR] defeated_boss: {e}")

    def status_menu(self, player):
        while True:
            try:
                BattleUI.display_status_menu(player)
                choice = input("Pilih opsi (1/2/3): ").strip()
                
                if choice == '1':
                    player.allocate_stat_points()
                elif choice == '2':
                    player.stat_handler.display_class_info()
                    input("\nTekan Enter untuk kembali...")
                    clear_screen()
                elif choice == '3':
                    break
                else:
                    BattleUI.display_invalid_choice()
            except Exception as e:
                print(f"[ERROR] status_menu: {e}")

    def action_menu(self, player, enemy):
        try:
            BattleUI.display_action_menu(player)
        except Exception as e:
            print(f"[ERROR] action_menu: {e}")

    def handle_player_action(self, player, enemy, current_level, input_key):
        try:
            if input_key == "1":
                BattleUI.display_start_fight(enemy)
                clear_screen()
                self.action.start_battle(self, current_level)
            elif input_key == "2":
                BattleUI.display_enemy_info(enemy)
            elif input_key == "3":
                return self.handle_escape_or_next_floor(player, current_level)
            elif input_key == "4":
                clear_screen()
                self.status_menu(player)
            elif input_key == "5":
                if self.confirm_exit():
                    clear_screen()
                    return "exit_to_menu"
            else:
                BattleUI.display_invalid_choice()
        except Exception as e:
            print(f"[ERROR] handle_player_action: {e}")
        return None

    def display_exit_text(self, player):
        try:
            BattleUI.display_exit_text(player)
        except Exception as e:
            print(f"[ERROR] display_exit_text: {e}")

    def handle_escape_or_next_floor(self, player, current_level):
        try:
            if player.world.boss_defeated:
                naik_lantai(player, current_level)
            else:
                confirm = input(f"\nApakah {player.name} yakin ingin keluar dari pertarungan? (y/n): ").strip().lower()
                if confirm != 'y':
                    print(f"{player.name} membatalkan aksi keluar.")
                elif confirm == 'y' and player.stats.stamina >= 10:
                    player.stats.stamina -= 5
                    print(f"Stamina {player.name} berkurang menjadi {player.stats.stamina}\n")
                    self.display_exit_text(player)
                    player.event_dispatcher.dispatch_event("battle_end")
                    player.event_dispatcher.reset_events()
                    return "battle_end"
                else:
                    print(f"{player.name} tidak memiliki cukup stamina untuk keluar dari pertarungan.")
        except Exception as e:
            print(f"[ERROR] handle_escape_or_next_floor: {e}")

    def confirm_exit(self):
        try:
            confirm = input("Anda yakin ingin keluar? Ini akan menghilangkan proses Anda! (y/n): ").strip().lower()
            return confirm == 'y'
        except Exception as e:
            print(f"[ERROR] confirm_exit: {e}")
            return False

    def start(self, player, current_level):
        try:
            enemy = self.game.choose_random_enemy(current_level)
            new_Handler = Enemy_passive(enemy, player.event_dispatcher)
            enemy.passive_skill_handler = new_Handler
            if enemy is None:
                print("Tidak ada musuh yang ditemukan di dungeon. Game berakhir.")
                return
            BattleUI.display_battle_intro(enemy)
            self.action = BattleSystem(player, enemy)

            while enemy.stats.hp > 0 and player.stats.hp > 0:
                BattleUI.display_start_fight(enemy)
                self.action_menu(player, enemy)
                
                input_key = self.interface.get_user_input("Pilih aksi (1-5): ")
                result = self.handle_player_action(player, enemy, current_level, input_key)

                if result == "exit_to_menu":
                    return result
                elif result == "battle_end":
                    break
                
                if player.stats.hp <= 0:
                    print(f"{player.name} kalah dalam pertarungan!")
                    return "exit_to_menu"
        except Exception as e:
            print(f"[ERROR] start: {e}")
