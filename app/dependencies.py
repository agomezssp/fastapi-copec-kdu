from functools import lru_cache
from typing import Optional

from fastapi import Header, HTTPException, Depends
from starlette import status

from .config import Settings
from .domain.logics.user_repository import UserRepository
from .domain.usecase.crud_use_case import CrudUseCase
from .repository.user_repository_in_memory_impl import UserRepositoryInMemoryImpl


@lru_cache
def get_settings():
    return Settings()


async def verify_key(x_api_key: Optional[str] = Header(
    default='',
    include_in_schema=False,
    example='1234',
    title='Llave de verificación'
)):
    if not x_api_key or x_api_key != get_settings().x_api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Encabezado X-Token inválido")


async def verify_token(token: str = Header(...)):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se se ha proveido el Token")


def user_repository_impl():
    return UserRepositoryInMemoryImpl()


def crud_use_case(repository: UserRepository = Depends(user_repository_impl)):
    return CrudUseCase(repository)
