from core.config import settings
from database.session import engine
from llm.openai_llm import OpenAILLM

class QueryNova:
    def convert_text_to_sql(text: str, relevant_tables: list) -> str:
        llm = OpenAILLM()
        prompt = f"Using these tables {relevant_tables}, convert this text to SQL: {text}"
        sql_query = llm.generate_sql(prompt)
        return sql_query
    
    def execute_query(sql_query: str) -> list:
        with engine.connect() as connection:
            result = connection.execute(sql_query)
            return [dict(row) for row in result]