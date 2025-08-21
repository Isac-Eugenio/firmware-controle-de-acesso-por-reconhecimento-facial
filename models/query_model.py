from dataclasses import dataclass
from typing import List, Any, Optional, Union


@dataclass
class QueryModel:
    table: str
    columns: Optional[List[str]] = None
    condition: Optional[str] = None
    values: Optional[Union[List[Any], dict]] = None
    query: Optional[str] = None
    
    def select(self, values: dict = None):
        if values is not None:
            self.values = values

        # Define colunas
        if self.columns is None:
            self.columns = "*"
        else:
            if isinstance(self.columns, str):
                self.columns = [self.columns]
            elif not isinstance(self.columns, (list, tuple)):
                raise Exception(f"`columns` inválido: {type(self.columns)}")
            self.columns = ", ".join(self.columns)

        # Começa a montar query
        self.query = f"SELECT {self.columns} FROM {self.table}"

        # Cria WHERE
        where_parts = []

        if self.values:
            # Prioriza values, gera parâmetros bind
            conditions = [f"{key} = :{key}" for key in self.values.keys()]
            where_parts.extend(conditions)
        
        # Mantém condição antiga se existir
        if self.condition:
            where_parts.append(self.condition)

        # Adiciona WHERE à query se houver alguma parte
        if where_parts:
            self.query += " WHERE " + " AND ".join(where_parts)


    def insert(self):
        if not isinstance(self.values, dict):
            raise Exception("values não é um Map (Obrigatório)")
        columns = ", ".join(self.values.keys())
        placeholders = ", ".join([f":{key}" for key in self.values.keys()])
        self.query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"

    def delete(self):
        if not self.values or not isinstance(self.values, dict):
            raise Exception("Para deletar, forneça um dicionário de condições em 'values'.")
        conditions = [f"{key} = :{key}" for key in self.values.keys()]
        where_clause = " AND ".join(conditions)
        self.query = f"DELETE FROM {self.table} WHERE {where_clause}"

    def update(self, new_query: "QueryModel"):
        if not self.values or not isinstance(self.values, dict):
            raise Exception("Forneça um dicionário de condições em 'values' para a cláusula WHERE.")
        if not new_query or not isinstance(new_query.values, dict):
            raise Exception("Forneça um dicionário de dados a serem atualizados em 'new_query.values' para a cláusula SET.")

        set_clause = ", ".join([f"{key} = :set_{key}" for key in new_query.values.keys()])
        where_clause = " AND ".join([f"{key} = :{key}" for key in self.values.keys()])
        self.query = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"

        new_values_prefixed = {f"set_{k}": v for k, v in new_query.values.items()}
        self.values = {**new_values_prefixed, **self.values}

    def count(self):
        self.query = f"SELECT COUNT(*) as total FROM {self.table}"
        where_parts = []

        if self.values:
            conditions = [f"{key} = :{key}" for key in self.values.keys()]
            where_parts.extend(conditions)
        elif self.condition:
            where_parts.append(self.condition)

        if where_parts:
            self.query += " WHERE " + " AND ".join(where_parts)
