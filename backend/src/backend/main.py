from fastapi import FastAPI,HTTPException
from fastapi.exceptions import RequestValidationError
from backend.api import router as api_router
from fastapi.staticfiles import StaticFiles
from backend.config import UPLOAD_DIR

from backend.models.user import User
from backend.database import engine,Base

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine) 

from backend.common.exceptions import (BusinessException,
handle_business_exception,
handle_http_exception,
handle_validation_exception,
handle_global_exception)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许所有来源
    allow_credentials=False, #通配符来源下不能开启凭证，浏览器会拒绝
    allow_methods=["*"], #允许所有方法
    allow_headers=["*"], #允许所有头
)
app.include_router(api_router)

#注册异常处理函数
app.add_exception_handler(BusinessException,handle_business_exception)
app.add_exception_handler(HTTPException,handle_http_exception)
app.add_exception_handler(RequestValidationError,handle_validation_exception)
# 注册全局异常处理函数
app.add_exception_handler(Exception,handle_global_exception)

#挂载静态的文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR))


@app.get("/")
def read_root():
    return {"Hello": "World"}