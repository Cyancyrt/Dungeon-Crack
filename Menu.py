import os
import json
from Player import Player, CLASSES


SAVE_FILE = "player_save.json"

def save_player(player):
    with open(SAVE_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)

def load_player():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
            return Player.from_dict(data)
    return None


def create_new_player():
    name = input("Masukkan nama karakter: ")
    print("\nPilih class karakter:")
    for i, class_name in enumerate(CLASSES, 1):
        print(f"{i}. {class_name}")
    class_choice = int(input("Pilih class (1-7): ")) - 1
    player_class = CLASSES[class_choice]
    return Player(name, player_class, hp=100, mp=50, attack=25, defense=15, agility=15, stamina=30, intelligence=25, crit_chance=5, crit_damage=50)

def show_menu():
    while True:
        print("\n=== MENU GAME ===")
        print("1. Play")
        print("2. Create New")
        print("3. Load Save")
        print("4. Exit")
        choice = input("Pilih opsi (1-4): ")

        if choice == "1":
            player = load_player()
            if player:
                print(f"\nMemuat game... Selamat datang kembali, {player.name}!")
                return player
            else:
                print("\nTidak ada save ditemukan, membuat karakter baru...")
                player = create_new_player()
                save_player(player)
                return player

        elif choice == "2":
            player = create_new_player()
            save_player(player)
            print("\nKarakter baru telah dibuat dan disimpan!")
            return player

        elif choice == "3":
            player = load_player()
            if player:
                print("\nSave ditemukan! Karakter berhasil dimuat:")
                for key, value in player.to_dict().items():
                    print(f"{key.capitalize()}: {value}")
                return player
            else:
                print("\nTidak ada save ditemukan!")

        elif choice == "4":
            print("\nKeluar dari game. Sampai jumpa!")
            exit()
        
        else:
            print("\nInput tidak valid! Silakan pilih lagi.")

# Menampilkan menu game saat program dijalankan
player = show_menu()

def game_loop(player):
    while True:
        print("\n=== GAME MENU ===")
        print("Tekan 'B' untuk membuka Inventory")
        print("Tekan 'S' untuk melihat Status Player")
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

        elif choice.lower() == 'q':
            print("Keluar dari game...")
            save_player(player)
            break
        
        else:
            print("Pilihan tidak valid! Coba lagi.")

game_loop(player)