from pydantic import BaseModel

class ReservationCreateRequest(BaseModel):
    """创建预约请求参数"""
    lab_id: int
    equipment_id: int|None=None
    date: str
    start_time: str
    end_time: str
    remark: str | None=None
