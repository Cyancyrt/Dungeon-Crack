import json

CLASSES = ["Swordsman", "Lancer", "Cleric", "Mage", "Rogue", "Archer", "Warrior"]
class Player:
    def __init__(self, name, player_class, hp, mp, attack, defense, agility, stamina, intelligence, crit_chance, crit_damage, level=1, stat_points=0,current_world=1, current_level=1, exp=0,level_up_exp=100, inventory=None):
        self.name = name
        self.player_class = player_class
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.stamina = stamina
        self.intelligence = intelligence
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.level = level
        # Set nilai maksimum
        self.max_hp = hp
        self.max_mp = mp
        self.max_stamina = stamina

        #world
        self.current_world = 1  # Menyimpan world saat ini
        self.current_level = 1  # Menyimpan level dungeon saat ini

        #exp
        self.exp = 0
        self.level_up_exp = 100  # EXP awal untuk naik level
        self.stat_points = stat_points  # Poin yang bisa dialokasikan
        self.inventory = inventory if inventory is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "player_class": self.player_class,
            "hp": self.hp,
            "mp": self.mp,
            "attack": self.attack,
            "defense": self.defense,
            "agility": self.agility,
            "stamina": self.stamina,
            "intelligence": self.intelligence,
            "crit_chance": self.crit_chance,
            "crit_damage": self.crit_damage,
            "level": self.level,
            "stat_points": self.stat_points,
            "inventory": self.inventory,
            "level": self.level,
            "exp": self.exp,
            "level_up_exp": self.level_up_exp,
            "current_world" : self.current_world,
            "current_level" : self.current_level
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def save_progress(self):
        with open("player_save.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print("✅ Progress berhasil disimpan!")
    def display_stats(self):
        stats = self.to_dict()
        stats["crit chance"] = f"{stats.pop('crit_chance', 0)}%"
        stats["crit damage"] = f"{stats.pop('crit_damage', 0)}%"
        stats.pop("inventory", None)

        # Konversi ke daftar tuple untuk pemetaan berpasangan
        stat_items = list(stats.items())
        half = len(stat_items) // 2

        # Cetak dalam format dua kolom
        for left, right in zip(stat_items[:half], stat_items[half:]):
            print(f"{left[0]:<15}: {left[1]:<10}  |  {right[0]:<15}: {right[1]}")

        # Jika jumlah elemen ganjil, cetak elemen terakhir
        if len(stat_items) % 2 != 0:
            last_key, last_value = stat_items[-1]
            print(f"{last_key:<15}: {last_value}")
    
    def gain_exp(self, enemy_level):
        """Menambahkan EXP berdasarkan level musuh dan naik level jika perlu"""
        base_exp = 15  # EXP dasar untuk mengalahkan musuh
        level_difference = enemy_level - self.level

        # Hitung EXP berdasarkan perbedaan level
        if level_difference > 0:  # Musuh lebih kuat
            exp_gained = round(base_exp + (level_difference * 2.5))
        elif level_difference < 0:  # Musuh lebih lemah
            exp_gained = round(max(5, base_exp + (level_difference * 5)))  # Minimum 10 EXP
        else:  # Level sama
            exp_gained = base_exp

        self.exp += exp_gained
        print(f"{self.name} mendapatkan {exp_gained} EXP!")
        self.save_progress()
        
        if  self.exp >= self.level_up_exp:
            self.level_up()

        
    def level_up(self):
        """Meningkatkan level pemain dan mengatur ulang EXP ke 0."""

        # Hitung batas EXP baru menggunakan formula
        while self.exp >= self.level_up_exp:  # Bisa naik beberapa level sekaligus
            self.stat_points += 3  # Tambahkan stat points
            self.exp -= self.level_up_exp  # Reset EXP kelebihan
            self.level += 1  # Naik 1 level
            self.level_up_exp = round(self.level_up_exp * 1.33)  # EXP naik 1.33x

            self.hp = self.max_hp
            self.mp = self.max_mp
            self.stamina = self.max_stamina

            print(f"HP, MP, dan Stamina telah dipulihkan sepenuhnya.")
            print(f"Selamat! {self.name} naik ke level {self.level}!")

        
        print(f"EXP yang dibutuhkan untuk level berikutnya: {self.level_up_exp}")
        print(f"Stat Points tersedia: {self.stat_points}")
        self.save_progress()

    def add_to_inventory(self, item):
        self.inventory.append(item)
        self.save_progress()
        print(f"{item} telah ditambahkan ke inventory.")

    def attack_enemy(self, enemy):
        # Menghitung damage serangan ke musuh
        damage = self.attack - round((1 - (enemy.defense / 100)))
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        print(f"{self.name} menyerang {enemy.name} dan memberikan {damage} damage!")
    

    def allocate_stat_points(self):
        """Mengalokasikan stat points"""
        print(f"\nKamu memiliki {self.stat_points} poin stat untuk dialokasikan.")
        while self.stat_points > 0:
            print(f"\nPilih stat yang ingin ditingkatkan:")
            print("1. HP")
            print("2. MP")
            print("3. Attack")
            print("4. Defense")
            print("5. Agility")
            print("6. Stamina")
            print("7. Intelligence")
            print("8. Crit Chance")
            print("9. Crit Damage")
            print(f"10. Selesai alokasikan poin stat.")
            choice = input("Pilih (1-10): ")

            if choice == "1":
                self.hp += 10
                self.stat_points -= 1
                print("HP +10")
            elif choice == "2":
                self.mp += 10
                self.stat_points -= 1
                print("MP +10")
            elif choice == "3":
                self.attack += 10
                self.stat_points -= 1
                print("Attack +10")
            elif choice == "4":
                self.defense += 10
                self.stat_points -= 1
                print("Defense +10")
            elif choice == "5":
                self.agility += 8
                self.stat_points -= 1
                print("Agility 8")
            elif choice == "6":
                self.stamina += 10
                self.stat_points -= 1
                print("Stamina +10")
            elif choice == "7":
                self.intelligence += 8
                self.stat_points -= 1
                print("Intelligence +8")
            elif choice == "8":
                self.crit_chance += 0.8
                self.stat_points -= 1
                print("Crit Chance +0.8")
            elif choice == "9":
                self.crit_damage += 0.8
                self.stat_points -= 1
                print("Crit Damage +0.8")
            elif choice == "10":
                break
            else:
                print("Pilihan tidak valid! Coba lagi.")
        self.save_progress()
    
   