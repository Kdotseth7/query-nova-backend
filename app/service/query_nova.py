from core.config import settings
from database.session import engine
from llm.openai_llm import OpenAILLM
from service.rag import Rag
from database.synthetic_db import get_db as synthetic_db
from sqlalchemy.orm import Session
import logging
import pandas as pd

class QueryNova:
    def get_schema(self, db: Session) -> dict:
        schema_info = {}
        
        # Query to get table names and their descriptions
        tables_query = """
            SELECT
                c.relname AS table_name,
                obj_description(c.oid, 'pg_class') AS table_description
            FROM
                pg_class c
            INNER JOIN
                pg_namespace n ON n.oid = c.relnamespace
            WHERE
                c.relkind = 'r'
                AND n.nspname = 'public';
        """
        tables = pd.read_sql(tables_query, db)
        
        for table in tables.itertuples():
            table_name = table.table_name
            table_description = table.table_description if table.table_description else "No description available"
            
            # Query to get column names and their descriptions for the current table
            columns_query = f"""
                SELECT
                    c.column_name,
                    col_description(a.attrelid, a.attnum) AS column_description
                FROM
                    information_schema.columns c
                JOIN
                    pg_attribute a ON c.table_name = a.attrelid::regclass::text AND c.column_name = a.attname
                WHERE
                    c.table_name = '{table_name}';
            """
            columns = pd.read_sql(columns_query, db)
            table_metadata = {}
            
            for column in columns.itertuples():
                column_name = column.column_name
                column_description = column.column_description if column.column_description else "No description available"
                table_metadata[column_name] = {"column_description": column_description}
            
            schema_info[table_name] = {
                "table_description": table_description,
                "table_metadata": table_metadata
            }
        
        return schema_info
    
    def convert_text_to_sql(text: str, relevant_tables: list) -> str:
        llm = OpenAILLM()
        prompt = f"Using these tables {relevant_tables}, convert this text to SQL: {text}"
        sql_query = llm.generate_sql(prompt)
        return sql_query
    
    def execute_query(sql_query: str) -> list:
        with engine.connect() as connection:
            result = connection.execute(sql_query)
            return [dict(row) for row in result]
        
    def run(self, user_id: str, query: str) -> list:
        schema_info = self.get_schema(synthetic_db)
        logging.info(f"Schema Info: {schema_info}")
        # filtered_tables = Rag.filter_tables(query, schema_info)
        # logging.info(f"Tables Filtered by RAG: {filtered_tables}")
        # sql_query = QueryNova.convert_text_to_sql(query, filtered_tables)
        # results = QueryNova.execute_query(sql_query)
        # return results
        