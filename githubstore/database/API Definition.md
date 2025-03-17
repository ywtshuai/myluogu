# Neo4j RESTful API 接口文档

## 基础信息
- 基础URL: `http://localhost:8000/api/v1`
- 所有请求和响应均使用 JSON 格式
- 时间格式: ISO 8601 (例如: "2023-12-20T10:00:00Z")
- 所有错误响应都将包含一个 `detail` 字段，说明错误原因

## 节点操作 (Nodes)

### 1. 查找节点
查找符合条件的节点列表。

- **URL**: `/nodes`
- **Method**: `GET`
- **查询参数**: 
  - `q`: Base64编码的JSON查询条件
  
**查询条件JSON格式**:
```json
{
    "label": "Person",  // 必需，节点标签
    "properties": {     // 可选，查询条件
        "name": "John",
        "age": 30
    }
}
```

**成功响应** (200 OK):
```json
{
    "nodes": [
        {
            "id": "1",
            "labels": ["Person"],
            "properties": {
                "name": "John",
                "age": 30
            },
            "created_at": "2023-12-20T10:00:00Z",
            "updated_at": "2023-12-20T10:00:00Z"
        }
    ],
    "count": 1
}
```
### 2. 创建节点
- **URL**: `/nodes`
- **Method**: `POST`
- **Body**:
```json
{
    "label": "Person",
    "properties": {
        "name": "John",
        "age": 30,
        "email": "john@example.com"
    }
}
```
- **Response**:
```json
{
    "node": {
        "id": "1",
        "labels": ["Person"],
        "properties": {
            "name": "John",
            "age": 30,
            "email": "john@example.com"
        },
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
}
```

### 3. 批量创建节点

- **URL**: `/nodes/batch`
- **Method**: `POST`
- **请求体**:
```json
{
    "nodes": [
        {
            "label": "Person",
            "properties": {
                "name": "John",
                "age": 30
            }
        },
        {
            "label": "Person",
            "properties": {
                "name": "Jane",
                "age": 25
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "created": [
        {
            "id": "1",
            "labels": ["Person"],
            "properties": {
                "name": "John",
                "age": 30
            },
            "created_at": "2023-12-20T10:00:00Z",
            "updated_at": "2023-12-20T10:00:00Z"
        },
        // ... 其他创建的节点
    ],
    "count": 2
}
```

### 4.批量更新节点

- **URL**: `/nodes`
- **Method**: `PUT`
- **请求体**:
```json
{
    "updates": [
        {
            "conditions": {
                "label": "Person",
                "properties": {
                    "name": "John"
                }
            },
            "new_properties": {
                "age": 31
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "updated": [
        {
            "id": "1",
            "labels": ["Person"],
            "properties": {
                "name": "John",
                "age": 31
            },
            "created_at": null,
            "updated_at": "2023-12-20T10:00:00Z"
        }
    ],
    "count": 1
}
```

### 5. 批量删除节点

- **URL**: `/nodes`
- **Method**: `DELETE`
- **请求体**:
```json
{
    "nodes": [
        {
            "label": "Person",
            "properties": {
                "name": "John"
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "deleted": 1,
    "message": "Nodes deleted successfully"
}
```

## 关系操作 (Relationships)

### 1. 查找关系

- **URL**: `/relationships`
- **Method**: `GET`
- **查询参数**: 
  - `q`: Base64编码的JSON查询条件

**查询条件JSON格式**:
```json
{
    "type": "KNOWS",           // 必需，关系类型
    "start_node": {           // 必需，起始节点
        "label": "Person",
        "properties": {
            "name": "John"
        }
    },
    "end_node": {             // 必需，终止节点
        "label": "Person",
        "properties": {
            "name": "Jane"
        }
    },
    "properties": {           // 可选，关系属性
        "since": "2023"
    }
}
```

