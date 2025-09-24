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

## 如何运行 (待补充)

此部分将在未来提供详细的运行说明。
