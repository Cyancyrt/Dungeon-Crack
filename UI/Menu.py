import os
import json
import time
from Player.Player_module import Player, CLASSES, Stats, World
from UI.Hooks import clear_screen

SAVE_FILE = "player_save.json"


# Save player data to a file
def save_player(player):
    with open(SAVE_FILE, "w") as file:
        json.dump(player.to_dict(), file, indent=4)

# Load player data from a save file
def load_player():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
            return Player.from_dict(data)
    return None

# Create a new player
def create_new_player():
    name = input("Masukkan nama karakter: ")
    print("\nPilih class karakter:")
    for i, class_name in enumerate(CLASSES, 1):
        print(f"{i}. {class_name}")
    class_choice = int(input("Pilih class (1-7): ")) - 1
    player_class = CLASSES[class_choice]
    stat = Stats()
    world = World()
    return Player(name, player_class, stat, world)

def loading_screen():
    border = "═" * 25
    for char in border:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()
    time.sleep(1)

# Display the main menu for game options
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
                loading_screen()
 
                clear_screen()
                return player
            else:
                print("\nTidak ada save ditemukan, membuat karakter baru...")
                player = create_new_player()
                save_player(player)
                clear_screen()
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



