# FastAPI 后端服务

这是一个使用 FastAPI 框架构建的后端服务，集成了 PostgreSQL 数据库。

## 已实现功能

*   **FastAPI 核心框架**：提供高性能的 API 接口。
*   **PostgreSQL 数据库集成**：使用 SQLAlchemy ORM 连接和操作 PostgreSQL 数据库。
*   **用户认证与授权**：
    *   用户注册 (`/register`)
    *   用户登录并生成 JWT Access Token (`/token`)
    *   通过 JWT Token 验证用户身份 (`/users/me/`)
*   **角色管理**：
    *   创建新角色 (`/roles/`)
    *   获取所有角色列表 (`/roles/`)
    *   按 ID 获取特定角色 (`/roles/{role_id}`)

## 数据库配置

数据库连接信息通过 `backend/.env` 文件中的 `DATABASE_URL` 环境变量配置。请确保您的 `.env` 文件包含正确的 PostgreSQL 连接字符串：

```
DATABASE_URL="postgresql://<your_username>:<your_password>@<your_host>:<your_port>/<your_database_name>"
```

**请注意：** `.env` 文件已被 `.gitignore` 忽略，请勿将其提交到版本控制中。

## 如何运行

本项目包含一个后端服务（基于 FastAPI）和一个前端应用（基于 Next.js）。请按照以下步骤启动：

### 1. 克隆仓库

首先，请克隆本项目的 Git 仓库到您的本地机器：

```bash
git clone <your-repository-url>
cd JAMESqiniuyun
```

### 2. 后端服务设置与运行

进入 `backend` 目录，安装依赖并启动后端服务。

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# 创建 .env 文件并配置 DATABASE_URL (参考上面的数据库配置说明)
uvicorn main:app --reload
```

后端服务默认运行在 `http://127.0.0.1:8000`。

### 3. 前端应用设置与运行

在一个新的终端窗口中，进入 `frontend` 目录，安装依赖并启动前端应用。

```bash
cd ../frontend
npm install
npm run dev
```

前端应用默认运行在 `http://localhost:3000`。

## 架构设计

### 模块规格与分工

本项目采用前后端分离的架构，主要分为以下两个模块：

1.  **后端服务 (backend/)**：
    *   **技术栈**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
    *   **职责**:
        *   提供 RESTful API 接口，处理客户端请求。
        *   用户认证与授权（JWT）。
        *   数据持久化与数据库交互。
        *   业务逻辑处理（例如，LLM 服务集成）。
        *   文件结构：
            *   `main.py`: FastAPI 应用的入口文件，路由定义。
            *   `app/auth.py`: 用户认证、JWT 生成和验证逻辑。
            *   `app/database.py`: 数据库连接、Session 管理。
            *   `app/models.py`: SQLAlchemy ORM 模型定义，与数据库表结构对应。
            *   `app/schemas.py`: Pydantic 模型定义，用于请求和响应数据验证与序列化。
            *   `app/llm_service.py`: 集成大型语言模型 (LLM) 服务的逻辑。

2.  **前端应用 (frontend/)**：
    *   **技术栈**: Next.js, React, TypeScript, Tailwind CSS
    *   **职责**:
        *   提供用户界面 (UI) 和用户体验 (UX)。
        *   通过 API 调用与后端服务进行数据交互。
        *   管理客户端状态和路由。
        *   用户注册、登录、仪表盘等页面展示。
        *   文件结构：
            *   `src/app/`: Next.js 页面和路由。
                *   `login/page.tsx`: 登录页面。
                *   `register/page.tsx`: 注册页面。
                *   `dashboard/page.tsx`: 用户仪表盘。
                *   `layout.tsx`: 整体布局。
                *   `globals.css`: 全局样式。
            *   `src/context/AuthContext.tsx`: 用户认证上下文管理。
            *   `src/api.ts`: 前后端 API 调用封装。

### 数据流

*   **前端到后端**: 用户在前端应用中进行操作（例如，登录、注册），前端通过 `src/api.ts` 中的函数向后端 API 发送 HTTP 请求。请求数据通过 Pydantic 模型的验证。
*   **后端到数据库**: 后端服务接收到请求后，根据业务逻辑通过 SQLAlchemy ORM 与 PostgreSQL 数据库进行交互，进行数据的增、删、改、查。
*   **数据库到后端**: 数据库返回数据给后端服务。
*   **后端到前端**: 后端服务处理完数据后，将结果（通常是 JSON 格式）通过 API 响应返回给前端，前端根据响应更新 UI。

### 认证流程

1.  用户在前端 `login/page.tsx` 提交用户名和密码。
2.  前端调用 `src/api.ts` 中的登录 API (`/token`)。
3.  后端 `main.py` 接收请求，调用 `app/auth.py` 进行用户验证。
4.  如果验证成功，`app/auth.py` 生成 JWT Access Token 并返回给前端。
5.  前端将 JWT Token 存储在本地（例如，localStorage 或 Context），并在后续请求中将其作为 `Authorization` 头发送给后端。
6.  后端在接收到带有 JWT Token 的请求时，使用 `app/auth.py` 验证 Token 的有效性，从而实现用户认证和授权。
