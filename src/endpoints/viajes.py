from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.viaje import Viaje, viaje_schema, viajes_schema

viajes = Blueprint("viajes", __name__ ,url_prefix="/api/v1/viajes")

@viajes.get("/")
def read_all():
    viajes = Viaje.query.order_by(Viaje.tipo_viaje).all()
    return {"data": viajes_schema.dump(viajes)}, HTTPStatus.OK

@viajes.get("/<int:id>")
def read_one(id):
    viaje = Viaje.query.filter_by(id=id).first()
    
    if(not viaje):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": viaje_schema.dump(viaje)}, HTTPStatus.OK

@viajes.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    viaje = Viaje(id = request.get_json().get("id",None),
                tipo_viaje = request.get_json().get("tipo_viaje",None),
                valor = request.get_json().get("valor",None),
                caracteristicas = request.get_json().get("caracteristicas",None))

    try:
        db.session.add(viaje)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":viaje_schema.dump(viaje)},HTTPStatus.CREATED


@viajes.patch('/<int:id>')
@viajes.put('/<int:id>')
def update(id):
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
    
    viaje = Viaje.query.filter_by(id=id).first()
    
    if(not viaje):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    viaje.nombre=request.get_json().get("nombre", viaje.nombre)
    viaje.tipo_viaje=request.get_json().get("tipo_viaje", viaje.tipo_viaje)
    viaje.valor=request.get_json().get("valor", viaje.valor)
    viaje.caracteristicas=request.get_json().get("caracteristicas", viaje.caracteristicas)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":viaje_schema.dump(viaje)}, HTTPStatus.OK

@viajes.delete("/<int:id>")
def delete(id):
    viaje = Viaje.query.filter_by(id=id).first()
    
    if(not viaje):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(viaje)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT

