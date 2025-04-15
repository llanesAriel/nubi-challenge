from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models.query_params import UserQueryParams, SortDirection
from app.services.user_service import UserService
from app.database.config import get_db
from fastapi import Depends
import json


async def get_user_query_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sortBy: Optional[str] = Query(None),
    sortDirection: SortDirection = Query(SortDirection.ascending),
    match: Optional[str] = Query(None, description='Filtros en formato JSON {"campo":"valor"}')
) -> UserQueryParams:

    match_dict = {}
    if match:
        try:
            match_dict = json.loads(match)
            if not isinstance(match_dict, dict):
                raise ValueError("El parámetro 'match' debe ser un diccionario JSON")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Parámetro 'match' no es un JSON válido")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    return UserQueryParams(
        page=page,
        limit=limit,
        sortBy=sortBy,
        sortDirection=sortDirection,
        match=match_dict or {}
    )


async def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService.from_config(db=db)
