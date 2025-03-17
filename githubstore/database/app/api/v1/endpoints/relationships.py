from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any, Optional, List
import base64
import json
import logging
from app.crud.relationship import relationship_crud
from app.schemas.relationship import (
    RelationshipBase,
    RelationshipCreate,
    RelationshipsCreate,
    RelationshipUpdate,
    BatchRelationshipUpdate,
    RelationshipDelete,
    RelationshipResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def find_relationship(
        q: Optional[str] = Query(
            None,
            description="Base64 encoded JSON query dictionary"
        )
):
    """
    查找关系
    查询参数 q 是一个 Base64 编码的 JSON 字符串，格式应符合 RelationshipBase 模型
    """
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        try:
            query_dict = json.loads(base64.b64decode(q))
            # 使用 Pydantic 模型验证
            query = RelationshipBase(**query_dict)
        except:
            raise HTTPException(status_code=400, detail="Invalid query format")

        result = await relationship_crud.find(
            rel_type=query.type,
            start_node=query.start_node,
            end_node=query.end_node,
            properties=query.properties
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding relationships: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=RelationshipResponse)
async def create_relationship(
        relationship: RelationshipCreate
):
    """创建单个关系"""
    try:
        result = await relationship_crud.create_one(relationship)
        return {
            "relationship": result["relationship"],
            "message": "Relationship created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating relationship: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=Dict[str, Any])
async def create_relationships(
        relationships: RelationshipsCreate
):
    """批量创建关系"""
    try:
        result = await relationship_crud.create_many(relationships.relationships)
        return result
    except Exception as e:
        logger.error(f"Error creating relationships: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=Dict[str, Any])
async def update_relationships(
        updates: BatchRelationshipUpdate
):
    """批量更新关系"""
    try:
        result = await relationship_crud.update_many(updates.updates)
        return result
    except Exception as e:
        logger.error(f"Error updating relationships: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/", response_model=Dict[str, Any])
async def delete_relationships(
        relationships: RelationshipDelete
):
    """批量删除关系"""
    try:
        result = await relationship_crud.delete_many(relationships.relationships)
        return result
    except Exception as e:
        logger.error(f"Error deleting relationships: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=Dict[str, Any])
async def get_all_relationships(
        batch_size: int = Query(1000, description="每页数量"),
        page: int = Query(1, description="页码"),
        rel_type: Optional[str] = Query(None, description="可选的关系类型过滤")
):
    """
    获取所有关系
    - batch_size: 每页返回的关系数量
    - page: 页码，从1开始
    - rel_type: 可选的关系类型过滤
    """
    try:
        result = await relationship_crud.get_all(
            batch_size=batch_size,
            page=page,
            rel_type=rel_type
        )
        return result
    except Exception as e:
        logger.error(f"Error getting all relationships: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))