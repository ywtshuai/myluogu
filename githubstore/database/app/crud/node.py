from typing import Dict, Any, Optional, List, Type
from app.db.neo4j import get_db
from app.schemas.node import NodeCreate, NodeUpdate, NodeDelete, NodeBase
from app.core.exceptions import NodeNotFoundError
from app.utils.cache import cache_result
from app.models.node import BaseNode
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NodeCRUD:
    def __init__(self):
        self.db = get_db()

    def _create_node_instance(self, label: str, properties: Dict[str, Any]) -> BaseNode:
        """创建节点实例"""
        node = BaseNode()
        node.add_label(label)

        # 添加基本属性
        properties['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key, value in properties.items():
            setattr(node, key, value)

        return node

    def _update_node_instance(self, node: BaseNode, properties: Dict[str, Any]) -> BaseNode:
        """更新节点实例"""
        properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key, value in properties.items():
            setattr(node, key, value)

        return node

    @cache_result()
    async def find(
            self,
            label: str,
            properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        查找节点

        参数:
            - label: 节点标签
            - properties: 节点属性查询条件
        """
        try:
            nodes = await self.db.find_node(label, properties)

            return {
                "nodes": [node.to_dict() for node in nodes],
                "count": len(nodes)
            }
        except Exception as e:
            #logging.error(f"Error in find method: {e}")
            raise

    async def create(self, node_data: NodeCreate) -> Dict[str, Any]:
        # 创建BaseNode实例
        node_instance = self._create_node_instance(
            node_data.label,
            node_data.properties
        )

        # 保存到数据库
        node = await self.db.create_node(node_instance)
        return {"node": node.to_dict()}

    async def update(self, node_data: NodeUpdate) -> Dict[str, Any]:
        # 查找现有节点
        existing_node = await self.db.find_node(
            node_data.label,
            node_data.properties
        )

        if not existing_node:
            raise NodeNotFoundError("Node not found")

        # 转换为BaseNode实例并更新
        if not isinstance(existing_node, BaseNode):
            node_instance = self._create_node_instance(
                node_data.label,
                dict(existing_node)
            )
        else:
            node_instance = existing_node

        updated_node = self._update_node_instance(
            node_instance,
            node_data.new_properties
        )

        # 保存更新
        result = await self.db.update_node(updated_node)
        return {"node": result.to_dict()}

    async def delete(self, node_data: NodeDelete) -> Dict[str, str]:
        node = await self.db.find_node(
            node_data.label,
            **node_data.properties
        )

        if not node:
            raise NodeNotFoundError("Node not found")

        # 确保是BaseNode实例
        if not isinstance(node, BaseNode):
            node = self._create_node_instance(
                node_data.label,
                dict(node)
            )

        await self.db.delete_node(node)
        return {"message": "Node deleted successfully"}

    async def create_many(
            self,
            nodes: List[NodeBase]
    ) -> Dict[str, Any]:
        """批量创建节点"""
        try:
            created_nodes = []
            for node_data in nodes:
                node_instance = self._create_node_instance(
                    node_data.label,
                    node_data.properties
                )

                # 保存到数据库
                node = await self.db.create_node(node_instance)
                created_nodes.append(node)

            return {
                "nodes": [node.to_dict() for node in created_nodes],
                "count": len(created_nodes)
            }
        except Exception as e:
            logger.error(f"Error in create_many: {e}")
            raise

    async def update_many(
            self,
            updates: List[NodeUpdate]
    ) -> Dict[str, Any]:
        """批量更新节点"""
        try:
            updated_nodes = []
            for update in updates:
                conditions = {
                    "label": update.conditions.label,
                    "properties": update.conditions.properties
                }

                nodes = await self.db.update_node(
                    conditions,
                    update.new_properties
                )
                updated_nodes.extend(nodes)

            return {
                "nodes": [node.to_dict() for node in updated_nodes],
                "count": len(updated_nodes)
            }
        except Exception as e:
            logger.error(f"Error in update_many: {e}")
            raise

    async def delete_many(
            self,
            nodes: List[NodeBase]
    ) -> Dict[str, Any]:
        """批量删除节点"""
        try:
            total_deleted = 0
            for node in nodes:
                conditions = {
                    "label": node.label,
                    "properties": node.properties
                }

                deleted_count = await self.db.delete_node(conditions)
                total_deleted += deleted_count

            return {"count": total_deleted}
        except Exception as e:
            logger.error(f"Error in delete_many: {e}")
            raise

    async def get_all(
            self,
            batch_size: int,
            page: int
    ) -> Dict[str, Any]:
        skip = (page - 1) * batch_size
        nodes = await self.db.get_all_nodes(skip, batch_size)

        # 转换所有节点为BaseNode实例
        node_instances = []
        for node in nodes:
            if not isinstance(node, BaseNode):
                node_dict = dict(node)
                label = next(iter(node.labels))  # 获取第一个标签
                node_instance = self._create_node_instance(label, node_dict)
                node_instances.append(node_instance)
            else:
                node_instances.append(node)

        return {
            "nodes": [node.to_dict() for node in node_instances],
            "page": page,
            "batch_size": batch_size
        }

node_crud = NodeCRUD()