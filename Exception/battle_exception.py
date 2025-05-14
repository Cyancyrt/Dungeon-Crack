# File: exceptions.py
class InvalidActionChoice(Exception):
    """Exception ketika pilihan aksi tidak valid"""
    pass

class ActionCancelled(Exception):
    """Exception ketika pemain membatalkan aksi"""
    pass

class BattleEnded(Exception):
    """Exception untuk menandai akhir pertempuran"""
    pass

# File: exceptions.py
class SkillNotFound(Exception):
    """Exception ketika skill yang dicari tidak ditemukan."""
    pass

class InsufficientMP(Exception):
    """Exception ketika MP pemain tidak cukup untuk menggunakan skill."""
    pass

class SkillOnCooldown(Exception):
    """Exception ketika skill sedang dalam cooldown."""
    pass

class InvalidSkillEffect(Exception):
    """Exception ketika skill memiliki efek yang tidak valid."""
    pass

class InvalidTargetForEffect(Exception):
    """Exception ketika target efek skill tidak valid."""
    pass

class EventNotRegisteredError(Exception):
    """Exception untuk event yang tidak terdaftar pada dispatcher."""
    pass

class SkillHandlerNotFoundError(Exception):
    """Exception untuk pemain yang tidak memiliki skill handler yang valid."""
    pass
