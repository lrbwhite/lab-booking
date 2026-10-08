import logging

from fastapi import Request,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.common.response import Response

logger = logging.getLogger(__name__)

class BusinessException(HTTPException):
    """
    业务异常
    """
    def __init__(self,code: int,msg: str):
        super().__init__(status_code=code,detail=msg)
        self.code = code
        self.msg = msg

async def handle_business_exception(request: Request,exc: BusinessException):
    """
    处理自定义业务异常
    """
    return JSONResponse(content=Response.error(code=exc.code,msg=exc.msg).model_dump(),
    status_code=exc.status_code)

async def handle_http_exception(request: Request,exc: HTTPException):
    """
    处理 HTTP 异常
    """
    return JSONResponse(content=Response.error(code=exc.status_code,msg=exc.detail).model_dump(),
    status_code=exc.status_code,headers=exc.headers)

async def handle_validation_exception(request: Request,exc: RequestValidationError):
    """
    处理验证异常
    """
    msg = ";".join(
        f"{'.'.join(str(item) for item in error['loc'])}: {error['msg']}"
        for error in exc.errors()
    )
    return JSONResponse(content=Response.error(code=422,msg=msg).model_dump(),
    status_code=422)

async def handle_global_exception(request: Request,exc: Exception):
    """
    处理全局异常
    """
    logger.error("%s %s 未处理异常",request.method,request.url.path,exc_info=exc)
    return JSONResponse(content=Response.error(code=500,msg="internal server error").model_dump(),
    status_code=500)