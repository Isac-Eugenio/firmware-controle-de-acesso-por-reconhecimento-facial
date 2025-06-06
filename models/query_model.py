from dataclasses import dataclass
from typing import List, Any, Optional, Union

from core.errors.database_exception import *
from models.query_model import *


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
                raise DatabaseQueryError("values não é um Map (Obrigatório)")
            columns = ", ".join(self.values.keys())

            # Criar os placeholders nomeados (usando :coluna)
            placeholders = ", ".join([f":{key}" for key in self.values.keys()])

            # Construção da query
            self.query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        
        except DatabaseException:
            raise

    def delete(self):

        try:
            if not self.values or not isinstance(self.values, dict):
                raise DatabaseQueryError("Para deletar, forneça um dicionário de condições em 'values'.")
            
            conditions = [f"{key} = :{key}" for key in self.values.keys()]
            where_clause = " AND ".join(conditions)
            self.query = f"DELETE FROM {self.table} WHERE {where_clause}"
        except DatabaseException:
            raise

    def update(self, new_query: 'QueryModel'):
        try:
            if not self.values or not isinstance(self.values, dict):
                raise DatabaseQueryError("Forneça um dicionário de condições em 'values' para a cláusula WHERE.")

            if not new_query or not isinstance(new_query.values, dict):
                raise DatabaseQueryError("Forneça um dicionário de dados a serem atualizados em 'new_query.values' para a cláusula SET.")

            # Cria a parte SET do SQL com prefixo nos parâmetros para evitar colisão com WHERE
            set_clause = ", ".join([f"{key} = :set_{key}" for key in new_query.values.keys()])

            # Cria a parte WHERE da query usando os valores atuais
            where_clause = " AND ".join([f"{key} = :{key}" for key in self.values.keys()])

            # Monta a query final
            self.query = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"

            # Junta os dicionários de parâmetros com prefixos distintos
            new_values_prefixed = {f"set_{k}": v for k, v in new_query.values.items()}
            condition_values = self.values  # já está no formato correto


            self.values = {**new_values_prefixed, **condition_values}

        except DatabaseException:
            raise

    def count(self):
        try:
            self.query = f"SELECT COUNT(*) as total FROM {self.table}"

            where_parts = []

            if self.values:
                conditions = [f"{key} = :{key}" for key in self.values.keys()]
                where_parts.extend(conditions)
            elif self.condition:
                where_parts.append(self.condition)

            if where_parts:
                self.query += " WHERE " + " AND ".join(where_parts)

        except Exception as e:
            raise DatabaseQueryError("Erro ao montar a query COUNT", details=str(e)) from e
