import math
from flask import Blueprint, jsonify, request
from config.extensions import db
from models import Products
from sqlalchemy import select, func

api_prodlist = Blueprint('api_prodlist', __name__, url_prefix='/api') # Use url_prefix to group all API routes

@api_prodlist.route('/products/list/<int:page>', methods=['GET'])
def productList(page):
    perPage = 5
    
    queryCnt =  db.session.query(func.count()).select_from(Products)
    totRecords = queryCnt.scalar()

    totalPage = math.ceil(totRecords / perPage)    
    query = db.paginate(db.select(Products).order_by(Products.id), page=page, per_page=perPage, error_out=False)
    products = [item.to_dict() for item in query.items]        
    return jsonify({
        "page": page,
        "totpage": totalPage,
        "totalrecords": totRecords,
        "products": products
    }), 200
