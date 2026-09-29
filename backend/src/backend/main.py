from fastapi import FastAPI,HTTPException
from fastapi.exceptions import RequestValidationError
from backend.api import router as api_router


from backend.models.user import User
from backend.database import engine,Base

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine) 

from backend.common.exceptions import (BusinessExceptionException,
handle_business_exception,
handle_http_exception,
handle_validation_exception,
handle_global_exception)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许所有来源
    allow_credentials=True, #允许携带cookie
    allow_methods=["*"], #允许所有方法
    allow_headers=["*"], #允许所有头
)
app.include_router(api_router)

#注册异常处理函数
app.add_exception_handler(BusinessExceptionException,handle_business_exception)
app.add_exception_handler(HTTPException,handle_http_exception)
app.add_exception_handler(RequestValidationError,handle_validation_exception)
# 注册全局异常处理函数
app.add_exception_handler(Exception,handle_global_exception)

@app.get("/")
def read_root():
    return {"Hello": "World"}