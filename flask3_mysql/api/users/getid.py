from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.extensions import db
from models import Users

api_getuserid = Blueprint('api_getuserid', __name__, url_prefix='/api') 

@api_getuserid.route('/getuserid/<int:id>', methods=['GET'])
@jwt_required()
def getUserid(id):
    user =  db.get_or_404(Users, id)    
    if user is not None:
        if user.secret == None:
            secret = None
        else:
            secret = str(user.secret)
            
        if user.qrcodeurl == None:
            qrcode = None
        else:
            qrcode = str(user.qrcodeurl)
            
        return jsonify({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'mobile': user.mobile,
            'userpic': user.userpic,
            'secret': secret,
            'qrcodeurl': qrcode
            }), 200        
    else:
        return jsonify({
            "message": "User ID not found."
        }), 200

