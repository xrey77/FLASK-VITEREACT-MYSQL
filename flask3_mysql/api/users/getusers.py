import math
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from config.extensions import db
from models import Users
from sqlalchemy import select, func

api_getusers = Blueprint('api_getusers', __name__, url_prefix='/api') # Use url_prefix to group all API routes

@api_getusers.route('/getallusers/<int:page>', methods=['GET'])
@jwt_required()
def getUsers(page):
    perPage = 5
    try:
        queryCnt =  db.session.query(func.count()).select_from(Users)                    
        totRecords = queryCnt.scalar()

        totalPage = math.ceil(totRecords / perPage)    
        query = db.paginate(db.select(Users).order_by(Users.id), page=page, per_page=perPage, error_out=False)        
        users = [item.to_dict() for item in query.items]    
        
        if len(users) == 0:
            return jsonify({
                'message': f"No record(s) found."
            }), 404
            
        return jsonify({
            "page": page,
            "totpage": totalPage,
            "totalrecords": totRecords,
            "users": users
        }), 200
    except Exception as e:
        return jsonify({
            'message': f"Error! {e}"
        }), 404
        