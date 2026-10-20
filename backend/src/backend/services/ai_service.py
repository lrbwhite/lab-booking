from backend.config import config
from backend.common.exceptions import BusinessException
from openai import OpenAI

SYSTEM_PROMPT = """你是智能实验室预约系统的助手，回答要简洁。
你可以介绍本系统的预约流程：
1. 登录后打开实验室列表，选择实验室或设备
2. 填写日期和时段并提交，状态为待审核
3. 管理员审核通过后即可使用
4. 待审核、已通过的预约，本人可以取消
你目前查不到真实的实验室、设备、预约数据。
如果用户问某个实验室几点开门、有没有某台设备，请说明去「实验室列表」查看，不要编造具体数据。
如果用户问了跟实验室无关的问题，可以直接拒绝回答。
"""

def get_client():
    """获取OpenAI客户端"""
    if not config.LLM_API_KEY:
        raise BusinessException(code=400,msg="请请配置LLM_API_KEY")
    return OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
    )

def chat(request: ChatRequest):
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
    try:
        res= client.chat.completions.create(
                model=Config.LLM_MODEL,
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                *history
            ]
        )
        message=res.choices[0].message.content
        if not message or not message.strip():
            raise BusinessException(code=400,msg="LLM返回空内容")
        return message
    except Exception as e:
        raise BusinessException(code=400,msg="请调用LLM失败")

