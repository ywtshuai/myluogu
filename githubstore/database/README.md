# Neo4j FastAPI Project

一个使用 FastAPI 和 Neo4j 构建的 RESTful API 服务。

## 目录结构

```
your_project/
│
├── alembic/              # 数据库迁移相关
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 应用程序入口
│   │
│   ├── api/             # API 路由
│   │   ├── __init__.py
│   │   ├── v1/         # API 版本
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── nodes.py       # 节点相关接口
│   │   │   │   ├── relationships.py # 关系相关接口
│   │   │   │   └── utils.py
│   │   │   └── router.py
│   │   └── deps.py     # 依赖项
│   │
│   ├── core/           # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py   # 配置类
│   │   ├── security.py # 安全相关
│   │   └── events.py   # 事件处理
│   │
│   ├── db/             # 数据库相关
│   │   ├── __init__.py
│   │   ├── neo4j.py    # Neo4j 连接和基本操作
│   │   └── cache.py    # 缓存实现
│   │
│   ├── models/         # 数据模型
│   │   ├── __init__.py
│   │   ├── node.py     # 节点模型
│   │   └── relationship.py # 关系模型
│   │
│   ├── schemas/        # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── node.py     # 节点验证模型
│   │   └── relationship.py # 关系验证模型
│   │
│   ├── crud/          # CRUD 操作
│   │   ├── __init__.py
│   │   ├── node.py    # 节点 CRUD
│   │   └── relationship.py # 关系 CRUD
│   │
│   ├── utils/         # 工具函数
│   │   ├── __init__.py
│   │   ├── cache.py   # 缓存工具
│   │
│   └── middleware/    # 中间件
│       ├── __init__.py
│       └── logging.py # 日志中间件
│
├── tests/            # 测试文件
│   ├── __init__.py
│
├── logs/            # 日志文件
│
├── .env            # 环境变量
├── .gitignore
├── requirements.txt
└── README.md
```

## 代码规范

1. 命名规范
   - 类名使用 PascalCase
   - 函数和变量使用 snake_case
   - 常量使用大写 SNAKE_CASE

2. 文档规范
   - 所有公共接口必须有文档字符串
   - 使用类型注解
   - 复杂逻辑需要添加注释

3. 错误处理
   - 使用自定义异常类
   - 统一的错误响应格式
   - 适当的日志记录



## API 文档

启动服务后，访问以下地址查看 API 文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
```