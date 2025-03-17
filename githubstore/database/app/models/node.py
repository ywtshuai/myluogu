from py2neo.ogm import GraphObject, Property, Label
from typing import Set, Dict, Any
from datetime import datetime

class BaseNode(GraphObject):
    """
    基础节点模型
    """
    __primarykey__ = "id"  # 主键属性

    # 基本属性
    id = Property()
    created_at = Property()
    updated_at = Property()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 使用 __labels__ 替代 labels set
        if not hasattr(self, '__labels__'):
            self.__labels__ = set()

    @property
    def labels(self) -> Set[str]:
        """获取节点标签"""
        return self.__labels__

    def add_label(self, label: str):
        """添加标签"""
        if not hasattr(self, '__labels__'):
            self.__labels__ = set()
        self.__labels__.add(label)
        # 确保标签在py2neo中正确设置
        if hasattr(self, '_GraphObject__node'):
            self.__node__.add_label(label)

    def remove_label(self, label: str):
        """移除标签"""
        if hasattr(self, '__labels__'):
            self.__labels__.discard(label)
            # 确保标签在py2neo中正确移除
            if hasattr(self, '_GraphObject__node'):
                self.__node__.remove_label(label)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        properties = {}
        # 获取所有属性
        for key, value in self.__dict__.items():
            if hasattr(self, key) & (not key.startswith('_')):
                properties[key] = getattr(self, key)

        return {
            "id": self.id,
            "labels": list(self.labels),
            "properties": properties,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_node(cls, node):
        """从py2neo节点创建实例"""
        instance = cls()
        # 设置标签
        instance.__labels__ = set(node.labels)
        # 设置属性
        for key, value in dict(node).items():
            setattr(instance, key, value)
        return instance