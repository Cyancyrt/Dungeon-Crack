class BattleUI:
    # UI/display.py

    @staticmethod
    def display_battle_status(player, enemy, turn_count):
        """Menampilkan status pertempuran saat ini"""
        print(f"Turn {turn_count}")
        print(f"Player:   {player.name} HP: {player.stats.hp}/{player.stats.max_hp}")
        print(f"Enemy:    {enemy.name} HP: {enemy.stats.hp}/{enemy.stats.max_hp}")
        print("=" * 30)

    @staticmethod
    def display_fight_menu():
        """Menampilkan menu aksi pertarungan"""
        print("\nPilih aksi:")
        print("1. Basic Attack")
        print("2. Gunakan Skill")
        print("3. Batalkan")

    @staticmethod
    def display_attack(player, enemy, attack_type, skill_name=None):
        """Menampilkan aksi serangan"""
        if attack_type == "basic":
            print(f"\n{player.name} menyerang {enemy.name} dengan Basic Attack!")
        elif attack_type == "skill" and skill_name:
            print(f"\n{player.name} menggunakan {skill_name}!")

    @staticmethod
    def display_enemy_defeated(enemy_name):
        """Menampilkan pesan saat musuh dikalahkan"""
        print(f"\n{enemy_name} telah mati!")

    @staticmethod
    def display_player_defeated(player_name):
        """Menampilkan pesan saat pemain dikalahkan"""
        print(f"{player_name} telah dikalahkan... Game Over!")

    @staticmethod
    def display_cancelled():
        """Menampilkan pembatalan aksi"""
        print("❌ Anda membatalkan serangan.")

    @staticmethod
    def display_invalid_choice():
        """Menampilkan pesan saat pilihan tidak valid"""
        print("❌ Pilihan tidak valid!")

    @staticmethod
    def display_attack_cancelled():
        """Menampilkan pesan ketika pemain membatalkan skill"""
        print("❌ Serangan dibatalkan.\n")
