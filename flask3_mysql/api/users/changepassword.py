from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from config.extensions import db
from models import Users

api_changepwd = Blueprint('api_changepwd', __name__, url_prefix='/api')
bcrypt = Bcrypt()

@api_changepwd.route('/changepassword/<int:id>', methods=['PATCH'])
@jwt_required()
def changePassword(id):
    req = request.get_json()
    pwd = req["password"]
    user =  db.get_or_404(Users, id)    
    if user is not None:
        hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        user.password = hash
        db.session.commit()
        return jsonify({
            'message': 'You have change your password successfully.'
            }), 200        
    else:
        return jsonify({"message": "User ID is not found."}), 404

