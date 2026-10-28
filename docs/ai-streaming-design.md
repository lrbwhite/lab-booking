# AI 流式输出设计说明

本文说明实验室预约系统智能助手的流式输出实现：为什么这样分层、协议为什么这样定义、工具调用阶段为什么会有“空白期”，以及前端为什么必须用响应式对象接收增量。

相关文件：

- 后端路由：[backend/src/backend/api/ai.py](../backend/src/backend/api/ai.py)
- 流式生成器：[backend/src/backend/services/async_ai_service.py](../backend/src/backend/services/async_ai_service.py)
- 工具定义与状态文案：[backend/src/backend/services/ai_tools.py](../backend/src/backend/services/ai_tools.py)
- 前端请求封装：[frontend/src/api/ai.js](../frontend/src/api/ai.js)
- 前端对话页面：[frontend/src/views/AIChat.vue](../frontend/src/views/AIChat.vue)

---

## 一、完整链路

```
浏览器 fetch(POST)
   └─> FastAPI 路由 /ai/chat/stream
         └─> async 生成器（工具循环）
               ├─> AsyncOpenAI 流式请求（第 1 轮）
               ├─> 有 tool_calls → 执行工具 → 回填消息 → 第 2 轮
               └─> 每个增量 yield 事件
         └─> StreamingResponse 把事件拼成 SSE 帧
   └─> 前端 ReadableStream 逐块解码 → 解析事件 → 写入 reactive 气泡
```

## 二、分层职责

这条链上每一层只负责一件事，越界就会出 bug：

| 层 | 职责 | 不该做的事 |
| --- | --- | --- |
| 传输层（SSE） | 把“连续事件”变成字节流 | 不关心内容是正文还是状态 |
| 协议层（事件对象） | 定义事件语义 | 不关心模型是谁 |
| 生成层（生成器） | 编排模型与工具 | 不直接拼 HTTP 响应 |
| 渲染层（Vue） | 把事件映射成界面 | 不解析网络细节 |

## 三、为什么用 SSE

对话流是**单向、一次请求、有限时长**的：客户端说一句，服务端连回一串。这正好是 SSE 的形状。

- **WebSocket**：双向全双工，需要额外维护连接生命周期、心跳、重连、鉴权握手，能力过剩。
- **轮询**：要么慢，要么空转浪费请求。
- **SSE**：基于普通 HTTP POST，复用现有 `Authorization` 头、现有异常处理、现有代理；响应结束即连接结束，不用管理长连接。

代价是 SSE 只能服务端→客户端，但对话本来就不需要客户端在流中途再发数据（要“停止生成”，用 `AbortController` 断 HTTP 即可）。

**用最简单的通道满足需求，是这套设计的第一原则。**

## 四、协议设计：统一事件对象

早期实现每个事件都是裸文本：

```
data: {"content":"实验"}
data: {"content":"室"}
```

前端默认“收到就是答案”。这带来一个硬约束：**只要模型没吐正文，前端就无事可做**，而工具调用阶段恰恰不产生正文。

现在协议统一为：

```
{"type":"status","content":"正在思考…"}         ← 瞬时状态，可覆盖
{"type":"status","content":"正在查询实验室设备…"} ← 瞬时状态，可覆盖
{"type":"content","content":"实验室有 3 个"}     ← 累积正文，只追加
{"type":"content","content":"，分别是…"}         ← 累积正文，只追加
data: [DONE]                                     ← 流结束
```

三个设计取舍：

1. **status 与 content 共用 `content` 字段，只靠 `type` 区分。**
   前端解析结构不变，不必为不同事件写两套解析器；后端也不必准备两套序列化逻辑。
2. **status 绝不写进 content。**
   `content` 会被当作 assistant 历史回传给模型，混入“正在查询…”会污染上下文，模型可能模仿这种话术。
3. **前端给 `type` 设默认值 `'content'`。**
   协议演进时，旧格式或漏字段的分支自动退化为“纯正文”，不会白屏。兼容性兜底放在消费端，而不是要求生产端永远正确。

## 五、为什么先吐状态，再请求模型

生成器启动后第一件事就是：

```python
yield {"type": "status", "content": "正在思考…"}
```

它放在第一个 `await` 之前，这是有意的顺序设计：

- **让响应头和第一块 body 立刻发出。** 用户点击后不到 1 秒就能看到反馈，而不是等模型 TTFT（通常数秒）。
- **唤醒中间层。** 浏览器、反向代理、Vite 代理在大块数据到来前可能攒着不发，先发一个小包能触发立即 flush。
- **把不可优化的等待变成可见的等待。** 模型首 token 的物理延迟删不掉，但“用户不知道系统在干嘛”可以删掉。

同理，工具执行前发查询提示、执行完发“正在整理答案…”，是把时间轴上每段黑箱都标上标签。这些 status 是**覆盖式**的：多个工具连续执行时，前端只显示最新一条，不会堆成一串提示语。

## 六、工具循环设计

```python
async def _chat_generator(current_user, client, messages):
    db = SessionLocal()
    try:
        yield {"type": "status", "content": "正在思考…"}
        for _ in range(5):
            res = await client.chat.completions.create(..., stream=True)
            # 1. 累积 content 与 tool_calls 分片
            # 2. 无 tool_calls → 结束
            # 3. 有 tool_calls → 执行工具、回填 tool 消息、进入下一轮
    finally:
        db.close()
```

