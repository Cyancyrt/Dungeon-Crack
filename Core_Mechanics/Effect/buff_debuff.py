import math
class StatusHandler:
    
    @staticmethod
    def _status_effect_dict():
        return {
            # "stun": StatusHandler._stun,
            "heal": StatusHandler._heal,
            "burn": StatusHandler._burn,    
            # "blind": StatusHandler._blind
        }
    
    @staticmethod
    def _burn( effect_type, effect_value,target, **kwargs):
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default
        
        if bonus_type == "percentage":
            bonus_value = amount / 100  # Konversi ke angka
        
        bonus_value  = int(max(math.ceil(target.stats.max_hp * bonus_value) - (target.stats.defense / 2), 1))

        
        effect_value = {**effect_value, "amount": bonus_value}
        StatusHandler._apply_Effect(effect_type, effect_value, target,**kwargs)

    @staticmethod
    def _damage_reduction( effect_type, effect_value,target, **kwargs):
        """Meningkatkan akurasi pemain"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default
        
        if bonus_type == "percentage":
            bonus_value = amount / 100  # Konversi ke angka
        
        effect_value = {**effect_value, "amount": bonus_value}
        StatusHandler._apply_buff(effect_type, effect_value, target, **kwargs)


    @staticmethod
    def _heal( effect_type, effect_value, target, **kwargs):
        if isinstance(effect_value, dict):  # Cek apakah benar dict 
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default
        
        if bonus_type == "percentage":
            bonus_value = (target.stats.health * amount) // 100  # Konversi ke angka
        else:
            bonus_value = amount  # Ambil nilai langsung jika flat
        
        effect_value = {**effect_value, "amount": bonus_value}
        StatusHandler._apply_Effect(effect_type, effect_value, target, **kwargs)
        target.stats.hp = min(target.stats.max_hp, target.stats.hp + bonus_value)
        
    @staticmethod
    def _apply_Effect(effect_type, effect_values,target, **kwargs):
        if effect_type not in target.debuffs:
            target.debuffs[effect_type] = {}  # Simpan buff sebagai angka, bukan list atau dict
        target.debuffs[effect_type] = effect_values

class Buff(StatusHandler):
    """Class for representing a buff effect."""
    @staticmethod
    def _buff_dict():
        return {
            "mana_restore": Buff._restore_mana,
            "attack_bonus": Buff._boost_attack,
            "defense_bonus": Buff._boost_def,
            "accuracy_bonus": Buff._boost_accuracy,
            "agility_bonus": Buff._boost_agility,
            "crit_chance_bonus": Buff._crit_chance_boost,
            "damage_reduction": Buff._damage_reduction,
            # "damage_bonus" : Buff._damage_boost
        }
    
    @staticmethod
    def _crit_chance_boost( effect_type, effect_value,target, **kwargs):
        """Meningkatkan akurasi pemain"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default
        
        if bonus_type == "percentage":
            bonus_value = (target.stats.crit_chance * amount) // 100  # Konversi ke angka
        else:
            bonus_value = amount  # Ambil nilai langsung jika flat
        
        effect_value = {**effect_value, "amount": bonus_value}
        Buff._apply_buff(effect_type, effect_value, target, **kwargs)
        target.stats.crit_chance += bonus_value
    


    @staticmethod
    def _restore_mana(effect_type, effect_value, target,**kwargs):
        """Memulihkan mana berdasarkan jumlah tetap atau persentase"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default

        restored_mana = (target.stats.max_mp * amount) // 100 if bonus_type == "percentage" else amount
        target.stats.mp = min(target.stats.mp + restored_mana, target.stats.max_mp)


    @staticmethod
    def _boost_attack(effect_type, effect_value,target, **kwargs):
        """Meningkatkan serangan pemain"""     
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default

        if bonus_type == "percentage":
            bonus_value = (target.stats.attack * amount) // 100  # Konversi ke angka
        else:
            bonus_value = amount  # Ambil nilai langsung jika flat
        
        effect_value = {**effect_value, "amount": bonus_value}

        Buff._apply_buff(effect_type, effect_value, target)  # Kirim angka, bukan dict
        target.stats.attack += bonus_value  # Tambahkan ke attack pemain

    @staticmethod
    def _boost_accuracy( effect_type, effect_value,target, **kwargs):
        """Meningkatkan akurasi pemain"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default

        if bonus_type == "percentage":
            bonus_value = (target.stats.accuracy * amount) // 100  # Konversi ke angka
        else:
            bonus_value = amount  # Ambil nilai langsung jika flat
        
        effect_value = {**effect_value, "amount": bonus_value}
        Buff._apply_buff(effect_type, effect_value, target)  # Kirim angka, bukan dict 
        target.stats.accuracy += bonus_value 

    @staticmethod
    def _boost_agility(effect_type, effect_value,target, **kwargs):
        """Meningkatkan kecepatan pemain"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default

        if bonus_type == "percentage":
            bonus_value = (target.stats.agility * amount) // 100  # Konversi ke angka
        else:
            bonus_value = amount  # Ambil nilai langsung jika flat
        
        effect_value = {**effect_value, "amount": bonus_value}
        Buff._apply_buff(effect_type, effect_value, target)  # Kirim angka, bukan dict
        target.stats.agility += bonus_value

    @staticmethod
    def _boost_def(effect_type, effect_value,target, **kwargs):

        """Meningkatkan pertahanan pemain"""
        if isinstance(effect_value, dict):  # Cek apakah benar dict
            amount = effect_value.get("amount", 0)  # Ambil nilai atau default 0
            bonus_type = effect_value.get("bonus_type", "default")  # Ambil atau default


        bonus_value = (target.stats.defense * amount) // 100 if bonus_type == "percentage" else amount
        effect_value = {**effect_value, "amount": bonus_value}

        Buff._apply_buff(effect_type, effect_value, target)
        target.stats.defense += bonus_value

    def _apply_buff(effect_type, effect_values,target, **kwargs):
        if effect_type not in target.buffs:
            target.buffs[effect_type] = {}  # Simpan buff sebagai angka, bukan list atau dict
        target.buffs[effect_type] = effect_values
    
   

    # def remove(self, target):
    #     if self.effect_type in target.buffs:
    #         target.buffs[self.effect_type]["amount"] -= self.value
    #         if target.buffs[self.effect_type]["amount"] <= 0:
    #             del target.buffs[self.effect_type]

class Debuff(StatusHandler):
    """Class for representing a debuff effect."""
    @staticmethod
    def _debuff_dict():
        return {
            "defense_reduction": Debuff._reduce_defense
        }
    
    @staticmethod
    def _reduce_defense(effect_type, effect_value,target, **kwargs):
        """Mengurangi pertahanan musuh"""

        if isinstance(effect_value, dict):  
            amount = effect_value.get("amount", 0)  
            bonus_type = effect_value.get("bonus_type", "flat")

            if bonus_type == "percentage":
                bonus_value = (target.defense * amount) // 100 
            else:
                bonus_value = amount  
            effect_value = {**effect_value, "amount": bonus_value}
            Debuff._apply_debuff(effect_type, effect_value, target, **kwargs)
            target.stats.defense = max(0, target.stats.defense - bonus_value)

    def _apply_debuff(effect_type, effect_values, target, **kwargs):
        if target is None:
            print(f"⚠️ Target tidak ditemukan untuk {effect_type}")
            return

        if effect_type not in target.debuffs:
            target.debuffs[effect_type] = {}  # Inisialisasi sebagai dict jika belum ada

        # Tambahkan flag "just_applied" ke dalam effect_values
        effect_values["just_applied"] = True  # Tandai bahwa efek ini baru saja diterapkan
        
        # Terapkan debuff pada target
        target.debuffs[effect_type] = effect_values
        

    # def remove(self, target):
    #     if self.effect_type in target.debuffs:
    #         target.debuffs[self.effect_type]["amount"] -= self.value
    #         if target.debuffs[self.effect_type]["amount"] <= 0:
    #             del target.debuffs[self.effect_type]

