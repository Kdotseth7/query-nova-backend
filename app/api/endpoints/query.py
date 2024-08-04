from fastapi import APIRouter, HTTPException
from models.schema import QueryRequest, QueryResponse

router = APIRouter()

# @router.post("/query")
# async def query_database(request: QueryRequest):
#     try:
#         filtered_tables = filter_tables(request.query, table_embeddings)
#         sql_query = generate_sql(request.query, filtered_tables)
#         results = execute_query(sql_query, connection_string)
#         return {"sql_query": sql_query, "results": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))