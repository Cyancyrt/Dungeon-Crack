 def _on_turn_interval(self, **kwargs):
        """Trigger ketika setiap turn"""
        self._apply_skill_effect("turn_interval", **kwargs)