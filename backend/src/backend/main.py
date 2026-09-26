from fastapi import FastAPI
from backend.api.auth import router as auth_router
from backend.models.user import User
from backend.database import engine,Base

Base.metadata.create_all(bind=engine) 

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}