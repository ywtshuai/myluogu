
# AW 项目代码管理规范

## 项目背景
> TODO 

## Git仓库管理规范

### 1. 分支管理规范
#### 1.1 分支类型与命名规则
| 分支类型    | 命名规范                                                 | 生命周期      | 合并方向     |
| ------- | ---------------------------------------------------- | --------- | -------- |
| master  | 生产环境唯一基准分支                                           | 永久保留      | 仅接受MR合并  |
| release | 无物理分支，通过tag标记                                        | 永久保留      | N/A      |
| 个人开发分支  | dev-成员ID（例: dev-yirui）                               | 永久保留      | → master |
| 功能开发分支  | feat-具体功能名称（例: feat-parallelization_of_agent_output） | 功能开发完毕后删除 | → master |

#### 1.2 分支管理细则
1. **个人分支规范**
   ```bash
   # 创建规范（基于最新master）
   git checkout -b dev/yirui master
   
   # 同步策略（每日首次开发前）
   git pull --rebase origin master
   ```
   
2. **分支保护规则**
   - master分支强制master权限审查
   - 禁止force push到所有分支

### 2. 提交规范
#### 2.1 Commit Message规范
```text
<type>(<scope>): <brief description>  # 英文标题
```

**通用示例**：
```bash
git commit -m "feat: implement modular processing"
```

#### 2.2 提交质量要求
1. **原子性提交**
   - 单个提交只完成一个逻辑变更
   - 禁止包含无关文件的修改（如同时修改代码+配置）
2. **代码控制**
   - 代码尽量低耦合高聚合，做好模块化管理
   - 每个文件行数控制在1000行以内

### 3. 合并规范
#### 3.1 MR模板规范
```markdown
## Change Summary
[完整描述融合内容]

## Quality Checklist
• [ ] 更新对应文档
• [ ] 完成代码自审
• [ ] 无已知安全风险

## Review Notes
[评审重点说明，如复杂算法说明等]
```

#### 3.2 MR命名规范
| 变更类型    | MR命名格式             | 示例                  |
| ------- | ------------------ | ------------------- |
| 新功能     | feat: 简要描述新功能      | feat: 添加agent并行模块      |
| 缺陷修复    | fix: 简要描述修复内容      | fix: 修复API报错问题     |
| 代码优化    | refactor: 简要描述优化内容 | refactor: 优化函数名与目录结构 |
| 文档更新    | docs: 简要描述文档变更     | docs: 更新API接口文档     |
| 测试相关    | test: 简要描述测试变更     | test: 添加快速批量测试模块    |
| 构建/依赖变更 | chore: 简要描述变更内容    | chore: 更新库依赖版本     |

#### 3.3 评审流程
1. **Reviewer分配矩阵**

| 变更类型   | 必须评审人           | 可选评审人  |
| ------ | --------------- | ------ |
| 核心模块变更 | 技术负责人 + 模块Owner | 随机2名开发 |
| 普通功能变更 | 模块Owner         | 随机1名开发 |
| 紧急修复   | 技术负责人           | 随机1名开发 |

2. **评审响应**
对修改完成的内容勾选resolved

### 4. 代码规范
#### 4.1 通用规范
1. **基础要求**
   - 新功能必须包含接口文档

#### 4.2 语言专项规范
**Python**
1.类型提示规范
- 必须包含google风格的docstring
```python
# 类型提示规范
def calculate_sum(a: int, b: int) -> int:
    """计算两个整数的和，并返回结果。

    函数会验证输入是否为整数，若类型错误则抛出异常。

    Args:
        a (int): 第一个加数。
        b (int): 第二个加数。

    Returns:
        int: 两个整数的和。

    Raises:
        TypeError: 如果 `a` 或 `b` 不是整数。

    Examples:
        >>> calculate_sum(3, 5)
        8
        >>> calculate_sum(-1, 10)
        9
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("参数必须为整数")
    return a + b
```

**C++**
```cpp
# TODO
```

**Bash**
```bash
# TODO
```

## 附则
1. **规范执行**
   - TODO

2. **版本记录**

   | 版本号   | 修订日期    | 修订内容摘要         |
   |----------|------------|---------------------|
   | v1.0.0   | 2025-03-05 | 首次发布完整规范体系 |

---
```