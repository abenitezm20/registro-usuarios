import logging
from flask import Blueprint, request, jsonify, make_response
from src.commands.registro.registrar_deportista import RegistrarDeportista
from src.commands.registro.registrar_deporte_deportista import RegistrarDeporteDeportista
from src.commands.registro.obtener_plan_subscripcion import ObtenerPlanSubscripcion
from src.commands.registro.registrar_socios import RegistrarSocios


logger = logging.getLogger(__name__)
registro_blueprint = Blueprint('registro', __name__)


@registro_blueprint.route('/deportistas', methods=['POST'])
def registrar_deportista():
    body = request.get_json()

    id_plan_subscripcion = ObtenerPlanSubscripcion('Gratis').execute()

    info_deportista = {
        'nombre': body.get('nombre', None),
        'apellido': body.get('apellido', None),
        'tipo_identificacion': body.get('tipo_identificacion', None),
        'numero_identificacion': body.get('numero_identificacion', None),
        'email': body.get('email', None),
        'genero': body.get('genero', None),
        'edad': body.get('edad', None),
        'peso': body.get('peso', None),
        'altura': body.get('altura', None),
        'pais_nacimiento': body.get('pais_nacimiento', None),
        'ciudad_nacimiento': body.get('ciudad_nacimiento', None),
        'pais_residencia': body.get('pais_residencia', None),
        'ciudad_residencia': body.get('ciudad_residencia', None),
        'antiguedad_residencia': body.get('antiguedad_residencia', None),
        'contrasena': body.get('contrasena', None),
        'id_plan_subscripcion': id_plan_subscripcion
    }

    info_deporte_deportista = {
        'deportes': body.get('deportes', None)
    }

    result_deportista = RegistrarDeportista(**info_deportista).execute()

    result_deporte_deportista = RegistrarDeporteDeportista(info_deporte_deportista, str(result_deportista['id_deportista'])).execute()

    if  result_deportista['message'] ==  result_deporte_deportista['message']:
        return make_response(jsonify(result_deportista['message']), 200)
    else:
        return make_response(jsonify(result_deportista['message']), 400)


@registro_blueprint.route('/socios', methods=['POST'])
def registrar_socios():
    body = request.get_json()

    result = RegistrarSocios(
        body.get('nombre', None),
        body.get('tipo_identificacion', None),
        body.get('numero_identificacion', None),
        body.get('email', None),
        body.get('contrasena', None)
    ).execute()
    return make_response(jsonify(result), 200)
