# 智能实验室预约系统（Lab Booking）

基于 FastAPI + Vue 3 的实验室 / 设备预约管理系统，支持学生自助预约、管理员审核，并集成大模型 function calling 实现自然语言查询助手。

## 功能特性

| 模块 | 说明 | 学生 | 管理员 |
| --- | --- | :---: | :---: |
| 登录鉴权 | JWT 登录态，接口按角色做数据隔离 | ✅ | ✅ |
| 实验室列表 | 查看开放中的实验室、位置、开放时间 | ✅ | — |
| 实验室设备 | 查看实验室下的设备、型号、数量、状态 | ✅ | — |
| 我的预约 | 查看本人预约、按状态筛选、取消待审核预约 | ✅ | — |
| 预约申请 | 预约实验室或指定设备，提交后进入待审核 | ✅ | — |
| 实验室管理 | 实验室的增删改查与开放 / 关闭 | — | ✅ |
| 设备管理 | 设备的增删改查与维修状态维护 | — | ✅ |
| 预约审核 | 通过 / 拒绝待审核预约 | — | ✅ |
| 用户管理 | 用户增删改查 | — | ✅ |
| 个人中心 | 修改资料、头像上传、修改密码 | ✅ | ✅ |
| 智能助手 | 自然语言查询实验室、设备、本人预约 | ✅ | ✅ |

### 预约规则

预约提交时会依次校验：

1. 预约日期不得早于当天；当天预约的开始时间不得早于当前时间；结束时间不得早于开始时间；
2. 实验室必须存在且处于开放状态，预约时段必须落在实验室开放时间内；
3. 预约设备时，设备必须存在且不处于维修状态；
4. **时间冲突检测**：同一实验室（或同一台设备）在同一天内，与「待审核 / 已通过」的预约存在时段重叠时拒绝提交。

此外，应用启动时通过 `lifespan` 启动后台任务，每 60 秒扫描一次，将已过期的「待审核」预约自动置为「已取消」。

### 智能助手

- 基于 OpenAI 兼容接口（`AsyncOpenAI`），通过 function calling 提供 3 个只读工具：
  - `list_open_labs`：按关键字查询开放中的实验室；
  - `list_lab_equipments`：查询指定实验室的设备及状态；
  - `get_my_reservations`：查询**当前登录用户**的预约（支持按状态、日期 / 月份筛选）。
- 工具函数统一签名 `(db, current_user, **params)`，`user_id` 不作为模型可传参数暴露，身份只能由服务端注入，避免越权查询。
- 流式接口 `POST /api/ai/chat/stream` 以 SSE（`data: {...}\n\n`）推送两类事件：
  - `{"type": "status", "content": "..."}`：思考中 / 工具执行中的状态提示；
  - `{"type": "content", "content": "..."}`：增量文本。
  - 结束标记为 `data: [DONE]`。
- 支持多轮工具调用（上限 5 轮），工具结果会精简字段并限制条数（最多 10 条），避免上下文膨胀。
- system prompt 动态注入当前日期（中国标准时间）与用户角色，并包含越权与提示注入防护。
- 助手仅支持信息查询，不代用户创建或取消预约。

更多流式实现细节见 [docs/ai-streaming-design.md](docs/ai-streaming-design.md)。

## 技术栈

后端

| 依赖 | 用途 |
| --- | --- |
| FastAPI 0.115 | Web 框架，自动生成 OpenAPI 文档 |
| SQLAlchemy 2.0 | ORM，使用 `Mapped` 声明式模型 |
| MySQL + PyMySQL | 数据存储 |
| pydantic-settings | `.env` 配置加载 |
| PyJWT + bcrypt | Token 签发与密码哈希 |
| OpenAI SDK | 大模型调用（AsyncOpenAI 流式） |
| Uvicorn | ASGI 服务器 |
| uv | 依赖与虚拟环境管理 |

前端

| 依赖 | 用途 |
| --- | --- |
| Vue 3.5 | 组合式 API |
| Vue Router 5 | 路由与登录守卫 |
| Element Plus | UI 组件库 |
| Axios | 请求封装与拦截器 |
| Vite 8 | 开发服务器与构建 |

## 项目结构

```
lab-booking/
├── backend/
│   ├── src/backend/
│   │   ├── api/            # 路由层：参数接收、鉴权、调用 service
│   │   ├── services/       # 业务逻辑：校验、查询、AI 工具与流式生成
│   │   ├── models/         # SQLAlchemy 模型
│   │   ├── schemas/        # Pydantic 出入参
│   │   ├── dependencies/   # get_current_user / get_current_admin
│   │   ├── common/         # 统一响应体与全局异常处理
│   │   ├── utils/          # JWT、密码哈希
│   │   ├── config.py       # 配置与上传目录
│   │   ├── database.py     # 引擎、Session、Base
│   │   └── main.py         # 应用入口、中间件、异常注册、定时任务
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   └── src/
│       ├── api/            # 接口封装
│       ├── views/          # 页面
│       ├── layouts/        # 后台布局与菜单权限
│       ├── router/         # 路由与登录守卫
│       └── utils/          # axios 拦截器、token 存取
├── docs/
│   └── ai-streaming-design.md
└── README.md
```

## 快速开始

### 环境要求

