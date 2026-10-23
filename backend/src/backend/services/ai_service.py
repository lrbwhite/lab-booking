import logging

from backend.config import config
from backend.common.exceptions import BusinessException
from openai import OpenAI
from backend.schemas.aichat import ChatRequest
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.services.ai_tools import TOOL_REGISTRY, TOOLS
import json
from backend.services.prompt import build_system_prompt



logger = logging.getLogger(__name__)



def get_client():
    """获取OpenAI客户端"""
    if not config.LLM_API_KEY:
        raise BusinessException(code=400,msg="请配置LLM_API_KEY")
    return OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
    )

def chat(db: Session,current_user: User,request: ChatRequest):
    """LLM对话"""
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
    try:
        for _ in range(5):
            res= client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )
            msg=res.choices[0].message
            if not msg.tool_calls:
                if not (msg.content or "").strip():
                    raise BusinessException(code=400,msg="LLM返回空内容")
                return msg.content

            messages.append(msg)
            for call in msg.tool_calls:
                try:
                    args=json.loads(call.function.arguments or "{}")
                    result=TOOL_REGISTRY[call.function.name](db,current_user,**args)
                except BusinessException as e:
                    result={"error": e.msg}
                except Exception as e:
                    logger.exception("调用工具失败:%s",e)
                    result={"error":"工具执行失败"}
                messages.append({
                    "role":"tool",
                    "tool_call_id":call.id,
                    "content":json.dumps(result,ensure_ascii=False)
                })
                    
        return "抱歉，查询步骤过多，请换个问法。"

    except BusinessException:
        raise
    except Exception as e:
        logger.exception("调用LLM失败: %s", e)
        raise BusinessException(code=500, msg="调用LLM失败")

