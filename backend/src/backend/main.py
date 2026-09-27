from fastapi import FastAPI
from backend.api import router as api_router


from backend.models.user import User
from backend.database import engine,Base

Base.metadata.create_all(bind=engine) 

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}