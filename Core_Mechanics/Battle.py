import traceback
from Hooks.Hooks import clear_screen, naik_lantai, check_enemy_status
from UI.Battle_ui import BattleUI
from Exception.battle_exception import InvalidActionChoice, ActionCancelled, BattleEnded


class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 1
        self.event_dispatcher = player.event_dispatcher
        self.passive_skill_handler = player.passive_skill_handler
        self.active_skill_handler = player.active_skill_handler

    def start_battle(self, games, current_level):
        if self.turn_count == 1 and "battle_start" not in self.event_dispatcher.triggered_events:
            try:
                self.event_dispatcher.dispatch_event("battle_start", object=self.enemy)
            except Exception as e:
                print(f"[ERROR] dispatch_event('battle_start'): {e}")
                traceback.print_exc()

        try:
            while self.player.stats.hp > 0 and self.enemy.stats.hp > 0:
                try:
                    self.event_dispatcher.dispatch_event("turn_start", turn=self.turn_count)
                    self.event_dispatcher.dispatch_event("turn_interval", turn=self.turn_count)
                    BattleUI.display_battle_status(self.player, self.enemy, self.turn_count)
                    action = self.handle_turn()
                    if action == "exit_to_menu":
                        break
                    self.event_dispatcher.dispatch_event("turn_end")
                    self.turn_count += 1
                except BattleEnded:
                    raise
                except Exception as e:
                    print(f"[ERROR] selama turn: {e}")
                    traceback.print_exc()
                    break
        except BattleEnded:
            try:
                if self.enemy.name == games.game.dungeon_data[str(current_level)]['boss']:
                    games.defeated_boss()
                    self.player.world.boss_defeated = True
                self.event_dispatcher.dispatch_event("battle_end")
            except Exception as e:
                print(f"[ERROR] setelah BattleEnded: {e}")
                traceback.print_exc()

        try:
            if self.enemy.stats.hp <= 0:
                self.enemy_defeated(games, current_level)
            elif self.player.stats.hp <= 0:
                self.player_defeated()
        except Exception as e:
            print(f"[ERROR] after battle resolution: {e}")
            traceback.print_exc()


    def handle_turn(self):
        if self.enemy.stats.hp <= 0:
            raise BattleEnded

        try:
            self.action_fight_menu()
        except ActionCancelled:
            return "exit_to_menu"
        except InvalidActionChoice as e:
            print(f"[ERROR] InvalidActionChoice: {e}")
            return "exit_to_menu"
        except Exception as e:
            print(f"[ERROR] handle_turn(): {e}")
            traceback.print_exc()
            return "exit_to_menu"

        try:
            enemy_status = check_enemy_status(
                self.enemy,
                self.event_dispatcher.dispatch_event,
                self.passive_skill_handler
            )
            if enemy_status == "enemy_died":
                raise BattleEnded
                return  # 🛑 Tambahkan return agar tidak lanjut ke bawah
        except BattleEnded:
            raise  # Propagasi ke start_battle
        except Exception as e:
            print(f"[ERROR] check_enemy_status: {e}")
            traceback.print_exc()
            return

        try:
            self.enemy.attack_player(self.player)
            self.event_dispatcher.dispatch_event("player_hit")
            input("\nTekan Enter untuk melanjutkan...")
            clear_screen()
        except Exception as e:
            print(f"[ERROR] enemy attack/player_hit: {e}")
            traceback.print_exc()

        if self.player.stats.hp <= 0:
            raise BattleEnded

        return True

    def action_fight_menu(self):
        while True:
            try:
                BattleUI.display_fight_menu()
                choice = input("Masukkan pilihan (1/2/3): ")
                if choice == "1":
                    print(f"\n{self.player.name} menyerang {self.enemy.name} dengan Basic Attack!")
                    self.player.combat_handler.basic_attack(self.enemy)
                    break
                elif choice == "2":
                    attack_name = self.player.active_skills.name
                    confirm = input(f"\nGunakan {attack_name}? (Y/N): ").lower()
                    if confirm != "y":
                        print("\n❌ Serangan dibatalkan.")
                        raise ActionCancelled
                    print(f"\n{self.player.name} menggunakan {attack_name}!")
                    self.player.combat_handler.skill_attack(self.enemy)
                    break
                elif choice == "3":
                    print("\n❌ Anda membatalkan serangan.")
                    raise ActionCancelled
                else:
                    print("❌ Pilihan tidak valid!")
                    raise InvalidActionChoice("Pilihan tidak tersedia dalam menu pertarungan.")
            except (InvalidActionChoice, ActionCancelled):
                raise  # Lempar ulang agar handle_turn bisa mengatasi
            except Exception as e:
                print(f"[ERROR] action_fight_menu: {e}")
                traceback.print_exc()

        try:
            self.event_dispatcher.dispatch_event("enemy_hit")
        except Exception as e:
            print(f"[ERROR] dispatch_event('enemy_hit'): {e}")
            traceback.print_exc()

    def enemy_defeated(self, games, current_level):
        try:
            print(f"\n{self.enemy.name} telah mati!")
            self.event_dispatcher.dispatch_event("enemy_defeat")
            self.enemy.mark_as_dead()

            if self.enemy.name == games.game.dungeon_data[str(current_level)]['boss']:
                naik_lantai(self.player, current_level)
            self.player.gain_exp(self.enemy.level)
            input("\nTekan Enter untuk melanjutkan...")
            clear_screen()
        except Exception as e:
            print(f"[ERROR] enemy_defeated: {e}")
            traceback.print_exc()

    def player_defeated(self):
        try:
            print(f"{self.player.name} telah dikalahkan... Game Over!")
        except Exception as e:
            print(f"[ERROR] player_defeated: {e}")
            traceback.print_exc()
