# Alicization World 项目启动指南

## 环境要求

### Node.js 和 NPM 版本
- Node.js: v18.18.0 (LTS版本)
- NPM: v9.8.1

### 检查当前版本
```bash
node -v
npm -v
```

### 版本管理工具安装（如需要）
如果需要安装或更新Node.js，推荐使用nvm (Node Version Manager)：

Windows:
1. 下载并安装nvm-windows安装包
2. 运行以下命令：
```bash
nvm install 18.18.0
nvm use 18.18.0
```

Mac/Linux:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
# 重启终端后
nvm install 18.18.0
nvm use 18.18.0
```

更新npm（如需要）：
```bash
npm install -g npm@9.8.1
```

## 项目初始化

### 1. 安装依赖
```bash
cd ai-world/html

# 安装项目所需的其他依赖
npm install antd @ant-design/icons d3 neo4j-driver
```

### 2. 项目目前依赖版本
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "antd": "^5.11.0",
    "d3": "^7.8.5",
    "neo4j-driver": "^5.28.1",
    "@ant-design/icons": "^5.2.6",
    "redux": "暂未选择版本"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@types/d3": "^7.4.3",
    "@vitejs/plugin-react": "^4.0.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}


```

### 3. 运行项目
```bash
npm run dev
```

## 项目结构
```
src/
├── assets/                  # 页面资源，如图片等
├── components/              # 页面组件
├── core/                    # 项目核心代码，用来进行复杂算法
├── hooks/                   # React的钩子函数
├── pages/                   # 页面
├── services/                # 与后端/数据库的api通信
├── store/                   # 状态管理（Redux）
├── styles/                  # 全局样式（局部样式请定义在components里，规范详见CODING STANDARD）
├── types/                   # 通用类型定义
├── utils/                   # 功能性函数
└── App.tsx                  # 应用入口
```

## 注意事项
1. 确保所有依赖都已正确安装
2. 如遇到版本冲突，可以尝试删除 node_modules 目录并重新安装
3. 开发时请遵循项目的TypeScript类型定义
4. 项目使用Vite作为构建工具，支持热更新

## 常见问题解决
如果遇到启动问题，请检查：
1. Node.js和npm版本是否符合要求
2. 是否已安装所有必要依赖
3. 是否在正确的目录下运行命令
4. 端口是否被占用（默认使用5173端口）

## 技术文档
- [React文档](https://react.dev/)
- [Ant Design文档](https://ant.design/)
- [D3.js文档](https://d3js.org/)
- [TypeScript文档](https://www.typescriptlang.org/)
- [Vite文档](https://vitejs.dev/)

如需更多帮助，请联系项目维护人员。