- Python 3.14+（见 `backend/pyproject.toml`）
- [uv](https://docs.astral.sh/uv/)
- Node.js `^22.18.0` 或 `>=24.12.0`
- MySQL 8.x

### 1. 创建数据库

```sql
CREATE DATABASE lab_booking DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

数据表由 `main.py` 中的 `Base.metadata.create_all()` 在启动时自动创建，无需手动建表。

### 2. 配置后端环境变量

在 `backend/` 下复制 `.env.example` 为 `.env` 并填写：

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `DB_HOST` / `DB_PORT` | MySQL 地址与端口 | `127.0.0.1` / `3306` |
| `DB_USER` / `DB_PASSWORD` | 数据库账号 | `root` / `your_password` |
| `DB_NAME` | 数据库名 | `lab_booking` |
| `JWT_SECRET_KEY` | 签发密钥，务必修改 | 随机长字符串 |
| `JWT_EXPIRE_TIME` | Token 有效期，**单位为小时（整数）** | `24` |
| `JWT_ALGORITHM` | 签名算法 | `HS256` |
| `LLM_API_KEY` | 大模型 API Key | `sk-xxx` |
| `LLM_BASE_URL` | OpenAI 兼容接口地址 | `https://api.deepseek.com/v1` |
| `LLM_MODEL` | 模型名 | `deepseek-chat` |

> 注意：`JWT_EXPIRE_TIME` 在代码中按整数小时使用，请填 `24` 而不是 `24h`，否则配置解析会失败。

### 3. 启动后端

```bash
cd backend
uv sync
uv run uvicorn backend.main:app --reload --port 8000
```

- 接口文档：http://127.0.0.1:8000/docs
- 静态资源（上传文件）：http://127.0.0.1:8000/uploads/...

### 4. 初始化管理员账号

系统没有开放注册，首个管理员需要直接写入数据库。密码必须是 bcrypt 哈希，先生成：

```bash
cd backend
uv run python -c "from backend.utils.password import hash_password; print(hash_password('admin123'))"
```

再执行（把 `<hash>` 替换为上一步输出）：

```sql
INSERT INTO user (username, password, role, name, email, phone, avatar)
VALUES ('admin', '<hash>', 'admin', '管理员', 'admin@example.com', NULL, NULL);
```

之后的用户可通过「用户管理」页面由管理员创建。

### 5. 启动前端

```bash
cd frontend
npm install
npm run dev
```

打开 http://localhost:5173，使用刚才创建的管理员账号登录。

Vite 已将 `/api` 与 `/uploads` 代理到 `http://127.0.0.1:8000`（见 `frontend/vite.config.js`），因此无需额外配置跨域。

## API 概览

所有接口统一前缀 `/api`，除登录外均需请求头 `Authorization: Bearer <token>`。

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/api/auth/login` | 登录并获取 token | 公开 |
| GET | `/api/user/me` | 当前用户信息 | 登录 |
| PUT | `/api/user/me` | 修改个人资料 | 登录 |
| PUT | `/api/user/password` | 修改密码 | 登录 |
| GET | `/api/user/list` | 用户分页列表 | 登录 |
| POST / PUT / DELETE | `/api/user`、`/api/user/{id}` | 用户增改删 | 管理员 |
| GET | `/api/lab/list` | 实验室分页列表（支持关键字、状态筛选） | 登录 |
| GET | `/api/lab/{lab_id}` | 实验室详情 | 登录 |
| POST / DELETE | `/api/lab`、`/api/lab/{lab_id}` | 实验室增删 | 管理员 |
| PUT | `/api/lab/{lab_id}` | 修改实验室 | 登录 |
| GET | `/api/equipment/list` | 设备分页列表（支持关键字、实验室筛选） | 登录 |
| POST / PUT / DELETE | `/api/equipment`、`/api/equipment/{id}` | 设备增改删 | 管理员 |
| GET | `/api/reservation/list` | 预约列表（管理员看全部，学生仅看本人） | 登录 |
| POST | `/api/reservation` | 创建预约 | 登录 |
| PUT | `/api/reservation/{id}/cancel` | 取消本人待审核预约 | 登录 |
| PUT | `/api/reservation/{id}/audit` | 审核预约（通过 / 拒绝） | 管理员 |
| POST | `/api/files/upload` | 文件上传 | 公开 |
| POST | `/api/ai/chat` | 智能助手（非流式） | 登录 |
| POST | `/api/ai/chat/stream` | 智能助手（SSE 流式） | 登录 |

### 响应结构

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

业务异常通过 `BusinessException(code, msg)` 抛出，由全局异常处理器统一转换；参数校验错误、HTTP 异常与未知异常分别有独立处理器兜底，避免以裸 500 返回。

## 数据模型

| 表 | 说明 | 关键字段 |
| --- | --- | --- |
| `user` | 用户 | `username`、`password`（bcrypt）、`role`（student / admin）、`name`、`email`、`phone`、`avatar` |
| `labs` | 实验室 | `name`、`description`、`location`、`capacity`、`open_time`、`close_time`、`status`（1 开放 / 0 关闭） |
| `equipments` | 实验室设备 | `lab_id`、`name`、`spec`、`quantity`、`img`、`status`（1 正常 / 0 维修） |
| `reservations` | 预约 | `user_id`、`lab_id`、`equipment_id`、`date`、`start_time`、`end_time`、`remark`、`status`（0 待审核 / 1 已通过 / 2 已拒绝 / 3 已取消） |

`equipment_id` 为空表示预约整个实验室，不为空表示预约该实验室下的具体设备。

## 已知限制

- 预约冲突检测采用「先查询再插入」，未加锁也未设唯一约束，高并发下仍可能出现同一时段被重复预约；
- 建表依赖 `create_all()`，尚未引入 Alembic 迁移；
- CORS 当前允许所有来源，生产环境需收敛为白名单；
- 文件上传接口未强制登录，生产环境应加上鉴权与频率限制；
- 暂无自动化测试。

## 许可证

[MIT](LICENSE)
