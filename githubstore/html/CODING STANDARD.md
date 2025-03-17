# Alicization World 前端代码规范

## 1. 文件结构规范

### 1.1 文件命名
- 组件文件夹使用 PascalCase: `AgentCard/index.tsx`，
- 按功能分类的文件夹使用 camelCase: `agentService.ts`
- 工具、hooks、服务等使用 camelCase: `agentService.ts`
- 样式文件使用 kebab-case: `agent-card.css`
- 类型定义文件使用 camelCase: `agentTypes.ts`

### 1.2 目录结构
- 每个组件建立独立文件夹，包含组件本身和相关文件
```
ComponentName/
├── index.tsx          # 主组件文件
├── styles.module.css  # 样式文件（如果需要）
├── types.ts           # 组件特需的类型（公共的请放在types文件夹里）
└── components/        # 子组件（如果需要）
```

## 2. 组件规范

### 2.1 组件声明
- 使用函数组件和 TypeScript
- 明确声明组件 Props 接口
```typescript
interface Props {
  name: string;
  onAction: (id: string) => void;
}

const MyComponent: React.FC<Props> = ({ name, onAction }) => {
  // ...
};
```

### 2.2 组件结构
```typescript
// 1. Imports
import React, { useState, useEffect } from 'react';
import type { ComponentProps } from './types';

// 2. Interfaces/Types (如果不在单独的types文件中)
interface LocalState {
  // ...
}

// 3. Component
const ComponentName: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // 3.1 Hooks
  const [state, setState] = useState<LocalState>();
  
  // 3.2 Effects
  useEffect(() => {
    // ...
  }, []);

  // 3.3 Handlers
  const handleAction = () => {
    // ...
  };

  // 3.4 Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
};

// 4. Export
export default ComponentName;
```

## 3. TypeScript 规范

### 3.1 类型定义
- 使用 interface 而不是 type（除非需要使用联合类型）
- 类型和接口名使用 PascalCase
```typescript
interface AgentState {
  id: string;
  status: 'idle' | 'busy';
}
```

### 3.2 类型导出
- 相关类型放在一个文件中
- 使用 export 导出所有类型
```typescript
// types/agent.ts
export interface Agent { ... }
export interface AgentAction { ... }
```

## 4. 样式规范

### 4.1 CSS 组织
- 使用 CSS Modules 或 styled-components
- 类名使用 kebab-case
- 避免内联样式（除非动态样式）
```typescript
import styles from './styles.module.css';

const Component = () => (
  <div className={styles['component-wrapper']}>
    ...
  </div>
);
```

## 5. 代码格式

### 5.1 基本格式
- 使用 2 空格缩进
- 大括号换行
- 每行最大长度 100 字符
- 文件末尾留一空行

### 5.2 命名规范
- 变量和函数使用 camelCase
- 常量使用 UPPER_SNAKE_CASE
- 组件使用 PascalCase
- 事件处理函数使用 handle 前缀
```typescript
const DEFAULT_TIMEOUT = 1000;
const handleClick = () => { ... };
```

## 6. 注释规范

### 6.1 文件头注释
```typescript
/**
 * @file ComponentName 组件
 * @description 组件的主要功能描述
 * @author 作者名
 */
```

### 6.2 函数注释
```typescript
/**
 * 函数描述
 * @param {string} param1 - 参数1描述
 * @param {number} param2 - 参数2描述
 * @returns {Promise<void>} 返回值描述
 */
```

## 7. 最佳实践

### 7.1 组件最佳实践
- 一个文件只包含一个组件
- 组件保持简单，复杂组件拆分为小组件
- Props 解构赋值
- 使用 memo 优化渲染性能

### 7.2 Hook 最佳实践
- 自定义 Hook 使用 use 前缀
- Hook 依赖项要完整
- 避免过深的 Hook 嵌套

### 7.3 状态管理
- 本地状态使用 useState
- 共享状态使用 Redux
- Action 和 Reducer 分文件管理

## 8. TODO 注释规范
```typescript
// TODO: 简短的待办描述
// TODO(开发者): 待办描述 - 预计完成时间
// FIXME: 需要修复的问题
```

## 9. Git 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式（不影响代码运行）
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

请所有开发者遵循这个规范，以保持代码的一致性和可维护性。后续可能会根据项目发展调整规范内容。