from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config.extensions import db
from models import Users

api_signin = Blueprint('api_signin', __name__, url_prefix='/auth') # Use url_prefix to group all API routes

@api_signin.route('/signin', methods=['POST'])
def userLogin():
    req = request.get_json()
    usrname = req.get("username")
    passwd = req.get("password")
    
    user = Users.query.filter_by(username=usrname).first()
    if user is not None:
        if (check_password_hash(user.password, passwd)):
            
            token = create_access_token(identity=user.username)
            
            return jsonify({
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'roles': user.roles,
                'email': user.email,
                'mobile': user.mobile,
                'isactivated': user.isactivated,
                'isblocked': user.isblocked,
                'userpic': user.userpic,
                'qrcodeurl': user.qrcodeurl,
                'token': token,
                "message": "Login Successfully."
            }), 200            
        else:            
            return jsonify({
                "message": "Invalid Password, please try again."
            }), 404

    else:
        return jsonify({
            "message": "Username does not exists, please register."
        }), 400

