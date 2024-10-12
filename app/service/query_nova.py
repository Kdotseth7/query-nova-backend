from database.session import engine
from llm.openai_llm import OpenAILLM
from service.rag import Rag
from database.synthetic_db import get_db
from sqlalchemy.orm import Session
import logging
import traceback
import pandas as pd
from typing import List
from models.pydantic_models import LLM_Table_Filter, PydanticSqlQuery
from utils.prompts import TABLE_FILTER_PROMPT, SQL_GENERATION_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.chat import ChatMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryNova:
    
    openai_llm = OpenAILLM()
    llm = openai_llm.initialize_gpt4()
    
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
    
    def execute_query(self, sql_query: str, db: Session) -> list:
        engine = db.get_bind()
        try:
            df = pd.read_sql(sql_query, engine)
            # logger.info(f"Query Results: {df}")
            return df.to_dict(orient="records")
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
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
        combined_schema = ""
        for table in schema_info:
            combined_schema += table + "\n"
        # logger.info(f"Combined Schema: {combined_schema}")
        
        try:
            prompt_messages = List = []
            prompt_messages.append(ChatMessage(role="system", content=TABLE_FILTER_PROMPT))
            prompt_messages.append(ChatMessage(role="user", content=f"Question: {query}"))
            prompt = ChatPromptTemplate.from_messages(prompt_messages)
            chain = prompt | self.llm.with_structured_output(LLM_Table_Filter)
            response = chain.invoke({"tables_schema": combined_schema})
            logger.info(f"LLM Table Filter Response with reasoning: {response}")
            logger.info(f"Tables Filtered by LLM: {response.dict()}")
            filtered_tables = [item['table_name'] for item in response.dict()["tables"]]
            return filtered_tables
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback: {traceback_str}")
            return {"status": "error", "message": str(e)}
        
        
    def generate_sql_query(self, query: str, filtered_tables: list, schema_info: list) -> str:
        combined_schema = ""
        for table in schema_info:
            combined_schema += table + "\n"
        # logger.info(f"Combined Schema: {combined_schema}")
        
        try:
            prompt_messages = List = []
            prompt_messages.append(ChatMessage(role="system", content=SQL_GENERATION_PROMPT))
            prompt_messages.append(ChatMessage(role="user", content=f"Question: {query}"))
            prompt = ChatPromptTemplate.from_messages(prompt_messages)
            chain = prompt | self.llm.with_structured_output(PydanticSqlQuery)
            response = chain.invoke({"tables_schema": combined_schema, "filtered_tables": filtered_tables})
            logger.info(f"Generated SQL Query with reasoning: {response}")
            sql_query = response.dict()["sql_query"]
            return sql_query
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback: {traceback_str}")
            return {"status": "error", "message": str(e)}
            
        
    def run(self, user_id: str, query: str) -> list:
        with get_db() as db:
            schema_info = self.get_schema(db)
            # logging.info(f"Schema Info: {schema_info}")
            
        combined_descriptions = self.generate_table_descriptions(schema_info)
        
        try:
            rag = Rag()
            filtered_tables_rag, filtered_tables_schema_rag = rag.filter_tables(query, combined_descriptions)
            logger.info(f"Tables Filtered by RAG: {filtered_tables_rag}")
            
            # Filter table using LLM by passing tables filtered by RAG with their schema info using Zero-shot Prompt
            filtered_tables_llm = self.filter_tables_llm(query, filtered_tables_schema_rag)
            
            sql_query = self.generate_sql_query(query, filtered_tables_llm, filtered_tables_schema_rag)
            
            with get_db() as db:
                df = self.execute_query(sql_query, db)
                if len(df) == 0:
                    return {"status": "error", "message": "No results found for the query."}
                return df
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.error(f"Traceback: {traceback_str}")
            return {"status": "error", "message": str(e)}
    