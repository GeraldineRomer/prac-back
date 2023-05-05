from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.consulta import Consulta, consulta_schema, consultas_schema

consultas = Blueprint("consultas", __name__ ,url_prefix="/api/v1")

@consultas.get("/consultas")
def read_all():
    consultas = Consulta.query.order_by(Consulta.id).all()
    return {"data": consultas_schema.dump(consultas)}, HTTPStatus.OK

@consultas.get("/consultas/<int:id>")
def read_one(id):
    consulta = Consulta.query.filter_by(id=id).first()
    
    if(not consulta):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": consulta_schema.dump(consulta)}, HTTPStatus.OK

@consultas.post("/clientes/<int:documento_cliente>/viajes/<int:id_viaje>/consultas")
def create(documento_cliente,id_viaje):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    consulta = Consulta(id = request.get_json().get("id",None),
                documento_cliente = documento_cliente,
                id_viaje = id_viaje)

    try:
        db.session.add(consulta)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":consulta_schema.dump(consulta)},HTTPStatus.CREATED


@consultas.patch('/clientes/<int:documento_cliente>/viajes/<int:id_viaje>/consultas/<int:id>')
@consultas.put('/clientes/<int:documento_cliente>/viajes/<int:id_viaje>/consultas/<int:id>')
def update(id,documento_cliente,id_viaje):
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
    
    consulta = Consulta.query.filter_by(id=id).first()
    
    if(not consulta):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    if (documento_cliente != consulta.documento_cliente):
        consulta.documento_cliente = documento_cliente
    if (id_viaje != consulta.id_viaje):
        consulta.id_viaje = id_viaje

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":consulta_schema.dump(consulta)}, HTTPStatus.OK

@consultas.delete("/consultas/<int:id>")
def delete(id):
    consulta = Consulta.query.filter_by(id=id).first()
    
    if(not consulta):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(consulta)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT

