from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, EmailStr
from pydantic.types import UUID, PastDate


class UserCreate(BaseModel):
    name: str = Field(title='Nombre', max_length=200, min_length=1, example='Juan')
    lastname: Optional[str] = Field(None, title='Nombre del usuario', max_length=200, example='Perez Montes')
    email: EmailStr = Field(title='Correo electrónico', example='email@mail.com')
    birth_date: PastDate = Field(title='Fecha de nacimiento', example='2000-10-20')


class User(UserCreate):
    id: UUID = Field(default_factory=uuid4)
