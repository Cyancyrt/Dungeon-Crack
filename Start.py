from UI.Menu import show_menu
from Core_Mechanics.SearchFight import Game


# Game loop
def game_loop(player):
    game = Game('data/data_enemy.json', 'data/dungeon.json')  # Pastikan 'enemies.json' berisi data musuh
    game.start(player)

# Mulai permainan
player = show_menu()
game_loop(player)
