class EventDispatcher:
    def __init__(self):
        self.event_handlers = {}
        self.triggered_events = set({"turn_end"})  # Menyimpan event yang sudah terjadi
        
    def register_event(self, event_type, handler):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        if handler not in self.event_handlers[event_type]:
            self.event_handlers[event_type].append(handler)
        else:
            print(f"[DEBUG] Handler untuk event '{event_type}' sudah terdaftar, tidak perlu ditambahkan lagi.")

    def dispatch_event(self, event_type, **kwargs):
        """Memicu semua handler untuk event tertentu"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                handler(**kwargs)
        
        if event_type != "battle_start":
                self.triggered_events.add(event_type)  
              
    def is_event_triggered(self, event_type):
        """Cek apakah event sudah terjadi"""
        return event_type in self.triggered_events
    
    def reset_events(self):
        """Reset semua event setelah pertarungan selesai"""
        self.triggered_events.clear()

