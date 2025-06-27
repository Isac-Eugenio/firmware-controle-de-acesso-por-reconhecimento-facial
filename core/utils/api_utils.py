import hashlib
import random

class ApiUtils:
    def _generate_id(self):
        return str(random.randint(0, 99999999)).zfill(8)
    
    def _ensure_str_values(self, data: dict):
        return {key: f"'{value}'" for key, value in data.items()}
    
    is_empty_list = lambda list: [] if not list else list
    
    def _hash_sha256(self, s: str) -> str:
     return hashlib.sha256(s.encode("utf-8")).hexdigest()


    def _is_sha256_hash(self, s: str) -> bool:
        if len(s) != 64:
            return False
        try:
            int(s, 16)  # testa se é hexadecimal
            return True
        except ValueError:
            return False
    