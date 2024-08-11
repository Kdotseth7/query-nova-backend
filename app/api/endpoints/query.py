from fastapi import APIRouter, HTTPException
from models.schema import QueryRequest, QueryResponse
from service.query_nova import QueryNova

router = APIRouter()

@router.post("/query")
async def query(request: QueryRequest):
    try:
        query_nova = QueryNova()
        result = query_nova.run(request.user_id, request.query)
        
        return {"query": request.query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))