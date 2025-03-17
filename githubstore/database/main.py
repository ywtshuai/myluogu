from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.middleware.logging import LoggingMiddleware
from app.core.exceptions import NodeNotFoundError, InvalidQueryError, DatabaseError, RelationshipNotFoundError
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志中间件
app.add_middleware(LoggingMiddleware)

# 路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 异常处理
@app.exception_handler(NodeNotFoundError)
async def node_not_found_handler(request, exc):
    return {"error": str(exc)}, 404

@app.exception_handler(InvalidQueryError)
async def invalid_query_handler(request, exc):
    return {"error": str(exc)}, 400

@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    return {"error": "Database error occurred"}, 500

@app.exception_handler(RelationshipNotFoundError)
async def relationship_not_found_handler(request, exc):
    return {"error": str(exc)}, 404

@app.on_event("startup")
async def startup_event():
    logging.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)