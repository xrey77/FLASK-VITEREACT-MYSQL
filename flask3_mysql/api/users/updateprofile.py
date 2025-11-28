from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.extensions import db
from models import Users

api_profile = Blueprint('api_profile', __name__, url_prefix='/api') # Use url_prefix to group all API routes

@api_profile.route('/updateprofile/<int:id>', methods=['PATCH'])
@jwt_required()
def updateProfile(id):
    req = request.get_json()
    fname = req["firstname"]
    lname = req["lastname"]
    mobile = req["mobile"]
    
    user =  db.get_or_404(Users, id)        
    if user is not None:
        user.firstname = fname
        user.lastname = lname
        user.mobile = mobile
        db.session.commit()
        return jsonify({
            "message": "Your profile info has been updated."
        }), 200        
    else:
        return jsonify({
            "message": "User ID not found."
        }), 440

