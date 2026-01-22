from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import Annotated, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import Raza, Mascota
from database import SessionLocal

router = APIRouter(
    prefix='/raza',
    tags=['Razas'],
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
class RazaBase(BaseModel):
    """Esquema base con los campos comunes para una raza."""
    especie: str = Field(min_length=2, description="Especie animal", json_schema_extra={"example": "Perro"})
    raza: str = Field(min_length=3, description="Raza de la especie", json_schema_extra={"example": "Puddle"})

class RazaRequest(RazaBase):
    """Esquema para la creación o actualización de razas."""
    pass

class RazaResponse(RazaBase):
    """Esquema de respuesta que incluye el ID generado por la base de datos."""
    id: int = Field(description="ID único de la raza en el sistema")

    class Config:
        from_attributes = True

class EspecieResponse(BaseModel):
    especie: str = Field(description="Especies registradas")

# --- Endpoints ---
@router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RazaResponse],
    summary="Obtener todas las razas",
    description="Retorna una lista completa de todas las razas registradas en la base de datos."
)
async def obtener_listado_completo_razas(db: db_dependency):
    return db.query(Raza).all()

@router.get(
    "/especie/{especie}/", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RazaResponse],
    summary="Obtener raza por especie",
    responses={404: {"description": "Raza no encontrada en el sistema"}}
)
async def obtener_raza_por_especie(
    db: db_dependency, 
    especie: str = Path(description="Nombre de la especie a filtrar", example="Perro")
):
    """
    Busca una raza específica una especia.
    """
    razas = db.query(Raza).filter(func.lower(Raza.especie) == especie.lower()).all()
    if not razas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se han encontrado razas para la especia buscada")
    return razas

@router.get(
    "/especies/",
    status_code=status.HTTP_200_OK,
    response_model=List[EspecieResponse],
    summary="Obtener listado de especies únicas"
)
async def obtener_listado_especies(db: db_dependency):
    """
    Retorna el listado de especies del sistema
    """
    return [{'especie': especie[0]} for especie in db.query(Raza.especie).distinct().all()]

@router.get(
    "/{id}/", 
    status_code=status.HTTP_200_OK, 
    response_model=RazaResponse,
    summary="Obtener raza por ID",
    responses={404: {"description": "Raza no encontrada en el sistema"}}
)
async def obtener_raza_por_id(
    db: db_dependency, 
    id: int = Path(gt=0, description="ID numérico de la raza a consultar", example=1)
):
    """
    Busca una raza específica mediante su identificador único.
    """
    raza = db.query(Raza).filter(Raza.id == id).first()
    if raza is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado la raza buscada")
    return raza

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva raza",
    description="Crea un nuevo registro de raza y lo persiste en la base de datos."
)
async def registrar_raza(db: db_dependency, raza_request: RazaRequest):
    raza = db.query(Raza).filter(func.lower(Raza.raza)==raza_request.raza.lower(), func.lower(Raza.especie)==raza_request.especie.lower()).first()
    if raza is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La raza {raza_request.raza} de la especie {raza_request.especie} ya se encuentra registrada")
    raza_model = Raza(**raza_request.model_dump())
    db.add(raza_model)
    db.commit()

@router.put(
    "/{id}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar raza",
    responses={404: {"description": "No se encontró la raza para actualizar"}}
)
async def actualizar_datos_raza(
    db: db_dependency, 
    raza_request: RazaRequest, 
    id: int = Path(gt=0, description="ID de la raza a modificar")
):
    """
    Actualiza íntegramente los datos de una raza existente.
    """
    raza = db.query(Raza).filter(func.lower(Raza.raza)==raza_request.raza.lower(), func.lower(Raza.especie)==raza_request.especie.lower()).first()
    if raza is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La raza {raza_request.raza} de la especie {raza_request.especie} ya se encuentra registrada")

    raza_model = db.query(Raza).filter(Raza.id == id).first()
    if raza_model is None:
        raise HTTPException(status_code=404, detail=f"No se ha encontrado la raza buscada con id {id}")
    
    for key, value in raza_request.model_dump().items():
        setattr(raza_model, key, value)

    db.add(raza_model)
    db.commit()

@router.delete(
    "/{id}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar raza",
    responses={404: {"description": "ID no válido o inexistente"}}
)
async def eliminar_raza(db: db_dependency, id: int = Path(gt=0, description="ID de la raza a eliminar")):
    """
    Elimina permanentemente una raza de la base de datos.
    """
    raza_query = db.query(Raza).filter(Raza.id == id)
    if raza_query.first() is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado la raza buscada")
    
    mascotas = db.query(Mascota).filter(Mascota.raza_id == id).first()
    if mascotas is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede eliminar la raza, porque tiene mascotas registradas")
    
    raza_query.delete()
    db.commit()

