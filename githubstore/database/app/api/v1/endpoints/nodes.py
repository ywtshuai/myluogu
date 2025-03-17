from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional, Dict, Any
from app.schemas.node import NodeCreate, NodeUpdate, NodeDelete, NodeResponse, NodesCreate, BatchNodeUpdate
from app.crud.node import node_crud
from app.api.v1.deps import get_query_params
from app.core.exceptions import NodeNotFoundError, InvalidQueryError
import json
import base64
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=NodeResponse)
async def create_node(node_create: NodeCreate):
    """创建新节点"""
    try:
        return await node_crud.create(node_create)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=Dict[str, Any])
async def create_nodes(node_create: NodesCreate):
    """
    批量创建节点
    """
    try:
        result = await node_crud.create_many(node_create.nodes)
        return {
            "created": result["nodes"],
            "count": result["count"]
        }
    except Exception as e:
        logger.error(f"Error creating nodes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=Dict[str, Any])
async def find_nodes(
        q: Optional[str] = Query(
            None,
            description="Base64 encoded JSON query dictionary",
            example="eyJsYWJlbCI6ICJQZXJzb24iLCAicHJvcGVydGllcyI6IHsiYWdlIjogMzAsICJuYW1lIjogIkpvaG4ifX0="
        )
):
    """
    查找节点

    查询参数 q 是一个 Base64 编码的 JSON 字符串，解码后应该是如下格式：
    {
        "label": "Person",
        "properties": {
            "age": 30,
            "name": "John"
        }
    }
    """
    try:
        if not q:
            raise InvalidQueryError("Query parameter is required")

        # 解码查询参数
        try:
            query_dict = json.loads(base64.b64decode(q))
        except:
            raise InvalidQueryError("Invalid query format")

        label = query_dict.get("label")
        if not label:
            raise InvalidQueryError("Label is required")

        properties = query_dict.get("properties", {})

        #logger.info(f"Searching nodes with label: {label} and properties: {properties}")

        result = await node_crud.find(label, properties)
        return result
    except NodeNotFoundError as e:
        #logger.warning(f"Node not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidQueryError as e:
        #logger.warning(f"Invalid query: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        #logger.error(f"Error while finding nodes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_nodes(
    batch_size: Optional[int] = 1000,
    page: Optional[int] = 1
):
    """获取所有节点（分页）"""
    try:
        return await node_crud.get_all(batch_size, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=Dict[str, Any])
async def update_nodes(updates: BatchNodeUpdate):
    """
    批量更新节点
    """
    try:
        result = await node_crud.update_many(updates.updates)
        return {
            "updated": result["nodes"],
            "count": result["count"]
        }
    except Exception as e:
        logger.error(f"Error updating nodes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/", response_model=Dict[str, Any])
async def delete_nodes(node_delete: NodeDelete):
    """
    批量删除节点
    """
    try:
        result = await node_crud.delete_many(node_delete.nodes)
        return {
            "deleted": result["count"],
            "message": "Nodes deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting nodes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))