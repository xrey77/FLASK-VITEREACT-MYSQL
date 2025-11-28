from flask import Blueprint, jsonify, request
import pyotp
from config.extensions import db
from models import Users

api_otp = Blueprint('api_otp', __name__, url_prefix='/auth') # Use url_prefix to group all API routes

@api_otp.route('/mfa/verifytotp/<int:id>', methods=['PATCH'])
def verifyOtp(id):
    req = request.get_json()
    otp = req["otp"]
    
    user =  db.get_or_404(Users, id)    
    if user is not None:                
        if pyotp.TOTP(user.secret).verify(otp):
            return jsonify({
                "username": user.username,
                "message": "OTP code has been verified successfully."
            }), 200                
        else:
            return jsonify({
                "message": "Invalid OTP code, please try again."
            }), 400
    else:
        return jsonify({
            "message": "User not found."
        }), 400    
        
            
        
        
