import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte_deportista import DeporteDeportista
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum


fake = Faker()
logger = logging.getLogger(__name__)
token = ""


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
        'deportes' : [ {"atletismo": 1}, {"ciclismo": 1}]
    }

    deportista_random = Deportista(**info_deportista)
    db_session.add(deportista_random)
    db_session.commit()


    yield deportista_random


    
    tmp_deportista = db_session.query(Deportista).filter(
        Deportista.email == deportista_random.email).first()
    if tmp_deportista is not None:
        tmp_deporte_deportista = db_session.query(DeporteDeportista).filter(DeporteDeportista.id_deportista == tmp_deportista.id).first()
        
        # if tmp_deporte_deportista is not None:
        #     db_session.delete(tmp_deporte_deportista)
        
        # db_session.delete(tmp_deportista)
        db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestObtenerDeportista():

    def test_obtener_deportista_exitoso(self, setup_data: Deportista):
        '''Prueba de obtener un deportista exitosamente'''
        with app.test_client() as test_client:
            #Se genera un login para el deportista y obtener el token
            usuario_deportista = {
                    "email": setup_data.email,
                    "contrasena": setup_data.contrasena
                }
            client = app.test_client()
            solicitud_login = client.post("registro-usuarios/login/deportista",
                                                data=json.dumps(usuario_deportista),
                                                headers={'Content-Type': 'application/json'})
            respuesta_login = json.loads(solicitud_login.get_data())
            token = respuesta_login['token']
            #Definir endpoint, encabezados y hacer el llamado
            endpoint_deportista = "registro-usuarios/registro/deportista"
            headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}
            resultado_obtener_deportista = test_client.get(endpoint_deportista, headers=headers)
            assert resultado_obtener_deportista.status_code == 200