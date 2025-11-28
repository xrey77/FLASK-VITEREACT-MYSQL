from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Numeric, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from config.extensions import db
from flask import jsonify

class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32),nullable=False)
    lastname = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    mobile = db.Column(db.String(32))
    username = db.Column(db.String(32),nullable=False, unique=True)
    password = db.Column(db.String(200),nullable=False)
    roles = db.Column(db.String(10), server_default="ROLE_USER")
    isactivated = db.Column(db.Integer, server_default=text("0"))
    isblocked = db.Column(db.Integer, server_default=text("0"))
    mailtoken = db.Column(db.Integer, server_default=text("0"))
    userpic = db.Column(String(100))    
    secret = db.Column(db.LargeBinary(length=60), nullable=True)
    qrcodeurl = db.Column(db.LargeBinary, nullable=True)    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
        
    def to_dict(self, secret=None, qrcodeurl=None):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'mobile': self.mobile,            
            'username': self.username,
            'roles': self.roles,
            'isactivated': self.isactivated,
            'iblocked': self.isblocked,
            'mailtoken': self.mailtoken,
            'userpic': self.userpic,
            'secret': self.secret.decode('utf-8') if self.secret else None,
            'qrcodeurl': self.qrcodeurl.decode('utf-8') if self.qrcodeurl else None
        }

    def __repr__(self):
        return f"<Users '{self.id}','{self.firstname}','{self.lastname}'>"
    
class Products(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(8),nullable=False, unique=True)
    descriptions = db.Column(db.String(50),nullable=False, unique=True)
    qty= db.Column(db.Integer, server_default=text("0"))
    unit = db.Column(db.String(10),nullable=False)
    costprice = db.Column(db.Numeric(10,2),nullable=False)
    sellprice = db.Column(db.Numeric(10,2),nullable=False)
    saleprice = db.Column(db.Numeric(10,2),nullable=False)    
    alertstocks = db.Column(db.Integer, server_default=text("0"))
    criticalstocks = db.Column(db.Integer, server_default=text("0"))
    productpicture = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())        

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'descriptions': self.descriptions,
            'qty': self.qty,
            'unit': self.unit,
            'costprice': self.costprice,
            'sellprice': self.sellprice,
            'saleprice': self.saleprice,
            'productpicture': self.productpicture,
            'alertstocks': self.alertstocks,
            'criticalstocks': self.criticalstocks,
        }

    def __repr__(self):
        return f"<Products '{self.id}','{self.category}','{self.descriptions}'>"
