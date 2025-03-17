from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List


class RelationshipBase(BaseModel):
    type: str = Field(..., description="关系类型")
    start_node: Dict[str, Any] = Field(..., description="起始节点")
    end_node: Dict[str, Any] = Field(..., description="终止节点")
    properties: Dict[str, Any] = Field(default={}, description="关系属性")

    class Config:
        schema_extra = {
            "example": {
                "type": "ACTED_IN",
                "start_node": {
                    "label": "Person",
                    "properties": {"name": "Tom Hanks"}
                },
                "end_node": {
                    "label": "Movie",
                    "properties": {"title": "Forrest Gump"}
                },
                "properties": {"role": "Forrest"}
            }
        }

class RelationshipCreate(RelationshipBase):
    pass

class RelationshipsCreate(BaseModel):
    relationships: List[RelationshipBase]


class RelationshipUpdate(BaseModel):
    conditions: RelationshipBase  # 用于查找要更新的关系的条件
    new_properties: Dict[str, Any]  # 新的属性值

class BatchRelationshipUpdate(BaseModel):
    updates: List[RelationshipUpdate]

class RelationshipDelete(BaseModel):
    relationships: List[RelationshipBase]

class RelationshipResponse(BaseModel):
    relationship: Dict[str, Any]
    message: Optional[str] = None