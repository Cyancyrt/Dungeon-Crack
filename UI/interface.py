import os
# Kelas untuk menangani antarmuka game
class GameInterface:
    def __init__(self):
        self.input_counter = 0
        self.riwayat_output = []
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_user_input(self, prompt):
        user_input = input(prompt)
        self.input_counter += 1
        
        
        if self.input_counter == 2:
            self.clear_screen()
            self.reset_history()
        
        return user_input
    
    
    def reset_history(self):
        self.input_counter = 0
