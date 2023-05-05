from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.cliente import Cliente, cliente_schema, clientes_schema

clientes = Blueprint("clientes", __name__ ,url_prefix="/api/v1/clientes")

@clientes.get("/")
def read_all():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return {"data": clientes_schema.dump(clientes)}, HTTPStatus.OK

@clientes.get("/<int:documento>")
def read_one(documento):
    cliente = Cliente.query.filter_by(documento=documento).first()
    
    if(not cliente):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": cliente_schema.dump(cliente)}, HTTPStatus.OK

@clientes.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    cliente = Cliente(documento = request.get_json().get("documento",None),
                        tipo_documento = request.get_json().get("tipo_documento",None),
                        nombre = request.get_json().get("nombre",None),
                        apellido = request.get_json().get("apellido",None),
                        telefono = request.get_json().get("telefono",None),
                        email = request.get_json().get("email",None),
                        ciudad_residencia = request.get_json().get("ciudad_residencia",None),
                        edad = request.get_json().get("edad",None))

    try:
        db.session.add(cliente)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":cliente_schema.dump(cliente)},HTTPStatus.CREATED


@clientes.patch('/<int:documento>')
@clientes.put('/<int:documento>')
def update(documento):
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
    
    cliente=Cliente.query.filter_by(documento=documento).first()
    
    if(not cliente):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    cliente.nombre=request.get_json().get("nombre", cliente.nombre)
    cliente.apellido=request.get_json().get("apellido", cliente.apellido)
    cliente.telefono=request.get_json().get("telefono", cliente.telefono)
    cliente.email=request.get_json().get("email", cliente.email)
    cliente.ciudad_residencia=request.get_json().get("ciudad_residencia", cliente.ciudad_residencia)
    cliente.edad=request.get_json().get("edad", cliente.edad)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":cliente_schema.dump(cliente)}, HTTPStatus.OK

@clientes.delete("/<int:documento>")
def delete(documento):
    cliente = Cliente.query.filter_by(documento=documento).first()
    
    if(not cliente):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(cliente)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT

