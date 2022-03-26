# Demo

### Documentaciones 

- [FastAPI](https://fastapi.tiangolo.com/)
- [Request](https://docs.python-requests.org/en/latest/)
- [Pydantic](https://pydantic-docs.helpmanual.io)
- [Uvicorn](https://www.uvicorn.org)

### Instalar la app

```shell
python3 --version
#Python 3.9.10
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar los Test

Test unitarios:
```shell
python -m unittest
#Ran 16 tests in 0.106s
#OK
```

Test de covertura:
```shell
coverage run -m unittest
#Ran 16 tests in 0.106s
#OK

coverage report -m
#TOTAL 440 12 97%

```

### Ejecutar la el servidor Rest

Comando para ejecutar la aplicación en desarrollo

Nota: `X_API_KEY` es utilizada como método de seguridad sencillo en las llamadas a los métodos de los recursos. Se debe especificar el valor deseado cuando se arranca el servidor. 
```shell
X_API_KEY=1234 uvicorn app.main:app --reload
# o
X_API_KEY=1234 python ./run.py
```

Comando para ejecutar la aplicación en Producción
```shell
uvicorn app.main:app --port 5000
```
### Documentación de los servicios
Acceder a la siguiente URL para ver la documentación de los métodos:
(http://localhost:8000/docs)

### Consultar servicios CRUD de usuarios
#### Crear usuario
```shell
curl --location --request POST 'http://localhost:8000/api/v1/user/' \
--header 'x-api-key: 1234' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw '{
  "name": "Juan",
  "email": "email@mail1.com",
  "birth_date": "2000-10-20",
  "lastname": "Perez Montes"
}'
```
#### Obtener un usuario
```shell
curl --location --request GET 'http://localhost:8000/api/v1/user/6e33c1dd-7634-4662-9d44-35a57fa5122c' \
--header 'x-api-key: 1234' \
--header 'Accept: application/json'
```

#### Actualizar usuario
```shell
curl --location --request PUT 'http://localhost:8000/api/v1/user/' \
--header 'x-api-key: 1234' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw '{
  "name": "Pedro",
  "email": "email@mail6.com",
  "birth_date": "2000-10-22",
  "lastname": "Perez Montes",
  "id": "6e33c1dd-7634-4662-9d44-35a57fa5122c"
}'
```
#### Eliminar usuario
```shell
curl --location --request DELETE 'http://localhost:8000/api/v1/user/fcae09bc-fd0d-4ba5-8b19-429483f30ca0' \
--header 'x-api-key: 1234' \
--header 'Accept: application/json'
```