from typing import Dict, Any, Optional, List
from app.db.neo4j import get_db
from app.schemas.relationship import RelationshipCreate, RelationshipUpdate, RelationshipDelete, RelationshipBase
from app.core.exceptions import RelationshipNotFoundError, NodeNotFoundError
from app.utils.cache import cache_result
from app.models.relationship import BaseRelationship
from app.models.node import BaseNode
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class RelationshipCRUD:
    def __init__(self):
        self.db = get_db()

    def _create_relationship_instance(
            self,
            rel_type: str,
            start_node: Dict[str, Any],
            end_node: Dict[str, Any],
            properties: Dict[str, Any]
    ) -> BaseRelationship:
        """创建关系实例"""
        relationship = BaseRelationship()
        relationship.set_type(rel_type)

        # 添加基本属性
        properties['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 设置起始和终止节点
        relationship.start_node = self._create_node_instance(
            start_node['label'],
            start_node['properties']
        )
        relationship.end_node = self._create_node_instance(
            end_node['label'],
            end_node['properties']
        )

        for key, value in properties.items():
            setattr(relationship, key, value)

        return relationship

    def _create_node_instance(self, label: str, properties: Dict[str, Any]) -> BaseNode:
        """创建节点实例"""
        node = BaseNode()
        node.add_label(label)
        for key, value in properties.items():
            setattr(node, key, value)
        return node

    def _update_relationship_instance(
            self,
            relationship: BaseRelationship,
            properties: Dict[str, Any]
    ) -> BaseRelationship:
        """更新关系实例"""
        properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key, value in properties.items():
            setattr(relationship, key, value)

        return relationship

    async def create_one(
            self,
            relationship: RelationshipCreate
    ) -> Dict[str, Any]:
        """创建单个关系"""
        try:
            rel = await self.db.create_relationship(
                rel_type=relationship.type,
                start_node=relationship.start_node,
                end_node=relationship.end_node,
                properties=relationship.properties
            )

            return {
                "relationship": rel.to_dict()
            }
        except Exception as e:
            logger.error(f"Error in create_one: {e}")
            raise

    async def create_many(
            self,
            relationships: List[RelationshipBase]
    ) -> Dict[str, Any]:
        """批量创建关系"""
        try:
            created_rels = []
            for rel_data in relationships:
                rel = await self.db.create_relationship(
                    rel_type=rel_data.type,
                    start_node=rel_data.start_node,
                    end_node=rel_data.end_node,
                    properties=rel_data.properties
                )
                created_rels.append(rel)

            return {
                "relationships": [rel.to_dict() for rel in created_rels],
                "count": len(created_rels)
            }
        except Exception as e:
            logger.error(f"Error in create_many: {e}")
            raise

    async def get_all(
            self,
            batch_size: int = 1000,
            page: int = 1,
            rel_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取所有关系
        支持分页和关系类型过滤
        """
        try:
            skip = (page - 1) * batch_size
            relationships = await self.db.get_all_relationships(
                skip=skip,
                limit=batch_size,
                rel_type=rel_type
            )

            return {
                "relationships": [rel.to_dict() for rel in relationships],
                "count": len(relationships),
                "page": page,
                "batch_size": batch_size
            }
        except Exception as e:
            logger.error(f"Error in get_all: {e}")
            raise


    async def find(
            self,
            rel_type: str,
            start_node: Dict[str, Any],
            end_node: Dict[str, Any],
            properties: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """查找关系"""
        try:
            relationships = await self.db.find_relationship(
                rel_type=rel_type,
                start_node=start_node,
                end_node=end_node,
                properties=properties
            )

            return {
                "relationships": [rel.to_dict() for rel in relationships],
                "count": len(relationships)
            }
        except Exception as e:
            logger.error(f"Error in find: {e}")
            raise

    async def update_many(
            self,
            updates: List[RelationshipUpdate]
    ) -> Dict[str, Any]:
        """批量更新关系"""
        try:
            updated_rels = []
            for update in updates:
                conditions = {
                    "type": update.conditions.type,
                    "start_node": update.conditions.start_node,
                    "end_node": update.conditions.end_node,
                }

                rels = await self.db.update_relationship(
                    conditions=conditions,
                    new_properties=update.new_properties
                )
                updated_rels.extend(rels)

            return {
                "relationships": [rel.to_dict() for rel in updated_rels],
                "count": len(updated_rels)
            }
        except Exception as e:
            logger.error(f"Error in update_many: {e}")
            raise

    async def delete_many(
            self,
            relationships: List[RelationshipBase]
    ) -> Dict[str, Any]:
        """批量删除关系"""
        try:
            total_deleted = 0
            for rel_data in relationships:
                conditions = {
                    "type": rel_data.type,
                    "start_node": rel_data.start_node,
                    "end_node": rel_data.end_node
                }

                deleted_count = await self.db.delete_relationship(conditions)
                total_deleted += deleted_count

            return {
                "count": total_deleted
            }
        except Exception as e:
            logger.error(f"Error in delete_many: {e}")
            raise
    async def get_all(
            self,
            batch_size: int,
            page: int
    ) -> Dict[str, Any]:
        skip = (page - 1) * batch_size
        relationships = await self.db.get_all_relationships(skip, batch_size)

        # 转换所有关系为BaseRelationship实例
        rel_instances = []
        for rel in relationships:
            if not isinstance(rel, BaseRelationship):
                rel_dict = dict(rel)
                rel_instance = self._create_relationship_instance(
                    rel.type(),
                    rel.start_node,
                    rel.end_node,
                    rel_dict
                )
                rel_instances.append(rel_instance)
            else:
                rel_instances.append(rel)

        return {
            "relationships": [rel.to_dict() for rel in rel_instances],
            "page": page,
            "batch_size": batch_size
        }

relationship_crud = RelationshipCRUD()