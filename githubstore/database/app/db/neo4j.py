from time import timezone

from py2neo import Graph, Node, Relationship
from typing import Dict, Any, Optional, List, Union
from app.core.config import settings
from app.core.exceptions import DatabaseError
from app.models.node import BaseNode
from app.models.relationship import BaseRelationship
import logging
from datetime import datetime


logger = logging.getLogger(__name__)
class Neo4jDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        try:
            self.graph = Graph(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            logger.info("Connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise DatabaseError(f"Database connection failed: {str(e)}")

    async def create_node(self, node: BaseNode) -> BaseNode:
        """创建节点"""
        try:
            # 确保有创建时间和更新时间
            if not node.created_at:
                node.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not node.updated_at:
                node.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 创建py2neo节点
            properties = {
                k: v for k, v in node.__dict__.items()
                if not k.startswith('_') and k != '__labels__'
            }

            properties['created_at'] = node.created_at
            properties['updated_at'] = node.updated_at
            py2neo_node = Node(*node.labels, **properties)
            self.graph.create(py2neo_node)

            # 更新node的id（如果需要）
            if not node.id:
                node.id = str(py2neo_node.identity)

            return node
        except Exception as e:
            logger.error(f"Failed to create node: {e}")
            raise DatabaseError(f"Failed to create node: {str(e)}")

    
    async def find_node(
            self,
            label: str,
            properties: Dict[str, Any]
    ) -> List[BaseNode]:
        """
        查找节点

        参数:
            - label: 节点标签
            - properties: 属性查询条件，值的类型会被保留
        """
        try:
            # 构建Cypher查询
            query = f"MATCH (n:{label})"
            where_clauses = []
            id = None
            for key, value in properties.items():
                where_clauses.append(f"n.{key} = ${key}")
                if key == 'id':
                    id = value

            if id is not None:
                query += " WHERE ID(n) = $id"
            elif where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            query += " RETURN ID(n) as id, n.created_at as created_at, "
            query += "n.updated_at as updated_at, labels(n) as labels, properties(n) as props"
            # Debug log
            logger.debug(f"Executing query: {query} with params: {properties}")

            results = self.graph.run(query, **properties)

            nodes = []
            for record in results:
                base_node = BaseNode()
                base_node.id = str(record['id'])
                base_node.__labels__ = set(record['labels'])
                base_node.created_at = record['created_at']
                base_node.updated_at = record['updated_at']

                # 设置所有属性
                for key, value in record['props'].items():
                    if key not in ['created_at', 'updated_at']:
                        setattr(base_node, key, value)

                nodes.append(base_node)

            return nodes
        except Exception as e:
            logger.error(f"Failed to find node: {e}")
            raise DatabaseError(f"Failed to find node: {str(e)}")

    async def update_node(
            self,
            conditions: Dict[str, Any],  # 包含label和properties的字典
            new_properties: Dict[str, Any]
    ) -> List[BaseNode]:
        """更新节点"""
        try:
            # 更新时间戳
            new_properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 构建查询条件
            label = conditions['label']
            properties = conditions['properties']

            where_clauses = []
            params = {}
            for key, value in properties.items():
                where_clauses.append(f"n.{key} = ${key}")
                params[key] = value

            # 使用 += 操作符来合并属性
            query = f"""
                   MATCH (n:{label})
                   WHERE {' AND '.join(where_clauses)}
                   SET n += $new_properties
                   RETURN 
                       ID(n) as id,
                       n.created_at as created_at,
                       n.updated_at as updated_at,
                       labels(n) as labels,
                       properties(n) as props
                   """

            logging.debug(f"Executing query: {query}")
            logging.debug(f"Query parameters: {params}")
            logging.debug(f"New properties: {new_properties}")

            results = self.graph.run(
                query,
                **params,
                new_properties=new_properties
            )

            updated_nodes = []
            for record in results:
                base_node = BaseNode()
                base_node.id = str(record['id'])
                base_node.__labels__ = set(record['labels'])
                base_node.created_at = record['created_at']
                base_node.updated_at = record['updated_at']

                # 设置所有属性
                for key, value in record['props'].items():
                    if key not in ['created_at', 'updated_at']:
                        setattr(base_node, key, value)

                updated_nodes.append(base_node)

            return updated_nodes
        except Exception as e:
            logging.error(f"Failed to update node: {e}")
            raise DatabaseError(f"Failed to update node: {str(e)}")

    async def delete_node(
            self,
            conditions: Dict[str, Any]  # 包含label和properties的字典
    ) -> int:
        """删除节点"""
        try:
            label = conditions['label']
            properties = conditions['properties']

            # 构建WHERE子句
            where_clauses = []
            params = {}
            for key, value in properties.items():
                where_clauses.append(f"n.{key} = ${key}")
                params[key] = value

            where_clause = " AND ".join(where_clauses) if where_clauses else "true"

            # 先计数，后删除
            count_query = f"""
               MATCH (n:{label})
               WHERE {where_clause}
               RETURN count(n) as count
               """

            count = self.graph.run(count_query, **params).evaluate()

            # 执行删除
            delete_query = f"""
               MATCH (n:{label})
               WHERE {where_clause}
               DETACH DELETE n
               """

            self.graph.run(delete_query, **params)

            return count
        except Exception as e:
            logging.error(f"Failed to delete node: {e}")
            raise DatabaseError(f"Failed to delete node: {str(e)}")

    async def create_relationship(
            self,
            rel_type: str,
            start_node: Dict[str, Any],
            end_node: Dict[str, Any],
            properties: Dict[str, Any] = None
    ) -> BaseRelationship:
        """创建关系"""
        try:
            # 查找或创建起始节点
            start_node_obj = await self.find_node(
                start_node['label'],
                start_node['properties']
            )
            if not start_node_obj:
                raise DatabaseError("Start node not found")
            start = start_node_obj[0]  # 假设find_node返回列表

            # 查找或创建终止节点
            end_node_obj = await self.find_node(
                end_node['label'],
                end_node['properties']
            )
            if not end_node_obj:
                raise DatabaseError("End node not found")
            end = end_node_obj[0]  # 假设find_node返回列表

            # 准备关系属性
            rel_props = properties or {}
            rel_props['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rel_props['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 创建Cypher查询
            query = """
            MATCH (start), (end)
            WHERE ID(start) = $start_id AND ID(end) = $end_id
            CREATE (start)-[r:`{}`]->(end)
            SET r += $properties
            RETURN ID(r) as id, type(r) as type, r as relationship,
                   ID(start) as start_id, start as start_node,
                   ID(end) as end_id, end as end_node
            """.format(rel_type)

            # 执行查询
            result = self.graph.run(
                query,
                start_id=int(start.id),
                end_id=int(end.id),
                properties=rel_props
            )

            if result:
                # 创建BaseRelationship实例
                rel = BaseRelationship(
                    type=rel_type,
                    start_node=start,
                    end_node=end,
                    **dict(result['relationship'])
                )
                rel.id = str(result['id'])
                return rel
            raise DatabaseError("Failed to create relationship")

        except Exception as e:
            logging.error(f"Failed to create relationship: {e}")
            raise DatabaseError(f"Failed to create relationship: {str(e)}")

    async def find_relationship(
            self,
            rel_type: str,
            start_node: Dict[str, Any],
            end_node: Dict[str, Any],
            properties: Dict[str, Any] = None
    ) -> List[BaseRelationship]:
        """查找关系"""
        try:
            # 构建查询参数
            params = {
                **{f"start_{k}": v for k, v in start_node['properties'].items()},
                **{f"end_{k}": v for k, v in end_node['properties'].items()},
            }
            if properties:
                params.update({f"rel_{k}": v for k, v in properties.items()})

            # 构建属性匹配条件
            rel_conditions = []
            if properties:
                rel_conditions.extend(f"r.{k} = $rel_{k}" for k in properties)
            rel_where = " AND ".join(rel_conditions) if rel_conditions else "true"

            # 构建查询
            query = f"""
            MATCH (start:{start_node['label']})-[r:{rel_type}]->(end:{end_node['label']})
            WHERE {' AND '.join(f"start.{k} = $start_{k}" for k in start_node['properties'])}
            AND {' AND '.join(f"end.{k} = $end_{k}" for k in end_node['properties'])}
            AND {rel_where}
            RETURN ID(r) as id, type(r) as type, r as relationship,
                   ID(start) as start_id, start as start_node,
                   ID(end) as end_id, end as end_node
            """

            results = list(self.graph.run(query, **params))

            relationships = []
            for record in results:
                # 创建起始节点
                start = BaseNode()
                start.id = str(record['start_id'])
                start.__labels__ = set(record['start_node'].labels)
                for key, value in dict(record['start_node']).items():
                    setattr(start, key, value)

                # 创建终止节点
                end = BaseNode()
                end.id = str(record['end_id'])
                end.__labels__ = set(record['end_node'].labels)
                for key, value in dict(record['end_node']).items():
                    setattr(end, key, value)

                # 创建关系
                rel = BaseRelationship(
                    type=record['type'],
                    start_node=start,
                    end_node=end,
                    **dict(record['relationship'])
                )
                rel.id = str(record['id'])
                relationships.append(rel)

            return relationships

        except Exception as e:
            logging.error(f"Failed to find relationship: {e}")
            raise DatabaseError(f"Failed to find relationship: {str(e)}")

    async def update_relationship(
            self,
            conditions: Dict[str, Any],  # 包含type、start_node、end_node的字典
            new_properties: Dict[str, Any]
    ) -> List[BaseRelationship]:
        """更新关系"""
        try:
            # 更新时间戳
            new_properties['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 从条件中提取信息
            rel_type = conditions['type']
            start_node = conditions['start_node']
            end_node = conditions['end_node']

            # 构建查询参数
            params = {
                **{f"start_{k}": v for k, v in start_node['properties'].items()},
                **{f"end_{k}": v for k, v in end_node['properties'].items()},
                "new_props": new_properties
            }

            # 构建查询
            query = f"""
            MATCH (start:{start_node['label']})-[r:{rel_type}]->(end:{end_node['label']})
            WHERE {' AND '.join(f"start.{k} = $start_{k}" for k in start_node['properties'])}
            AND {' AND '.join(f"end.{k} = $end_{k}" for k in end_node['properties'])}
            SET r += $new_props
            RETURN ID(r) as id, type(r) as type, r as relationship,
                   ID(start) as start_id, start as start_node,
                   ID(end) as end_id, end as end_node
            """

            results = list(self.graph.run(query, **params))

            updated_rels = []
            for record in results:
                # 创建起始节点
                start = BaseNode()
                start.id = str(record['start_id'])
                start.__labels__ = set(record['start_node'].labels)
                for key, value in dict(record['start_node']).items():
                    setattr(start, key, value)

                # 创建终止节点
                end = BaseNode()
                end.id = str(record['end_id'])
                end.__labels__ = set(record['end_node'].labels)
                for key, value in dict(record['end_node']).items():
                    setattr(end, key, value)

                # 创建关系
                rel = BaseRelationship(
                    type=record['type'],
                    start_node=start,
                    end_node=end,
                    **dict(record['relationship'])
                )
                rel.id = str(record['id'])
                updated_rels.append(rel)

            return updated_rels

        except Exception as e:
            logging.error(f"Failed to update relationship: {e}")
            raise DatabaseError(f"Failed to update relationship: {str(e)}")

    async def delete_relationship(
            self,
            conditions: Dict[str, Any]  # 包含type、start_node、end_node的字典
    ) -> int:
        """删除关系"""
        try:
            # 从条件中提取信息
            rel_type = conditions['type']
            start_node = conditions['start_node']
            end_node = conditions['end_node']

            # 构建查询参数
            params = {
                **{f"start_{k}": v for k, v in start_node['properties'].items()},
                **{f"end_{k}": v for k, v in end_node['properties'].items()}
            }

            # 计数查询
            count_query = f"""
            MATCH (start:{start_node['label']})-[r:{rel_type}]->(end:{end_node['label']})
            WHERE {' AND '.join(f"start.{k} = $start_{k}" for k in start_node['properties'])}
            AND {' AND '.join(f"end.{k} = $end_{k}" for k in end_node['properties'])}
            RETURN count(r) as count
            """

            count = self.graph.run(count_query, **params).evaluate()

            if count > 0:
                # 删除查询
                delete_query = f"""
                MATCH (start:{start_node['label']})-[r:{rel_type}]->(end:{end_node['label']})
                WHERE {' AND '.join(f"start.{k} = $start_{k}" for k in start_node['properties'])}
                AND {' AND '.join(f"end.{k} = $end_{k}" for k in end_node['properties'])}
                DELETE r
                """

                self.graph.run(delete_query, **params)

            return count

        except Exception as e:
            logging.error(f"Failed to delete relationship: {e}")
            raise DatabaseError(f"Failed to delete relationship: {str(e)}")

    async def get_all_nodes(
            self,
            skip: int,
            limit: int
    ) -> List[BaseNode]:
        """获取所有节点"""
        try:
            query = f"MATCH (n) RETURN n SKIP {skip} LIMIT {limit}"
            results = self.graph.run(query)

            nodes = []
            for record in results:
                node = record['n']
                base_node = self._to_base_node(node)
                nodes.append(base_node)

            return nodes
        except Exception as e:
            logger.error(f"Failed to get all nodes: {e}")
            raise DatabaseError(f"Failed to get all nodes: {str(e)}")

    async def get_all_relationships(
            self,
            skip: int,
            limit: int
    ) -> List[BaseRelationship]:
        """获取所有关系"""
        try:
            query = f"MATCH ()-[r]->() RETURN r, startNode(r) as start, endNode(r) as end SKIP {skip} LIMIT {limit}"
            results = self.graph.run(query)

            relationships = []
            for record in results:
                rel = record['r']
                start_node = record['start']
                end_node = record['end']

                base_rel = BaseRelationship()
                base_rel.set_type(rel.type())
                base_rel.start_node = self._to_base_node(start_node)
                base_rel.end_node = self._to_base_node(end_node)

                for key, value in dict(rel).items():
                    setattr(base_rel, key, value)

                relationships.append(base_rel)

            return relationships
        except Exception as e:
            logger.error(f"Failed to get all relationships: {e}")
            raise DatabaseError(f"Failed to get all relationships: {str(e)}")

    async def execute_advanced_query(
            self,
            query_params: Dict[str, Any]
    ) -> List[BaseNode]:
        """
        执行高级节点查询
        返回符合条件的节点列表
        """
        try:
            # 构建高级查询
            query = self._build_advanced_query(query_params)
            results = self.graph.run(query, **query_params.get('parameters', {}))

            nodes = []
            for record in results:
                node = record['n']
                base_node = self._to_base_node(node)
                nodes.append(base_node)
            return nodes
        except Exception as e:
            logger.error(f"Failed to execute advanced query: {e}")
            raise DatabaseError(f"Failed to execute advanced query: {str(e)}")

    async def execute_advanced_relationship_query(
            self,
            query_params: Dict[str, Any]
    ) -> Union[BaseRelationship, List[BaseRelationship]]:
        """执行高级关系查询"""
        try:
            # 构建高级查询
            query = self._build_advanced_relationship_query(query_params)
            results = self.graph.run(query, **query_params.get('parameters', {}))

            if query_params.get('return_many', False):
                relationships = []
                for record in results:
                    rel = record['r']
                    start_node = record['start']
                    end_node = record['end']
                    base_rel = self._to_base_relationship(rel, start_node, end_node)
                    relationships.append(base_rel)
                return relationships
            else:
                record = results.evaluate()
                if record:
                    return self._to_base_relationship(
                        record['r'],
                        record['start'],
                        record['end']
                    )
                return None
        except Exception as e:
            logger.error(f"Failed to execute advanced relationship query: {e}")
            raise DatabaseError(f"Failed to execute advanced relationship query: {str(e)}")

    def _to_base_node(self, node: Node) -> BaseNode:
        """转换py2neo节点为BaseNode实例"""
        base_node = BaseNode()

        # 添加标签
        for label in node.labels:
            base_node.add_label(label)

        # 添加属性
        for key, value in dict(node).items():
            setattr(base_node, key, value)

        return base_node

    def _to_base_relationship(
            self,
            rel: Relationship,
            start_node: Node,
            end_node: Node
    ) -> BaseRelationship:
        """转换py2neo关系为BaseRelationship实例"""
        base_rel = BaseRelationship()
        base_rel.set_type(rel.type())
        base_rel.start_node = self._to_base_node(start_node)
        base_rel.end_node = self._to_base_node(end_node)

        for key, value in dict(rel).items():
            setattr(base_rel, key, value)

        return base_rel

    def _build_advanced_query(self, query_params: Dict[str, Any]) -> str:
        """构建高级节点查询"""
        # 基本匹配
        query = "MATCH (n"

        # 添加标签
        if 'labels' in query_params:
            query += ":" + ":".join(query_params['labels'])
        query += ")"

        # 添加WHERE子句
        where_clauses = []
        if 'properties' in query_params:
            for key, value in query_params['properties'].items():
                where_clauses.append(f"n.{key} = ${key}")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # 添加排序
        if 'order_by' in query_params:
            query += f" ORDER BY {query_params['order_by']}"

        # 返回结果
        query += " RETURN n"

        return query

    def _build_advanced_relationship_query(self, query_params: Dict[str, Any]) -> str:
        """构建高级关系查询"""
        # 基本匹配
        query = "MATCH (start)-[r"

        # 添加关系类型
        if 'type' in query_params:
            query += f":{query_params['type']}"
        query += "]->(end)"

        # 添加WHERE子句
        where_clauses = []
        if 'properties' in query_params:
            for key, value in query_params['properties'].items():
                where_clauses.append(f"r.{key} = ${key}")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # 添加排序
        if 'order_by' in query_params:
            query += f" ORDER BY {query_params['order_by']}"

        # 返回结果
        query += " RETURN r, start, end"

        return query

    async def find_or_create_node(self, node: BaseNode) -> Node:
        """查找节点，如果不存在则创建"""
        try:
            existing_node = await self.find_node(
                next(iter(node.labels)),
                {k: v for k, v in node.__dict__.items() if not k.startswith('_')}
            )

            if existing_node is None:
                return await self.create_node(node)
            return existing_node
        except Exception as e:
            logger.error(f"Failed to find or create node: {e}")
            raise DatabaseError(f"Failed to find or create node: {str(e)}")

def get_db() -> Neo4jDB:
    """获取数据库实例"""
    return Neo4jDB()