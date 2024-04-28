import json
import uuid
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deporte_deportista import DeporteDeportista
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum
from src.models.plan_subscripcion import PlanSubscripcion
from sqlalchemy import delete

fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    info_deportista = {
        'nombre': fake.name(),
        'apellido': fake.name(),
        'tipo_identificacion': fake.random_element(elements=(
            tipo_identificacion.value for tipo_identificacion in TipoIdentificacionEnum)),
        'numero_identificacion': fake.random_int(min=1000000, max=999999999),
        'email': fake.email(),
        'genero': fake.random_element(elements=(genero.value for genero in GeneroEnum)),
        'edad': fake.random_int(min=18, max=100),
        'peso': fake.pyfloat(3, 1, positive=True),
        'altura': fake.random_int(min=140, max=200),
        'pais_nacimiento': fake.country(),
        'ciudad_nacimiento': fake.city(),
        'pais_residencia': fake.country(),
        'ciudad_residencia': fake.city(),
        'antiguedad_residencia': fake.random_int(min=0, max=10),
        'contrasena': fake.password(),
        'deportes' : [ {"atletismo": 1}, {"ciclismo": 0}]
    }
    deportista_random = Deportista(**info_deportista)

    info_deporte = {
        'nombre': 'Atletismo',
    }
    deporte_random = Deporte(**info_deporte)
    db_session.add(deporte_random)
    db_session.commit()

    info_plan_subscripcion = {
        'nombre': 'Gratis',
    }
    planSubs_random = PlanSubscripcion(**info_plan_subscripcion)
    db_session.add(planSubs_random)
    db_session.commit()

            
    yield {
        'deportes': deporte_random,
        'deportista': deportista_random,
        'plan_subscripcion': planSubs_random
    }

    db_session.delete(deporte_random)
    db_session.delete(planSubs_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestRegistroDeportista():

    @patch('requests.get')
    def test_registro_deportista_exitoso(self, mock_get, setup_data: Deportista):
        '''Prueba de crear un deportista exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": setup_data['deportista'].email,
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": setup_data['deportista'].peso,
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 200
            

    def test_registro_deportista_existente(self, setup_data: Deportista):
        '''Prueba de crear un deportista exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": setup_data['deportista'].email,
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": setup_data['deportista'].peso,
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 432
            
            tmp_deportista = db_session.query(Deportista).filter(Deportista.email == setup_data['deportista'].email).first()
            deleSTMS = delete(DeporteDeportista).where(DeporteDeportista.id_deportista == tmp_deportista.id)
            db_session.execute(deleSTMS)
            db_session.delete(tmp_deportista)
            db_session.commit()

    def test_registro_deportista_campos_vacios(self):
        '''Prueba de crear un deportista con campos vacios'''
        with app.test_client() as test_client:
            body = {
                "nombre": "",
                "apellido": "",
                "tipo_identificacion": "",
                "numero_identificacion": "",
                "email": "",
                "genero": "",
                "edad": "",
                "peso": "",
                "altura": "",
                "pais_nacimiento": "",
                "ciudad_nacimiento": "",
                "pais_residencia": "",
                "ciudad_residencia": "",
                "antiguedad_residencia": "",
                "contrasena": "",
                "deportes" : []
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400

    def test_registro_deportista_identificacion_mayor_10digitos(self, setup_data: Deportista):
        '''Prueba de crear un deportista con identificacion mayor a 15 digitos'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": fake.random_int(min=1000000000000000, max=9999999999999999),
                "email": fake.email(),
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": setup_data['deportista'].peso,
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400

    def test_registro_deportista_edad_mayor_3digitos(self, setup_data: Deportista):
        '''Prueba de crear un deportista con edad mayor a 3 digitos'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": fake.email(),
                "genero": setup_data['deportista'].genero,
                "edad": fake.random_int(min=1000, max=9999),
                "peso": setup_data['deportista'].peso,
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400

    def test_registro_deportista_peso_3digitos_1decimal(self, setup_data: Deportista):
        '''Prueba de crear un deportista con peso mayor a 3 digitos y 1 decimal'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": fake.email(),
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": fake.pyfloat(4, 2, positive=True),
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400

    def test_registro_deportista_altura_mayor_3digitos(self, setup_data: Deportista):
        '''Prueba de crear un deportista con altura mayor a 3 digitos'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": fake.email(),
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": setup_data['deportista'].peso,
                "altura": fake.random_int(min=1000, max=99999),
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": setup_data['deportista'].antiguedad_residencia,
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400

    def test_registro_deportista_tiempo_residencia_mayor_3digitos(self, setup_data: Deportista):
        '''Prueba de crear un deportista con tiempo de residencia mayor a 3 digitos'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data['deportista'].nombre,
                "apellido": setup_data['deportista'].apellido,
                "tipo_identificacion": setup_data['deportista'].tipo_identificacion,
                "numero_identificacion": setup_data['deportista'].numero_identificacion,
                "email": fake.email(),
                "genero": setup_data['deportista'].genero,
                "edad": setup_data['deportista'].edad,
                "peso": setup_data['deportista'].peso,
                "altura": setup_data['deportista'].altura,
                "pais_nacimiento": setup_data['deportista'].pais_nacimiento,
                "ciudad_nacimiento": setup_data['deportista'].ciudad_nacimiento,
                "pais_residencia": setup_data['deportista'].pais_residencia,
                "ciudad_residencia": setup_data['deportista'].ciudad_residencia,
                "antiguedad_residencia": fake.random_int(min=1000, max=99999),
                "contrasena": setup_data['deportista'].contrasena,
                "deportes" : setup_data['deportista'].deportes
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400