**成功响应** (200 OK):
```json
{
    "relationships": [
        {
            "type": "KNOWS",
            "start_node": {
                "id": "1",
                "labels": ["Person"],
                "properties": {
                    "name": "John"
                }
            },
            "end_node": {
                "id": "2",
                "labels": ["Person"],
                "properties": {
                    "name": "Jane"
                }
            },
            "properties": {
                "since": "2023",
                "created_at": "2023-12-20T10:00:00Z",
                "updated_at": "2023-12-20T10:00:00Z"
            }
        }
    ],
    "count": 1
}
```

### 2. 创建关系
- **URL**:  `/relationships/`
- **Method**: `POST`
- **Body**:
```json
{
    "type": "KNOWS",
    "start_node": {
        "label": "Person",
        "properties": {
            "name": "John"
        }
    },
    "end_node": {
        "label": "Person",
        "properties": {
            "name": "Jane"
        }
    },
    "properties": {
        "since": "2023"
    }
}
```
- **Response**:
```json
{
    "relationship": {
        "type": "KNOWS",
        "start_node": {
            "label": "Person",
            "properties": {
                "name": "John"
            }
        },
        "end_node": {
            "label": "Person",
            "properties": {
                "name": "Jane"
            }
        },
        "properties": {
            "since": "2023",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    }
}
```

### 3. 批量创建关系

- **URL**: `/relationships/batch`
- **Method**: `POST`
- **请求体**:
```json
{
    "relationships": [
        {
            "type": "KNOWS",
            "start_node": {
                "label": "Person",
                "properties": {
                    "name": "John"
                }
            },
            "end_node": {
                "label": "Person",
                "properties": {
                    "name": "Jane"
                }
            },
            "properties": {
                "since": "2023"
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "created": [
        // 创建的关系列表
    ],
    "count": 1
}
```

### 4. 批量更新关系

- **URL**: `/relationships`
- **Method**: `PUT`
- **请求体**:
```json
{
    "updates": [
        {
            "conditions": {
                "type": "KNOWS",
                "start_node": {
                    "label": "Person",
                    "properties": {"name": "John"}
                },
                "end_node": {
                    "label": "Person",
                    "properties": {"name": "Jane"}
                }
            },
            "new_properties": {
                "since": "2024"
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "updated": [
        // 更新的关系列表
    ],
    "count": 1
}
```

### 5. 批量删除关系

- **URL**: `/relationships`
- **Method**: `DELETE`
- **请求体**:
```json
{
    "relationships": [
        {
            "type": "KNOWS",
            "start_node": {
                "label": "Person",
                "properties": {"name": "John"}
            },
            "end_node": {
                "label": "Person",
                "properties": {"name": "Jane"}
            }
        }
    ]
}
```

**成功响应** (200 OK):
```json
{
    "deleted": 1,
    "message": "Relationships deleted successfully"
}
```

## 错误响应

### 常见错误代码
- 400 Bad Request: 请求格式错误
- 404 Not Found: 未找到请求的资源
- 500 Internal Server Error: 服务器内部错误

**错误响应示例**:
```json
{
    "detail": "Error message here"
}
```

## 注意事项

1. Base64 编码/解码示例:
```python
# 编码
import base64
import json

query = {
    "label": "Person",
    "properties": {"name": "John"}
}
encoded = base64.b64encode(json.dumps(query).encode()).decode()

# 解码
decoded = json.loads(base64.b64decode(encoded).decode())
```

2. 所有批量操作都应注意数据量的控制，建议单次请求不超过1000条记录。

3. 时间戳字段 (`created_at`, `updated_at`) 由服务器自动维护，不需要客户端提供。

4. 查询条件中的属性值类型需要与数据库中的类型匹配（例如：数字类型不要使用字符串）。

5. 所有请求都需要处理可能的错误响应。

## 联系方式

如有问题请联系：wsz12358_plai(stewartwei)

---

文档版本：1.0.0
最后更新：2025.3.12