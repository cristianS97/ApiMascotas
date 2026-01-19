from fastapi import FastAPI
from database import engine
import models

# uvicorn main:app --reload
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def healthcheck():
    return {"Hello": "World"}
