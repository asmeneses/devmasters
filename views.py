from flask import request, jsonify
from config import Config
from models import db, BlacklistEmail
from application import application
import uuid
import re

# Expresión para validar emails
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email):
    #Verifica si el email tiene un formato válido.
    return re.match(EMAIL_REGEX, email) is not None

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token.split()[1] != Config.SECRET_TOKEN:
            return jsonify({'message': 'Token is missing or invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid.UUID(uuid_to_test, version=version)
        return True
    except ValueError:
        return False

@application.route('/blacklists', methods=['POST'], endpoint='add_to_blacklist_endpoint')
@token_required
def add_to_blacklist():
    data = request.get_json()
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    blocked_reason = data.get('blocked_reason')
    
    if not email or not app_uuid:
        return jsonify({'message': 'Email and app_uuid are required!'}), 400
    
    # Verificar si el email tiene un formato válido
    if not is_valid_email(email):
        return jsonify({"error": "Email no válido"}), 400
    
    # Validación del UUID
    if not is_valid_uuid(app_uuid):
        return jsonify({'message': 'Invalid app_uuid, must be a valid UUID!'}), 400

    # Validación del motivo (blocked_reason)
    if blocked_reason and len(blocked_reason) > 255:
        return jsonify({'message': 'Blocked reason must be less than 255 characters!'}), 400
    
    # Verificar si ya existe el email en la lista negra
    if BlacklistEmail.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already in blacklist!'}), 409
    
    ip_address = request.remote_addr
    new_entry = BlacklistEmail(
        email=email,
        app_uuid=app_uuid,
        blocked_reason=blocked_reason,
        ip_address=ip_address
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': f'Email {email} added to blacklist'}), 201


@application.route('/blacklists/<string:email>', methods=['GET'], endpoint='check_blacklist_endpoint')
@token_required
def check_blacklist(email):
    entry = BlacklistEmail.query.filter_by(email=email).first()

    if entry:
        return jsonify({
            'blacklisted': True,
            'blocked_reason': entry.blocked_reason
        }), 200
    else:
        return jsonify({
            'blacklisted': False,
            'message': 'Email not in blacklist'
        }), 404

