import hashlib
import random

import hashlib
import random


class ApiUtils:
    @staticmethod
    def _generate_id() -> str:
        return str(random.randint(0, 99999999)).zfill(8)

    @staticmethod
    def _ensure_str_values(data: dict) -> dict:
        return {key: f"'{value}'" for key, value in data.items()}

    @staticmethod
    def is_empty_list(lst) -> list:
        return [] if not lst else lst

    @staticmethod
    def _hash_sha256(s: str) -> str:
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    @staticmethod
    def _is_sha256_hash(s: str) -> bool:
        if len(s) != 64:
            return False
        try:
            int(s, 16)  # testa se é hexadecimal
            return True
        except ValueError:
            return False

    @staticmethod
    def _limpar_dict(d: dict) -> dict:
        return {k: v for k, v in d.items() if v not in ("", None, [], {})}

    @staticmethod
    def _null_or_empty_columns(d: dict) -> list[str]:
        return [k for k, v in d.items() if v in ("", None, [], {})]
