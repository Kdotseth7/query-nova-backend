TABLE_FILTER_PROMPT = """
### Task: Identify Relevant Database Tables

Determine which database tables are relevant to answering the user's specific query based on the descriptions of each table in the database schema.

### Guidelines:
1. **Analyze the Query:** Understand the user's request.
2. **Use Table Descriptions:** Carefully review the table descriptions provided below to select the appropriate tables that could contribute to the answer.
3. **List All Relevant Tables:** Identify all tables that could contribute to the answer and return them as a list.

### Table Descriptions:
{tables_schema}
"""

SQL_GENERATION_PROMPT = """
### Task: Generate SQL Query

Write an SQL query that retrieves the necessary information from the relevant database tables to answer the user's query.

### Guidelines:
1. **Use Filtered Tables:** Utilize the list of filtered tables to construct the SQL query.
2. **Use Table Schema:** Refer to the schema descriptions to understand the structure of the tables and generate an appropriate query using correct table names and columns.

### Filtered Tables:
{filtered_tables}
### Tables Schema:
{tables_schema}
"""