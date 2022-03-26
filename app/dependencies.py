import logging
from functools import lru_cache

from fastapi import Header, HTTPException, Depends
from starlette import status

from .config import Settings
from .domain.logics.user_repository import UserRepository
from .domain.models.exception import MessageErrorResponse
from .domain.usecase.crud_user_use_case import CrudUserUseCase
from .repository.user_repository_in_memory_impl import UserRepositoryInMemoryImpl

logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return Settings()


async def verify_key(x_api_key: str = Header(
    default='',
    include_in_schema=True,
    example='1234',
    title='Llave de verificación'
)):
    """
    Verificar api key con el valor en la configuracion
    :param x_api_key:
    :return: None
    :except HTTPException Si no se encuentra o no es igual al api key de la configuracion
    """
    logger.info('Verificando X-Api-Key')
    if not x_api_key or x_api_key != get_settings().x_api_key:
        logger.error(f'X-Api-Key inválido. {x_api_key} != {get_settings().x_api_key}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=MessageErrorResponse(msg="Encabezado X-Token inválido", type="verify")
        )


def user_repository_impl():
    """
    Creación del repositorio Para la inyeccion de dependencia
    :return: UserRepository
    """
    logger.info('Creando Repositorio de usuario')
    return UserRepositoryInMemoryImpl()


def crud_use_case(repository: UserRepository = Depends(user_repository_impl)):
    """
    Creación del caso de uso Para la inyeccion de dependencia
    :return: CrudUserUseCase
    """
    logger.info('Creando caso de uso de CRUD de usuarios')
    return CrudUserUseCase(repository)
