CLASSES = ["Swordsman", "Lancer", "Cleric", "Mage", "Rogue", "Archer", "Warrior"]
class Player:
    def __init__(self, name, player_class, hp, mp, attack, defense, agility, stamina, intelligence, crit_chance, crit_damage, level=1, stat_points=0, inventory=None):
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
            "inventory": self.inventory
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def display_stats(self):
        stats = self.to_dict()
        stats["crit_chance"] = f"{self.crit_chance}%"
        stats["crit_damage"] = f"{self.crit_damage}%"
        return stats

    def level_up(self):
        """Fungsi untuk menangani level-up pemain"""
        self.level += 1
        self.stat_points += 3  # Dapatkan 3 poin setiap level-up
        print(f"\nLevel Up! Sekarang levelmu adalah {self.level}. Kamu mendapatkan 3 poin stat!")

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"{item} telah ditambahkan ke inventory.")
        
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
   