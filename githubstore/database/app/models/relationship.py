from datetime import datetime
from typing import Dict, Any, Optional
from .node import BaseNode


class BaseRelationship:
    def __init__(
            self,
            type: str = None,
            start_node: BaseNode = None,
            end_node: BaseNode = None,
            **properties
    ):
        self.id = None  # Neo4j内部ID
        self.type = type
        self.start_node = start_node
        self.end_node = end_node
        self.created_at = properties.pop('created_at', datetime.utcnow())
        self.updated_at = properties.pop('updated_at', datetime.utcnow())

        # 设置其他属性
        for key, value in properties.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": str(self.id) if self.id else None,
            "type": self.type,
            "start_node": self.start_node.to_dict() if self.start_node else None,
            "end_node": self.end_node.to_dict() if self.end_node else None,
            "properties": {
                key: value
                for key, value in self.__dict__.items()
                if not key.startswith('_')
                   and key not in ['id', 'type', 'start_node', 'end_node']
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseRelationship':
        """从字典创建实例"""
        start_node = BaseNode.from_dict(data['start_node']) if data.get('start_node') else None
        end_node = BaseNode.from_dict(data['end_node']) if data.get('end_node') else None

        rel = cls(
            type=data.get('type'),
            start_node=start_node,
            end_node=end_node,
            **data.get('properties', {})
        )
        rel.id = data.get('id')
        return rel