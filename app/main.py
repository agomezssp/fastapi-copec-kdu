import logging
import time

from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from .dependencies import get_settings
from .domain.models.exception import NotFoundException, MessageErrorResponse, ExistsEmailException
from .routers import crud

logger = logging.getLogger(__name__)

logger.info('Inicializando aplicación')
app = FastAPI(
    title="Demo",
    dependencies=[Depends(get_settings)]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allow_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info('Configuración de los CORS realizada')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.debug(f"start request path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"finish request with response{response}")
    return response
logger.info('Configuración de medicion de tiempo de la peticion adicionada correctamente')


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """Manejo de excepcion Generica"""
    error_message = f"{exc}"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(MessageErrorResponse(
            msg=error_message,
            type="unexpected_error"
        ))
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Manejo de excepcion de errores de validación"""
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    """Manejo de excepcion de errores Genericos de HTTP"""
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(exc.detail), )


@app.exception_handler(ValidationError)
async def exception_handler(request: Request, exc: ValidationError):
    """Manejo de excepcion de errores de validación"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(NotFoundException)
async def exception_handler(request: Request, exc: NotFoundException):
    """Manejo de excepcion para elementos no encontrados"""
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(exc), )


@app.exception_handler(ExistsEmailException)
async def exception_handler(request: Request, exc: ExistsEmailException):
    """Manejo de excepcion de errores de validación"""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(exc), )


app.include_router(crud.router)
