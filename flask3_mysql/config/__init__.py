import datetime
from flask import Flask, render_template,jsonify
from config.extensions import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS, cross_origin

from api.auth.register import api_signup
from api.auth.login import api_signin
from api.auth.mfa_activate import api_mfa
from api.auth.mfa_verifyotp import api_otp

from api.users.getid import api_getuserid
from api.users.getusers import api_getusers
from api.users.uploadpic import api_profilepic
from api.users.updateprofile import api_profile
from api.users.changepassword import api_changepwd
from api.users.delete import api_deleteuser

from api.products.list import api_prodlist
from api.products.search import api_prodsearch
from api.products.deleteprod import api_deleteproduct

from api.files.users import api_userpic
from api.files.image import api_image
from api.files.products import api_prodpic

from config.main import main_bp

def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, static_url_path='', static_folder='templates')
    
            
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://rey:rey@127.0.0.1/flask3_vitereact'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    app.config["JWT_SECRET_KEY"] = "super-secret-key-that-should-be-long-and-random"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=24)     

    CORS(app, origins=["http://localhost:5173"],supports_credentials=False)
    CORS(app, methods=["GET", "POST", "PATCH", "PUT", "DELETE"])

    jwt = JWTManager(app)    
    @jwt.unauthorized_loader
    def custom_unauthorized_callback(err):
        return jsonify({
            'message': 'Unauthorized Access.',
        }), 401    
    
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(api_signup)    
    app.register_blueprint(api_signin)
    app.register_blueprint(api_mfa)
    app.register_blueprint(api_otp)

    app.register_blueprint(api_getuserid)
    app.register_blueprint(api_getusers)
    app.register_blueprint(api_prodlist)
    app.register_blueprint(api_prodsearch)
    app.register_blueprint(api_deleteuser)
    
    app.register_blueprint(api_profilepic)
    app.register_blueprint(api_profile)
    app.register_blueprint(api_changepwd)
    
    app.register_blueprint(api_image)
    app.register_blueprint(api_prodpic)
    app.register_blueprint(api_userpic)
    
    app.register_blueprint(main_bp)
    
    return app

    

