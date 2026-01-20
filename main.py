from fastapi import FastAPI
from database import engine
import models
from routers import mascota, raza

# uvicorn main:app --reload
app = FastAPI(
    title="Sistema de Gestión de Mascotas",
    description="API para la administración de registros de mascotas en una clínica veterinaria.",
    version="1.0.0",
    contact={
        "name": "Soporte Técnico",
        "email": "soporte@soporte.falso.com",
    },
    license_info={
        "name": "MIT",
    }
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def healthcheck():
    return {"Hello": "World"}

app.include_router(mascota.router)
app.include_router(raza.router)
