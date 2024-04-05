import logging
from flask import Blueprint, request, jsonify, make_response
from src.commands.registro.registrar_deportista import RegistrarDeportista


logger = logging.getLogger(__name__)
registro_blueprint = Blueprint('registro', __name__)


@registro_blueprint.route('/deportistas', methods=['POST'])
def registrar_deportista():
    body = request.get_json()

    result = RegistrarDeportista(
        body.get('nombre', None),
        body.get('apellido', None),
        body.get('tipo_identificacion', None),
        body.get('numero_identificacion', None),                        
        body.get('email', None),
        body.get('genero', None),
        body.get('edad', None),
        body.get('peso', None),
        body.get('altura', None),
        body.get('pais_nacimiento', None),
        body.get('ciudad_nacimiento', None),
        body.get('pais_residencia', None),
        body.get('ciudad_residencia', None),
        body.get('antiguedad_residencia', None),
        body.get('contrasena', None)
    ).execute()
    return make_response(jsonify(result), 200)