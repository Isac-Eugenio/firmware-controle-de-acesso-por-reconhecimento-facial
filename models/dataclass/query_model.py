from dataclasses import dataclass
from typing import List, Any, Optional, Union

from core.errors.database_exception import *

@dataclass
class QueryModel:
    table: str
    columns: Optional[List[str]] = None
    condition: Optional[str] = None
    values: Optional[Union[List[Any], dict]] = None
    query: Optional[str] = None

    def select(self):
        if self.columns is None:
            self.columns = "*"
        else:
            self.columns = ", ".join(self.columns)

        self.query = f"SELECT {self.columns} FROM {self.table}"
        if self.condition:
            self.query += f" WHERE {self.condition}"
    
    def insert(self):
        try:
            if not isinstance(self.values, dict):
                raise DatabaseQueryError("Values não é um Map (Obrigatório)")
            columns = ", ".join(self.values.keys())

            # Criar os placeholders nomeados (usando :coluna)
            placeholders = ", ".join([f":{key}" for key in self.values.keys()])

            # Construção da query
            self.query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        
        except DatabaseException:
            raise