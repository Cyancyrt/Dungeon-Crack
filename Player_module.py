import json

CLASSES = ["Swordsman", "Lancer", "Cleric", "Mage", "Rogue", "Archer", "Warrior"]



class Stats:
    def __init__(self, hp=100, mp=50, attack=25, defense=15, agility=15, stamina=30, intelligence=25, crit_chance=5, crit_damage=50,  max_hp=None, max_mp=None, max_stamina=None):
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.stamina = stamina
        self.intelligence = intelligence
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        # Pastikan max_hp, max_mp, dan max_stamina menerima nilai yang diberikan
        self.max_hp = max_hp if max_hp is not None else hp
        self.max_mp = max_mp if max_mp is not None else mp
        self.max_stamina = max_stamina if max_stamina is not None else stamina

    def restore(self):
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.stamina = self.max_stamina

class World:
    def __init__(self, current_world=1, current_level=1, boss_defeated=False):
        self.current_world = current_world
        self.current_level = current_level
        self.boss_defeated = boss_defeated

    def advance_level(self):
        self.current_level += 1
        self.boss_defeated = False  # Reset after advancing

class Player:
    def __init__(self, name, player_class, stats, world, level=1, exp=0, level_up_exp=100, stat_points=0, inventory=None):
        self.name = name
        self.player_class = player_class
        self.stats = stats  # Use Stats instance
        self.world = world  # Use World instance
        self.level = level  # Tambahkan level
        self.exp = exp
        self.level_up_exp = level_up_exp
        self.stat_points = stat_points
        self.inventory = inventory if inventory is not None else []


    def to_dict(self):
        """Mengonversi atribut pemain menjadi dictionary untuk disimpan"""
        return {
            "name": self.name,
            "player_class": self.player_class,
            "stats": {
                "hp": self.stats.hp,
                "mp": self.stats.mp,
                "attack": self.stats.attack,
                "defense": self.stats.defense,
                "agility": self.stats.agility,
                "stamina": self.stats.stamina,
                "intelligence": self.stats.intelligence,
                "crit_chance": self.stats.crit_chance,
                "crit_damage": self.stats.crit_damage,
                "max_hp": self.stats.max_hp,
                "max_mp": self.stats.max_mp,
                "max_stamina": self.stats.max_stamina
            },
            "exp": self.exp,
            "level_up_exp": self.level_up_exp,
            "stat_points": self.stat_points,
            "inventory": self.inventory,
            "world": {
                "current_world": self.world.current_world,
                "current_level": self.world.current_level,
                "boss_defeated": self.world.boss_defeated
            }
        }

    @classmethod
    def from_dict(cls, data):
        # Ambil data untuk Stats dan World
        stats_data = data.get('stats', {})
        stats = Stats(**stats_data)  # Membuat objek Stats dari data yang ada
        world_data = data.get('world', {})
        world = World(**world_data)  # Membuat objek World dari data yang ada
        return cls(name=data['name'],
                   player_class=data['player_class'],
                   stats=stats,
                   world=world,
                   exp=data['exp'],
                   level_up_exp=data['level_up_exp'],
                   stat_points=data['stat_points'],
                   inventory=data['inventory'])
    
    def save_progress(self):
        with open("player_save.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print("✅ Progress berhasil disimpan!")

        
    def display_stats(self):
        stats = self.to_dict()

        # Menghapus inventory karena tidak ingin ditampilkan
        stats.pop("inventory", None)

        # Pisahkan stats dan world dari dictionary utama
        player_stats = stats.pop('stats', {})
        world_info = stats.pop('world', {})

        # Pastikan crit_chance dan crit_damage ditampilkan dengan simbol persen
        player_stats['crit_chance'] = f"{player_stats.get('crit_chance', 0)}%"  # Menambahkan persen pada crit_chance
        player_stats['crit_damage'] = f"{player_stats.get('crit_damage', 0)}%"  # Menambahkan persen pada crit_damage

        # Gabungkan semua statistik ke dalam satu dictionary
        all_stats = {**stats, **player_stats, **world_info}

        # Ubah stats ke dalam bentuk list of tuples (key, value) untuk ditampilkan
        stat_items = list(all_stats.items())

        # Tentukan titik tengah untuk membagi menjadi dua kolom
        half = len(stat_items) // 2


        # Menampilkan dua kolom untuk statistik
        for left, right in zip(stat_items[:half], stat_items[half:]):
            # Ganti underscore (_) dengan spasi pada key
            left_key = left[0].replace('_', ' ')
            right_key = right[0].replace('_', ' ')

            # Format nilai
            left_value = str(left[1]) if not isinstance(left[1], str) else left[1]
            right_value = str(right[1]) if not isinstance(right[1], str) else right[1]

            print(f"{left_key:<15}: {left_value:<10}  |  {right_key:<15}: {right_value}")

        # Jika jumlah item ganjil, cetak yang tersisa
        if len(stat_items) % 2 != 0:
            last_key, last_value = stat_items[-1]
            last_key = last_key.replace('_', ' ')  # Ganti underscore (_) dengan spasi
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

            self.stats.restore()

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
        damage = self.stats.attack - round((1 - (enemy.defense / 100)))
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        print(f"{self.name} menyerang {enemy.name} dan memberikan {damage} damage!")
    

    def allocate_stat_points(self):
        """Mengalokasikan stat points"""
        if self.stat_points <= 0:
            print(f"Maaf, {self.name}, Anda tidak memiliki poin untuk dialokasikan.")
            return
        else :
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
    
   