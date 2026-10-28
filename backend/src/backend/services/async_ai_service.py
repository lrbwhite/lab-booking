from openai import AsyncOpenAI
from backend.config import config
from backend.common.exceptions import BusinessException
from backend.models.user import User
from backend.schemas.aichat import ChatRequest
from backend.database import SessionLocal
from backend.services.ai_tools import TOOL_REGISTRY, TOOLS, TOOL_STATUS_TEXT
import json
from backend.services.prompt import build_system_prompt
import logging


logger = logging.getLogger(__name__)

def get_client():
    """获取OpenAI客户端"""
    if not config.LLM_API_KEY:
        raise BusinessException(code=400,msg="请配置LLM_API_KEY")
    return AsyncOpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
    )

def chat_stream(current_user: User,request: ChatRequest):
    """普通函数,执行校验。建client"""
    if not request.message:
        raise BusinessException(code=400,msg="对话历史为空")
    history=[]
    for msg in request.message:
        if msg.role == "system":
            continue
        if msg.role in("user","assistant") and msg.content.strip():
            history.append(msg.model_dump())
    if not history:
        raise BusinessException(code=400,msg="请输入对话内容")
    # 调用LLM客户端发送对话请求
    client = get_client()
    messages=[
                {"role":"system","content":build_system_prompt(current_user)},
                *history
            ]
    return _chat_generator(current_user,client,messages)

async def _chat_generator(current_user: User,client: AsyncOpenAI,messages: list):
    """工具循环，统一产出 {"type": "status"|"content", "content": str} 事件"""
    db=SessionLocal()
    try:
        # 第一轮模型请求前先吐一条状态，让响应尽快返回，避免前端长时间空白
        yield {"type": "status", "content": "正在思考…"}
        for _ in range(5):
            res=await client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                stream=True,
            )
            content_parts = []
            tool_calls = {}
            async for chunk in res:
                if not chunk.choices:
                    continue
                delta=chunk.choices[0].delta
                if delta.content:
                    content_parts.append(delta.content)
                    yield {"type": "content", "content": delta.content}
                for toolcall in delta.tool_calls or []:
                    idx=toolcall.index if toolcall.index is not None else 0
                    item=tool_calls.setdefault(
                        idx,
                        {"id": "", "type": "function",
                         "function": {"name": "", "arguments": ""}}
                         )
                    if toolcall.id:
                        item["id"]=toolcall.id
                    if toolcall.function:
                        if toolcall.function.name:
                            item["function"]["name"] += toolcall.function.name
                        if toolcall.function.arguments:
                            item["function"]["arguments"] += toolcall.function.arguments

            if not tool_calls:
                if not "".join(content_parts).strip():
                    yield {"type": "content", "content": "抱歉，我没有生成有效回答，请换个问法试试。"}
                return

            calls = [tool_calls[i] for i in sorted(tool_calls)]
            messages.append({
                "role": "assistant",
                "content": "".join(content_parts) or None,
                "tool_calls": calls,
            })

            for call in calls:
                name = call["function"]["name"]
                yield {"type": "status", "content": TOOL_STATUS_TEXT.get(name, "正在查询数据…")}
                try:
                    args=json.loads(call["function"]["arguments"] or "{}")
                    result=TOOL_REGISTRY[name](db,current_user,**args)
                except BusinessException as e:
                    result = {"error": e.msg}
                except json.JSONDecodeError:
                    result = {"error": "工具参数不是合法JSON"}
                except Exception as e:
                    logger.exception("调用工具失败: %s", e)
                    result = {"error": "工具执行失败"}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": json.dumps(result, ensure_ascii=False),
                })
            # 工具执行完到下一轮模型请求之间还有一段等待，给出整理答案的提示
            yield {"type": "status", "content": "正在整理答案…"}
        yield {"type": "content", "content": "抱歉，查询步骤过多，请换个问法。"}
    except Exception as e:
        logger.exception("调用LLM失败: %s", e)
        yield {"type": "content", "content": "抱歉，调用模型失败，请稍后再试。"}
    finally:
        db.close()