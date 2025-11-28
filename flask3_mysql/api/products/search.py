import math
from flask import Blueprint, jsonify, request
from config.extensions import db
from models import Products
from sqlalchemy import select, func, or_

api_prodsearch = Blueprint('api_prodsearch', __name__, url_prefix='/api') # Use url_prefix to group all API routes

@api_prodsearch.route('/products/search/<int:page>/<keyword>', methods=['GET'])
def productSearch(page, keyword):
    perPage = 5
    search = f"%{keyword.lower()}%"

    queryCnt =  db.session.query(func.count()).select_from(Products)    
    totRecords = queryCnt.where(or_(Products.descriptions.ilike(search))).scalar()

    totalPage = math.ceil(totRecords / perPage)    

    stmt = select(Products).order_by(Products.id)

    stmt = stmt.where(or_(Products.descriptions.ilike(search)))
    pagination = db.paginate(stmt, page=page, per_page=perPage, error_out=False)
    
    prods = [item.to_dict() for item in pagination.items]        
    if len(prods)== 0:
        return jsonify({
            'message': 'No Product(s) found.'
        }), 404
    
    
    return jsonify({
        "page": page,
        "totpage": totalPage,
        "totalrecords": totRecords,
        "products": prods
    }), 200
