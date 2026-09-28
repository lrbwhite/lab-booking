from typing import Any
from pydantic import BaseModel

class Response(BaseModel):
    code: int
    msg: str
    data: Any = None

    @classmethod
    def success(cls,data: Any = None) -> "Response":
        return cls(code=200,msg="success",data=data)
    @classmethod
    def error(cls,code: int,msg: str) -> "Response":
        return cls(code=code,msg=msg)
     