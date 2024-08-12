from database.session import engine
from llm.openai_llm import OpenAILLM
from service.rag import Rag
from database.synthetic_db import get_db
from sqlalchemy.orm import Session
import logging
import pandas as pd


class QueryNova:
    def get_schema(self, db: Session) -> list:
        schema_info = []

        engine = db.get_bind()

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
        tables = pd.read_sql(tables_query, engine)

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
            columns = pd.read_sql(columns_query, engine)
            table_metadata = []
            
            for column in columns.itertuples():
                column_name = column.column_name
                column_description = column.column_description if column.column_description else "No description available"
                table_metadata.append({
                    "column_name": column_name,
                    "column_description": column_description
                })
            
            schema_info.append({
                "table_name": table_name,
                "table_description": table_description,
                "table_metadata": table_metadata
            })

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
        
    def generate_table_descriptions(self, schema_info: list) -> list:
        table_descriptions = []
        for table in schema_info:
            table_name = table["table_name"]
            table_description = table["table_description"]
            table_metadata = table["table_metadata"]
            
            # Combine the table name, description, and metadata into a single string
            full_description = f"Table Name: {table_name}\nTable Description: {table_description}\n"
            full_description += "Table Metadata:\n"
            
            for column in table_metadata:
                column_name = column["column_name"]
                column_description = column["column_description"]
                full_description += f"Column Name: {column_name}\nColumn Description: {column_description}\n"
            
            table_descriptions.append(full_description.strip())
        
        return table_descriptions
    
    
    def filter_tables_llm(self, query: str, schema_info: list) -> list:
        openai_llm = OpenAILLM()
        
        combined_schema = ""
        for table in schema_info:
            combined_schema += table + "\n"
            
        logging.info(f"Combined Schema: {combined_schema}")
        
        filtered_tables = openai_llm.generate_response(query, combined_schema)

        
    def run(self, user_id: str, query: str) -> list:
        with get_db() as db:
            schema_info = self.get_schema(db)
            # logging.info(f"Schema Info: {schema_info}")
            
        combined_descriptions = self.generate_table_descriptions(schema_info)
        
        rag = Rag()
        filtered_tables_rag, filtered_tables_schema_rag = rag.filter_tables(query, combined_descriptions)
        logging.info(f"Tables Filtered by RAG: {filtered_tables_rag}")
        
        # Filter table using LLM by passing tables filtered by RAG with their schema info using Zero-shot Prompt
        filtered_tables_llm = self.filter_tables_llm(query, filtered_tables_schema_rag)
        
        # sql_query = self.convert_text_to_sql(self, query, filtered_tables)
        # results = self.execute_query(sql_query)
        return filtered_tables_rag
    