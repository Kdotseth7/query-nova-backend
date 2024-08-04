from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import query, users
from database.session import engine
from database.models import Base
import uvicorn
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Query Nova Agent is running!"}

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Query Nova Agent is healthy!"}

app.include_router(query.router, prefix="/api/v1")
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

    # Create tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Tables created successfully.")
    except Exception as e:
        logging.error(f"Error during startup: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
