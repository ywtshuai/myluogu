from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class NodeBase(BaseModel):
    label: str = Field(..., description="节点标签")
    properties: Dict[str, Any] = Field(..., description="节点属性")

    class Config:
        schema_extra = {
            "example": {
                "label": "Person",
                "properties": {"name": "John", "age": 30}
            }
        }

class NodeCreate(NodeBase):
    pass

class NodesCreate(BaseModel):
    nodes: List[NodeCreate]

class NodeUpdate(BaseModel):
    conditions: NodeBase
    new_properties: Dict[str, Any] = Field(..., description="新的节点属性")

class BatchNodeUpdate(BaseModel):
    updates: List[NodeUpdate]

class NodeDelete(BaseModel):
    nodes: List[NodeBase]

class NodeResponse(BaseModel):
    node: Dict[str, Any]
    message: Optional[str] = None

class QueryParams(BaseModel):
    labels: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None
    relationships: Optional[Dict[str, Dict[str, Any]]] = None
    limit: Optional[int] = 10
    skip: Optional[int] = 0
    order_by: Optional[str] = None