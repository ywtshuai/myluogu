from fastapi import APIRouter
from app.api.v1.endpoints import nodes, relationships

api_router = APIRouter()

# 注册节点相关路由
api_router.include_router(
    nodes.router,
    prefix="/nodes",
    tags=["nodes"]
)

# 注册关系相关路由
api_router.include_router(
    relationships.router,
    prefix="/relationships",
    tags=["relationships"]
)