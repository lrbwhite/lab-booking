from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: T | None = None

    @classmethod
    def success(cls, data: Any = None) -> "Response":
        return cls(code=200, msg="success", data=data)

    @classmethod
    def error(cls, code: int, msg: str) -> "Response":
        return cls(code=code, msg=msg)

class PageResponse(BaseModel):
    """分页返回结果"""
    list: Any=[]
    total: int=0
