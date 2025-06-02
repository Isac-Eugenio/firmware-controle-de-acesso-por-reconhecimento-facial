from dataclasses import dataclass
from typing import List, Any, Optional, Union

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
        