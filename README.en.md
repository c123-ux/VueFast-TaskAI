# VueFast-TaskAI

> Personal Task Management + AI Chat Assistant | Vue 3 + FastAPI + GLM-4-Flash

Author: [c123-ux](https://github.com/c123-ux)

A full-stack personal task management application built with **Vue 3 + TypeScript + FastAPI + SQLite**, integrated with the **Zhipu GLM-4-Flash** model as an AI chat assistant. Supports task CRUD, category management, multi-condition filtering, and customizable AI chat with role/personality/region settings.

## Features

### 📋 Task Management
- Full CRUD operations for tasks
- Priority levels (High / Medium / Low)
- Status tracking (To Do / In Progress / Done)
- Category tags (many-to-many relationships)
- Due date support
- Multi-condition filtering (status / priority / category)

### 🤖 AI Chat Assistant
- Intelligent conversations powered by Zhipu GLM-4-Flash
- Multi-conversation management (create / select / delete)
- Batch conversation deletion with multi-select
- Customizable AI character, personality, and region
- Quick presets (Xiaomei / Xiaoshuai / Xiaozhi / Xiaomeng)
- Real-time message display with streaming UX
- Enter to send / Shift+Enter for new line
- Stop AI generation anytime

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue 3 + TypeScript |
| **Build Tool** | Vite 5 |
| **UI Library** | Element Plus |
| **State Management** | Pinia |
| **HTTP Client** | Axios |
| **Backend** | FastAPI (Python) |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | SQLite |
| **Validation** | Pydantic 2 |
| **AI Model** | Zhipu GLM-4-Flash |
| **Async HTTP** | httpx (Zhipu API calls) |

## Project Structure

```
VueFast-TaskAI/
├── backend/                    # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── database.py        # Database configuration
│   │   ├── config.py          # Configuration
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── task.py        # Task & Category models
│   │   │   └── chat.py        # Conversation & Message models
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── task.py
│   │   │   └── chat.py
│   │   └── routers/           # API routes
│   │       ├── tasks.py       # Task CRUD
│   │       ├── categories.py  # Category management
│   │       └── chat.py        # Chat endpoints
│   ├── .env                   # Environment variables (API Key)
│   ├── requirements.txt
│   ├── run.py                 # Startup script
│   └── todo.db                # SQLite database file
│
├── frontend/                   # Frontend (Vue 3)
│   ├── src/
│   │   ├── api/               # API wrappers
│   │   │   └── chat.ts
│   │   ├── components/        # Shared components
│   │   │   ├── TaskForm.vue   # Task form dialog
│   │   │   └── CategoryDialog.vue  # Category manager dialog
│   │   ├── views/
│   │   │   ├── Home.vue       # Task management page
│   │   │   └── Chat.vue       # AI chat page
│   │   ├── stores/            # Pinia stores
│   │   │   └── chat.ts
│   │   ├── router/index.ts    # Router config
│   │   ├── main.ts            # Entry point
│   │   └── App.vue            # Root component
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts         # Vite config (with API proxy)
│
├── start.ps1                   # One-click startup script (Windows)
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Zhipu API Key ([Apply here](https://open.bigmodel.cn/))

### 1. Configure Backend

```bash
cd backend

# (Optional) Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API Key (edit .env file)
# Replace ZHIPUAI_API_KEY=your_api_key_here with your actual key
```

### 2. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Backend runs at http://localhost:8000

API Docs (Swagger UI): http://localhost:8000/docs

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### 4. One-Click Start (Windows)

```powershell
.\start.ps1
```

## API Endpoints

### Task Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List tasks (with filtering) |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/{id}` | Get task details |
| PUT | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |

### Category Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/categories` | List categories |
| POST | `/api/categories` | Create a category |
| DELETE | `/api/categories/{id}` | Delete a category |

### AI Chat

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/conversations` | List conversations |
| POST | `/api/conversations` | Create a new conversation |
| GET | `/api/conversations/{id}` | Get conversation details (with AI settings) |
| PATCH | `/api/conversations/{id}` | Update conversation (AI role/personality/region) |
| DELETE | `/api/conversations/{id}` | Delete a conversation |
| POST | `/api/conversations/{id}/messages` | Send a message |
| GET | `/api/conversations/{id}/messages` | Get message history |
| POST | `/api/conversations/{id}/stop` | Stop AI generation |

## Usage

### Task Management
1. Click "New Task" to create a task with title, description, priority, due date, and categories
2. Click "Edit" on a task to modify it, or use the status dropdown for quick status switching
3. Use the filter bar to filter tasks by status, priority, or category
4. Click "Category Manager" to create or delete category tags

### AI Chat
1. Click "New Conversation" to start a fresh chat
2. Check the box next to conversations to batch select and delete
3. Type your message in the input box — Enter to send, Shift+Enter for a new line
4. Configure the AI's name, personality, and region in the sidebar settings panel
5. Use preset roles to quickly switch between different AI personalities

## Author

- **GitHub**: [c123-ux](https://github.com/c123-ux)

## License

MIT
