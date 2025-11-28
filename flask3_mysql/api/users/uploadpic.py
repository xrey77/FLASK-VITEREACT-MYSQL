import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request
from config.extensions import db
from models import Users

api_profilepic = Blueprint('api_profilepic', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
basedir = os.path.abspath(os.path.dirname('static'))
IMAGES_DIR = os.path.join(basedir, 'static/users/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_profilepic.route('/uploadpicture/<int:id>', methods=['PATCH'])
def profilePicture(id):

    if 'userpic' not in request.files:
        return jsonify({
            "message": "No Image found."
        }), 400
    
    
    file = request.files['userpic']

    if file.filename == '':
        return jsonify({
            "message": "No Selected Image."
        }), 400


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # newFile = "00" + str(id) + ext
        name, ext = os.path.splitext(filename)        
        prefix = "00"
        pref = ".*"
        
        
        newFile = f"{prefix}{id}{ext}"
        user =  db.get_or_404(Users, id)    
        if user is not None:
            dbPic = user.userpic        
            oldFile = secure_filename(dbPic.split('/')[-1])
            if oldFile != "pix.png":
                xfile = IMAGES_DIR + oldFile
                os.remove(xfile)
            
            user.userpic = "http://127.0.0.1:5000/api/users/" + newFile
            db.session.commit()

            
        file.save(os.path.join(IMAGES_DIR, newFile))            
        return jsonify({
            "userpic": "http://127.0.0.1:5000/api/users/" + newFile,
            "message": "Your profile picture has been changed succesfully."
        }), 200

        # return redirect(url_for('download_file', name=filename))



    # if user is not None:
    #     return jsonify({
    #         'id': user.id,
    #         }), 200        
    # else:
    #     return jsonify({
    #         "message": "Login Successfully."
    #     }), 400

