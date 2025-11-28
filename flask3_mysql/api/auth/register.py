import os
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from config.extensions import db
from models import Users

api_signup = Blueprint('api_signup', __name__, url_prefix='/auth') # Use url_prefix to group all API routes

bcrypt = Bcrypt()

@api_signup.route('/signup', methods=['POST'])
def userRegister():
    req = request.get_json()
    plain = req.get("password")
    hash = bcrypt.generate_password_hash(plain).decode('utf-8')
    mail = req.get("email")
    usrname = req.get("username")
    
    userEmail = Users.query.filter_by(email=mail).first()        
    if userEmail is not None:
        return jsonify({
            "message": "Email Address is already taken."
        }), 400
    
    userName = Users.query.filter_by(username=usrname).first() 
    if userName is not None:
        return jsonify({
            "message": "Username is already taken."
        }), 400
    
        
    user = Users(
        firstname = req.get("firstname"),
        lastname = req.get("lastname"),
        email =  mail,
        mobile = req.get("mobile"),
        roles = "ROLE_ADMIN",
        isactivated = 1,
        userpic = "http://127.0.0.1:5000/api/users/pix.png",
        username = usrname,
        password = hash        
    )

    try:    
        db.session.add(user)
        db.session.commit()    
        return jsonify({
            "message": "You have registered successfully, please sign-in now."
        }), 200
    except Exception as e:
        return jsonify({
            "message": f"Error! {e}"
        }), 400
        
