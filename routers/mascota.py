from fastapi import APIRouter, Depends, HTTPException, Path, Body
from starlette import status
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import Mascota
from database import SessionLocal
from routers.raza import RazaResponse

router = APIRouter(
    prefix='/mascota',
    tags=['Mascotas'],
)

# --- Dependencias ---
def get_db():
    """Generador de sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# --- Modelos de Pydantic (Schemas) ---

class MascotaBase(BaseModel):
    """Esquema base con los campos comunes para una mascota."""
    nombre: str = Field(min_length=2, description="Nombre de la mascota", json_schema_extra={"example": "Firulais"})
    edad: int = Field(gt=0, description="Edad en años", json_schema_extra={"example": 3})
    raza_id: int = Field(ge=0, description="Id de la raza de la mascota", json_schema_extra={"example": 3})

class MascotaRequest(MascotaBase):
    """Esquema para la creación o actualización de mascotas."""
    pass

class MascotaResponse(MascotaBase):
    """Esquema de respuesta que incluye el ID generado por la base de datos."""
    id: int = Field(description="ID único de la mascota en el sistema")
    raza_obj: RazaResponse

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    response_model=List[MascotaResponse],
    summary="Obtener todas las mascotas",
    description="Retorna una lista completa de todas las mascotas registradas en la base de datos."
)
async def obtener_listado_completo_mascotas(db: db_dependency):
    return db.query(Mascota).all()

@router.get(
    "/{id}/", 
    status_code=status.HTTP_200_OK, 
    response_model=MascotaResponse,
    summary="Obtener mascota por ID",
    responses={404: {"description": "Mascota no encontrada en el sistema"}}
)
async def obtener_mascota_por_id(
    db: db_dependency, 
    id: int = Path(gt=0, description="ID numérico de la mascota a consultar", example=1)
):
    """
    Busca una mascota específica mediante su identificador único.
    """
    mascota = db.query(Mascota).filter(Mascota.id == id).first()
    if mascota is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado la mascota buscada")
    return mascota

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva mascota",
    description="Crea un nuevo registro de mascota y lo persiste en la base de datos."
)
async def registrar_mascota(db: db_dependency, mascota_request: MascotaRequest):
    mascota_model = Mascota(**mascota_request.model_dump())
    db.add(mascota_model)
    db.commit()

@router.put(
    "/{id}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar mascota",
    responses={404: {"description": "No se encontró la mascota para actualizar"}}
)
async def actualizar_datos_mascota(
    db: db_dependency, 
    mascota_request: MascotaRequest, 
    id: int = Path(gt=0, description="ID de la mascota a modificar")
):
    """
    Actualiza íntegramente los datos de una mascota existente.
    """
    mascota_model = db.query(Mascota).filter(Mascota.id == id).first()
    if mascota_model is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado la mascota buscada")
    
    for key, value in mascota_request.model_dump().items():
        setattr(mascota_model, key, value)

    db.add(mascota_model)
    db.commit()

@router.delete(
    "/{id}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mascota",
    responses={404: {"description": "ID no válido o inexistente"}}
)
async def eliminar_mascota(db: db_dependency, id: int = Path(gt=0, description="ID de la mascota a eliminar")):
    """
    Elimina permanentemente una mascota de la base de datos.
    """
    mascota_query = db.query(Mascota).filter(Mascota.id == id)
    if mascota_query.first() is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado la mascota buscada")
    
    mascota_query.delete()
    db.commit()