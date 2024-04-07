import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista, GeneroEnum, Tipo_IdentificacionEnum


fake = Faker()
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def setup_data():
        deportista_random = Deportista(
            nombre=fake.name(),
            apellido=fake.name(),
            tipo_identificacion=fake.random_element(elements=(
                tipo_identificacion.value for tipo_identificacion in Tipo_IdentificacionEnum)),
            numero_identificacion=fake.random_int(min=1000000, max=9999999),
            email=fake.email(),
            genero=fake.random_element(
                elements=(genero.value for genero in GeneroEnum)),
            edad=fake.random_int(min=18, max=100),
            peso=fake.random_int(min=40, max=200),
            altura=fake.random_int(min=140, max=200),
            pais_nacimiento=fake.country(),
            ciudad_nacimiento=fake.city(),
            pais_residencia=fake.country(),
            ciudad_residencia=fake.city(),
            antiguedad_residencia=fake.random_int(min=0, max=10),
            contrasena=fake.password())
        return deportista_random


@pytest.mark.usefixtures("setup_data")
class TestRegistroDeportista():

    def test_registro_deportista_exitoso(self, setup_data: Deportista):
        '''Prueba de crear un deportista exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data.nombre,
                "apellido": setup_data.apellido,
                "tipo_identificacion": setup_data.tipo_identificacion,
                "numero_identificacion": setup_data.numero_identificacion,
                "email": setup_data.email,
                "genero": setup_data.genero,
                "edad": setup_data.edad,
                "peso": setup_data.peso,
                "altura": setup_data.altura,
                "pais_nacimiento": setup_data.pais_nacimiento,
                "ciudad_nacimiento": setup_data.ciudad_nacimiento,
                "pais_residencia": setup_data.pais_residencia,
                "ciudad_residencia": setup_data.ciudad_residencia,
                "antiguedad_residencia": setup_data.antiguedad_residencia,
                "contrasena": setup_data.contrasena
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 200  
            assert response.json['message'] == 'success'
    
    def test_registro_deportista_existente(self, setup_data: Deportista):
        '''Prueba de crear un deportista exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data.nombre,
                "apellido": setup_data.apellido,
                "tipo_identificacion": setup_data.tipo_identificacion,
                "numero_identificacion": setup_data.numero_identificacion,
                "email": setup_data.email,
                "genero": setup_data.genero,
                "edad": setup_data.edad,
                "peso": setup_data.peso,
                "altura": setup_data.altura,
                "pais_nacimiento": setup_data.pais_nacimiento,
                "ciudad_nacimiento": setup_data.ciudad_nacimiento,
                "pais_residencia": setup_data.pais_residencia,
                "ciudad_residencia": setup_data.ciudad_residencia,
                "antiguedad_residencia": setup_data.antiguedad_residencia,
                "contrasena": setup_data.contrasena
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 432

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
                "contrasena": ""
            }

            response = test_client.post(
                'registro-usuarios/registro/deportistas', json=body)

            assert response.status_code == 400