from typing import Optional, List

from fastapi import APIRouter, Depends, status, Path

from ..dependencies import crud_use_case, verify_key
from ..domain.models.exception import MessageErrorResponse
from ..domain.models.user import User, UserCreate
from ..domain.usecase.crud_user_use_case import CrudUserUseCase

router = APIRouter(
    prefix="/api/v1/user",
    tags=["user_crud"],
    dependencies=[Depends(verify_key)],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": MessageErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": MessageErrorResponse},
        status.HTTP_403_FORBIDDEN: {'model': MessageErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': MessageErrorResponse}
    },
)


@router.get("/", response_model=Optional[List[User]], status_code=status.HTTP_200_OK)
async def get_all(use_case: CrudUserUseCase = Depends(crud_use_case)):
    """
    Obtener todos los usuarios
    :param use_case: Dependencia Inyectada
    :return: json
    """
    return use_case.execute_all()


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def detail(user_id: str = Path(..., title="id"), use_case: CrudUserUseCase = Depends(crud_use_case)):
    """
    Obtener un usuario
    :param user_id: Filtrar por Id
    :param use_case: Dependencia Inyectada
    :return: json
    """
    return use_case.execute_detail(user_id)


@router.post("/",
             response_model=User,
             status_code=status.HTTP_201_CREATED,
             )
async def create(user: UserCreate, use_case: CrudUserUseCase = Depends(crud_use_case)):
    """
    Crear un usuario
    :param user: Datos del usuario a ser creado
    :param use_case: Dependencia Inyectada
    :return:
    """
    return use_case.execute_create(user)


@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update(user: User, use_case: CrudUserUseCase = Depends(crud_use_case)):
    """
    Actaulizar un usuario
    :param user: Datos del usuario a se actualizado
    :param use_case: Dependencia Inyectada
    :return: usuario actualizado
    """
    return use_case.execute_update(user)


@router.delete("/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: str = Path(..., title="id"), use_case: CrudUserUseCase = Depends(crud_use_case)):
    """
    Eliminar un usuario
    :param user_id: ID del usuario a ser eliminado
    :param use_case: Dependencia Inyectada
    """
    return use_case.execute_delete(user_id)
