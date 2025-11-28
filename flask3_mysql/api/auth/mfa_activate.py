import pyotp
import qrcode
import base64
import io
from flask import Blueprint, jsonify, request
from config.extensions import db
from models import Users
from datetime import datetime

api_mfa = Blueprint('api_mfa', __name__, url_prefix='/auth') # Use url_prefix to group all API routes

@api_mfa.route('/mfa/activate/<int:id>', methods=['PATCH'])
def mfaActivate(id):
    req = request.get_json()

    if req.get("TwoFactorEnabled"):

        
        user =  db.get_or_404(Users, id)    
        if user is not None:
            secret = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="BARCLAYS BANK")            

            img = qrcode.make(uri)            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            imgbase64 = base64.b64encode(buffer.read()).decode('utf-8')

            user.qrcodeurl = imgbase64
            user.secret = secret
            db.session.commit()
            # data:image/png;base64,
        return jsonify({
            "qrcodeurl": imgbase64,
            "message": "Multi-Factor Authenticator has been enabled."
        }), 200    
    else:
        
        user =  db.get_or_404(Users, id)    
        user.qrcodeurl = None
        user.secret = None
        db.session.commit()
        
        return jsonify({
            "message": "Multi-Factor Authenticator has been disabled."
        }), 200
        