关键点与原因：

- **`AsyncOpenAI` + `stream=True`**：同步客户端会阻塞事件循环，一个用户流式输出时其他请求全部卡住。
- **生成器自己开 DB session**：路由层 `Depends(get_db)` 的 session 生命周期与会话内流式生成器不一致，复用会触发 `DetachedInstanceError`。
- **tool_calls 按 `index` 累积碎片**：流式返回的 `tool_calls` 是残缺拼接的，直接当完整对象使用会丢 id 或参数，下一轮请求直接 400。
- **必须回填 `role="tool"` + `tool_call_id`**：这是 OpenAI 协议要求的“一问一答”配对，缺了模型无法把结果和调用对上。
- **最多 5 轮**：工具循环本质是“模型自己决定还要不要查”，没有上限就可能无限调用、请求永不结束。到上限给降级文案，保证系统有界。
- **工具结果精简并限制条数**：结果全部进入下一轮上下文，冗余数据既烧 token 又拖慢首字时间。

## 七、错误处理：请求期错误与流内错误

校验逻辑放在普通函数 `chat_stream()` 里，而不是生成器里：

```python
def chat_stream(current_user, request):
    # 校验 message、过滤 system 消息
    client = get_client()
    return _chat_generator(current_user, client, messages)  # 返回生成器
```

原因是 **HTTP 状态码只能在响应头发出前决定**。一旦 `StreamingResponse` 开始返回字节，状态码已固化为 200；此时再抛 `BusinessException` 只会变成“流里混进一段报错文本”，前端收到 200 + 奇怪内容。

所以设计纪律是：

- **“能不能开始”属于请求期** → 抛异常，返回 4xx。
- **“过程中出错”属于流内事件** → 捕获后转成 `{"type":"content","content":"抱歉…"}`，保持连接正常结束。

## 八、前端渲染设计

前端有两个独立的正确性要求。

### 1. 对象身份：必须用 `reactive`

```js
const reply = reactive({ role: 'assistant', content: '', status: '' })
messages.value.push(reply)
```

`messages = ref([])` 里的数组是 Proxy。`push` 时存入的是**原始对象**，模板读取时 Vue 才把它惰性包成 Proxy。如果回调里修改的是局部变量 `reply`（原始对象），就绕过了 Proxy 的 `set` 拦截器：

```
模板渲染：messages.value[i].content → 走 Proxy get → 收集依赖 ✅
回调写入：raw.content += chunk      → 无拦截器      → 不触发渲染 ❌
```

结果是流式期间一次都不重渲染，直到 `loading` 变化才把全文一次性画出来。

**结论：`ref`/`reactive` 只对经过 Proxy 的读写生效；对象一旦以原始引用被外部持有，改它等于改“影子”，界面不会更新。**

### 2. 数据语义：追加 vs 覆盖

- `content` 是累积量 → `+=`
- `status` 是瞬态量 → 直接赋值覆盖
- 正文到达时清空 status，避免“提示语”和“答案”同时出现

模板用优先级表达式：

```vue
{{ item.content || item.status }}
```

有正文显示正文，没有正文显示状态。同一个气泡同时承载进度和结果，无需额外组件。

### 3. 历史消息只回填 role/content

```js
const history = messages.value
  .filter(item => item.role === 'user' || item.role === 'assistant')
  .map(item => ({ role: item.role, content: item.content }))
```

避免 `status` 字段被回传给后端。

## 九、状态机

```
提交 → status: 正在思考
     → 第 1 轮模型
         ├─ 有正文 → content 流 → 结束
         └─ 有 tool_calls → status: 正在查询X → 执行工具
              → status: 正在整理答案 → 下一轮模型 → …
     → 异常 → content: 抱歉…
     → [DONE] → 前端结束 loading
```

每一步都满足三个约束：**有反馈、有界（最多 5 轮）、失败可降级（转成正文而不是切断连接）**。

## 十、验证方法

直接用 curl 观察事件顺序（`-N` 关闭 curl 自身缓冲）：

```bash
curl -N -X POST http://127.0.0.1:8000/api/ai/chat/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"message":[{"role":"user","content":"有哪些开放中的实验室"}]}'
```

预期：`正在思考…` 立刻出现，随后是工具查询提示，最后是 content 事件。

也可以用假客户端直接驱动生成器，断言事件顺序：

```
{'type': 'status', 'content': '正在思考…'}
{'type': 'status', 'content': '正在查询你的预约记录…'}
{'type': 'status', 'content': '正在整理答案…'}
{'type': 'content', 'content': '你'}
{'type': 'content', 'content': '好'}
```

## 十一、尚未补上的稳健性缺口

架构已完整，以下是长期运行才会暴露的问题，属于收尾工作：

1. `AsyncOpenAI` 实例从不关闭 → httpx 连接池泄漏，应在 `finally` 中 `await client.close()`。
2. 客户端断开后上游请求仍在跑 → 白白消耗 token，应检查 `request.is_disconnected()` 并 `await res.close()`。
3. 工具结果的 `json.dumps` 位于 try 之外 → 序列化失败会截断整条回答。
4. 前端 SSE 解析假设 `data: ` 固定格式、`JSON.parse` 无保护。
5. 缺少 SSE 心跳注释行，超长工具调用可能被代理判为空闲断开。
6. 同步 DB 调用在 async 生成器中执行，会阻塞事件循环。
