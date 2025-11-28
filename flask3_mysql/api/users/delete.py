from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.extensions import db
from models import Users

api_deleteuser = Blueprint('api_deleteuser', __name__, url_prefix='/api') 

@api_deleteuser.route('/deleteuser/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteUser(id):
    user =  db.get_or_404(Users, id)    
    if user is not None:
        db.session.delete(user)            
        return jsonify({'message': f'User ID {id} has been deleted.'}), 200
    else:
        return jsonify({
            "message": "User ID not found."
        }), 200

