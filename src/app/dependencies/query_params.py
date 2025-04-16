import json
from typing import Optional

from app.core.database.config import get_db
from app.models.query_params import SortDirection, UserQueryParams
from app.services.user_service import UserService
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session


async def get_user_query_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sortBy: Optional[str] = Query(None),
    sortDirection: SortDirection = Query(SortDirection.ascending),
    match: Optional[str] = Query(
        None, description='Filtros en formato JSON {"campo":"valor"}'
    ),
) -> UserQueryParams:
    match_dict = {}
    if match:
        try:
            match_dict = json.loads(match)
            if not isinstance(match_dict, dict):
                raise ValueError(
                    "El parámetro 'match' debe ser un diccionario JSON"
                )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Parámetro 'match' no es un JSON válido",
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    return UserQueryParams(
        page=page,
        limit=limit,
        sortBy=sortBy,
        sortDirection=sortDirection,
        match=match_dict or {},
    )


async def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService.from_config(db=db)
