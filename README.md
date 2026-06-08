# VueFast-TaskAI

> 个人任务计划管理 + AI 聊天助手 | Vue 3 + FastAPI

作者：[c123-ux](https://github.com/c123-ux)

基于 **Vue 3 + TypeScript + FastAPI + SQLite** 的全栈个人任务管理应用，集成 AI 大模型作为智能聊天助手，支持任务 CRUD、分类管理、多条件筛选，以及带有角色/性格/地区自定义的智能对话。

## 功能特性

### 📋 任务管理
- 任务的增删改查
- 优先级设置（高/中/低）
- 状态管理（待办/进行中/已完成）
- 分类标签管理（多对多关联）
- 截止日期设置
- 多条件筛选（状态/优先级/分类）

### 🤖 AI 聊天助手
- 基于大语言模型的智能对话
- 多对话管理（创建/选择/删除）
- 批量选择删除对话
- 支持 AI 角色、性格、地区自定义
- 预设角色快速切换（小美/小帅/小智/小萌）
- 实时消息展示，流式输入体验
- Enter 发送 / Shift+Enter 换行
- 随时停止 AI 生成

## 技术栈

| 层级 | 技术 |
|------|------|
| **前端框架** | Vue 3 + TypeScript |
| **构建工具** | Vite 5 |
| **UI 组件库** | Element Plus |
| **状态管理** | Pinia |
| **HTTP 客户端** | Axios |
| **后端框架** | FastAPI (Python) |
| **ORM** | SQLAlchemy 2.0 |
| **数据库** | SQLite |
| **数据验证** | Pydantic 2 |
| **AI 模型** | 大语言模型 |
| **HTTP 客户端** | httpx |

## 项目结构

```
VueFast-TaskAI/
├── backend/                    # 后端（FastAPI）
│   ├── app/
│   │   ├── main.py            # FastAPI 入口
│   │   ├── database.py        # 数据库配置
│   │   ├── config.py          # 配置文件
│   │   ├── models/            # SQLAlchemy 模型
│   │   │   ├── task.py        # 任务 & 分类模型
│   │   │   └── chat.py        # 聊天 & 消息模型
│   │   ├── schemas/           # Pydantic 数据模型
│   │   │   ├── task.py
│   │   │   └── chat.py
│   │   └── routers/           # API 路由
│   │       ├── tasks.py       # 任务 CRUD
│   │       ├── categories.py  # 分类管理
│   │       └── chat.py        # 聊天相关
│   ├── .env                   # 环境变量（含 API Key）
│   ├── requirements.txt
│   ├── run.py                 # 启动脚本
│   └── todo.db                # SQLite 数据库文件
│
├── frontend/                   # 前端（Vue 3）
│   ├── src/
│   │   ├── api/               # API 接口封装
│   │   │   └── chat.ts
│   │   ├── components/        # 公共组件
│   │   │   ├── TaskForm.vue   # 任务表单弹窗
│   │   │   └── CategoryDialog.vue  # 分类管理弹窗
│   │   ├── views/
│   │   │   ├── Home.vue       # 任务管理主页
│   │   │   └── Chat.vue       # AI 聊天页面
│   │   ├── stores/            # Pinia 状态管理
│   │   │   └── chat.ts
│   │   ├── router/index.ts    # 路由配置
│   │   ├── main.ts            # 入口
│   │   └── App.vue            # 根组件
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts         # Vite 配置（含 API 代理）
│
├── start.ps1                   # 一键启动脚本
└── README.md
```

## 快速开始

### 前置条件

- Python 3.9+
- Node.js 18+
- AI API Key

### 1. 配置后端

```bash
cd backend

# （可选）创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置 API Key（编辑 .env 文件）
# 将 API_KEY=your_api_key_here 替换为你的真实 Key
```

### 2. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

后端运行在 http://localhost:8000

API 文档（Swagger UI）: http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

### 4. 一键启动（Windows）

```powershell
.\start.ps1
```

## API 接口

### 任务管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks` | 获取任务列表（支持筛选） |
| POST | `/api/tasks` | 创建任务 |
| GET | `/api/tasks/{id}` | 获取任务详情 |
| PUT | `/api/tasks/{id}` | 更新任务 |
| DELETE | `/api/tasks/{id}` | 删除任务 |

### 分类管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 获取分类列表 |
| POST | `/api/categories` | 创建分类 |
| DELETE | `/api/categories/{id}` | 删除分类 |

### AI 聊天

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/conversations` | 获取对话列表 |
| POST | `/api/conversations` | 创建新对话 |
| GET | `/api/conversations/{id}` | 获取对话详情（含 AI 设置） |
| PATCH | `/api/conversations/{id}` | 更新对话（AI 角色/性格/地区） |
| DELETE | `/api/conversations/{id}` | 删除对话 |
| POST | `/api/conversations/{id}/messages` | 发送消息 |
| GET | `/api/conversations/{id}/messages` | 获取消息历史 |
| POST | `/api/conversations/{id}/stop` | 停止 AI 生成 |

## 使用说明

### 任务管理
1. 点击「新建任务」创建任务，设置标题、描述、优先级、截止日期和分类
2. 在列表中点击「编辑」修改任务，或通过状态下拉框快速切换状态
3. 使用筛选栏按状态/优先级/分类筛选任务
4. 点击「分类管理」创建或删除分类标签

### AI 聊天
1. 点击「新建对话」开始新对话
2. 勾选对话前的复选框可批量选择删除
3. 在底部输入框输入消息，Enter 发送，Shift+Enter 换行
4. 侧栏底部可设置 AI 角色的名字、性格和地区
5. 支持预设角色一键切换，打造专属 AI 助手

## 作者

- **GitHub**: [c123-ux](https://github.com/c123-ux)

## 许可证

MIT
