import random

class ApiUtils:
    def _generate_id(self):
        return str(random.randint(0, 99999999)).zfill(8)
    
    def _ensure_str_values(self, data: dict):
        return {key: f"'{value}'" for key, value in data.items()}