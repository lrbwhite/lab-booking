from sqlalchemy.orm import Session

from backend.models.reservation import Reservation
from backend.models.user import User
from backend.services import equipment_services, lab_services

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_open_labs",
            "description": "查询当前开放中的实验室列表，返回 id、名称、位置、开放时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "实验室的名称关键字，可以为空",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_lab_equipments",
            "description": "查询指定实验室下的设备及状态，lab_id 可先从 list_open_labs 的结果获取",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab_id": {
                        "type": "integer",
                        "description": "实验室 ID",
                    },
                    "keywords": {
                        "type": "string",
                        "description": "设备名称的关键字，可以为空",
                    },
                },
                "required": ["lab_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_my_reservations",
            "description": "查询当前登录用户本人的预约列表，返回 id、实验室名称、设备名称、预约日期、时段、状态。用户没有指定筛选条件时不要传参数，直接查询全部",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "enum": [0, 1, 2, 3],
                        "description": "预约状态：0-待审核，1-已通过，2-已拒绝，3-已取消，可以为空",
                    },
                    "date": {
                        "type": "string",
                        "description": "预约日期，格式 YYYY-MM-DD；也可只传 YYYY-MM 查询某个月的预约，可以为空",
                    },
                },
            },
        },
    },
]

# 单次工具查询最多返回的条数，避免把过多数据塞进模型上下文
MAX_TOOL_RESULTS = 10


def list_open_labs(db: Session, current_user: User, keywords: str | None = None):
    """查询当前开放中的实验室，返回精简字段"""
    page = lab_services.get_lab_page_list(
        db, 1, MAX_TOOL_RESULTS, keywords or None, status=1
    )
    labs = [
        {
            "id": lab.id,
            "name": lab.name,
            "location": lab.location,
            "capacity": lab.capacity,
            "open_time": lab.open_time,
            "close_time": lab.close_time,
            "description": lab.description,
        }
        for lab in page.list
    ]
    result = {"total": page.total, "labs": labs}
    if page.total > len(labs):
        result["note"] = f"共 {page.total} 个，仅展示前 {len(labs)} 个，可用 keywords 缩小范围"
    return result


def list_lab_equipments(
    db: Session, current_user: User, lab_id: int, keywords: str | None = None
):
    """查询指定实验室下的设备，返回精简字段"""
    lab_services.get_lab(db, lab_id)  # 实验室不存在时抛出 404
    page = equipment_services.get_equipment_page_list(
        db, 1, MAX_TOOL_RESULTS, keywords or None, lab_id
    )
    equipments = [
        {
            "id": item.id,
            "name": item.name,
            "spec": item.spec,
            "quantity": item.quantity,
            "status": "正常" if item.status == 1 else "维修",
            "description": item.description,
        }
        for item in page.list
    ]
    result = {"lab_id": lab_id, "total": page.total, "equipments": equipments}
    if page.total > len(equipments):
        result["note"] = f"共 {page.total} 台，仅展示前 {len(equipments)} 台，可用 keywords 缩小范围"
    return result


RESERVATION_STATUS_TEXT = {0: "待审核", 1: "已通过", 2: "已拒绝", 3: "已取消"}


def get_my_reservations(
    db: Session, current_user: User, status: int | None = None, date: str | None = None
):
    """查询当前用户本人的预约，返回精简字段"""
    query = db.query(Reservation).filter(Reservation.user_id == current_user.id)
    if status is not None:
        query = query.filter(Reservation.status == status)
    if date:
        query = query.filter(Reservation.date.like(f"{date.strip()}%"))
    total = query.count()
    items = (
        query.order_by(Reservation.date.desc(), Reservation.start_time.desc())
        .limit(MAX_TOOL_RESULTS)
        .all()
    )
    reservations = [
        {
            "id": item.id,
            "type": "设备" if item.equipment_id else "实验室",
            "lab_name": item.lab.name if item.lab else None,
            "equipment_name": item.equipment.name if item.equipment else None,
            "date": item.date,
            "start_time": item.start_time,
            "end_time": item.end_time,
            "status": RESERVATION_STATUS_TEXT.get(item.status, "未知"),
            "remark": item.remark,
        }
        for item in items
    ]
    result = {"total": total, "reservations": reservations}
    if total > len(reservations):
        result["note"] = (
            f"共 {total} 条，仅展示最近 {len(reservations)} 条，可用 status 或 date 缩小范围"
        )
    return result


TOOL_REGISTRY = {
    "list_open_labs": list_open_labs,
    "list_lab_equipments": list_lab_equipments,
    "get_my_reservations": get_my_reservations,
}

# 工具执行期间返回给前端的提示文案，避免工具调用阶段界面空白
TOOL_STATUS_TEXT = {
    "list_open_labs": "正在查询开放中的实验室…",
    "list_lab_equipments": "正在查询实验室设备…",
    "get_my_reservations": "正在查询你的预约记录…",
}