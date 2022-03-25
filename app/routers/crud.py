from typing import Optional, List

from fastapi import APIRouter, Depends, status, Path, Header

from ..dependencies import crud_use_case, verify_token, verify_key
from ..domain.models.user import User, UserCreate
from ..domain.usecase.crud_use_case import CrudUseCase

router = APIRouter(
    prefix="/api/v1/user",
    tags=["banking"],
    dependencies=[Depends(verify_key)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Optional[List[User]], status_code=status.HTTP_200_OK)
async def get_all(use_case: CrudUseCase = Depends(crud_use_case)):
    # await verify_key(x_api_key) # TODO revisar await bloqueo
    return use_case.execute_all()


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def detail(user_id: str = Path(..., title="id"), use_case: CrudUseCase = Depends(crud_use_case)):
    return use_case.execute_detail(user_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate, use_case: CrudUseCase = Depends(crud_use_case)):
    # await verify_key(x_api_key)  # TODO revisar await bloqueo
    return use_case.execute_create(user)


@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update(user: User, use_case: CrudUseCase = Depends(crud_use_case)):
    return use_case.execute_update(user)


@router.delete("/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: str = Path(..., title="id"), use_case: CrudUseCase = Depends(crud_use_case)):
    return use_case.execute_delete(user_id)
