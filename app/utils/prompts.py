class Prompts:
    @staticmethod
    def textToSqlPrompt(text: str, tables: str) -> str:
        return f"""
        Convert the following text to SQL queries:
        {text}
    """