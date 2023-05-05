from flask import Blueprint, request
from datetime import datetime
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from src.database import db
from src.models.reserva import Reserva, reserva_schema, reservas_schema

reservas = Blueprint("reservas", __name__ ,url_prefix="/api/v1")

@reservas.get("/reservas")
def read_all():
    reservas = Reserva.query.order_by(Reserva.id).all()
    return {"data": reservas_schema.dump(reservas)}, HTTPStatus.OK

@reservas.get("/reservas/<int:id>")
def read_one(id):
    reserva = Reserva.query.filter_by(id=id).first()
    
    if(not reserva):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": reserva_schema.dump(reserva)}, HTTPStatus.OK

@reservas.post("/consultas/<int:id_consulta>/reservas")
def create(id_consulta):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST
    
    fecha = request.get_json().get("fecha",None)
    fecha_ = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    reserva = Reserva(id = request.get_json().get("id",None),
                    origen = request.get_json().get("origen",None),
                    destino = request.get_json().get("destino",None),
                    fecha = fecha_,
                    estado = request.get_json().get("estado",None),
                    id_consulta = id_consulta)

    try:
        db.session.add(reserva)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":reserva_schema.dump(reserva)},HTTPStatus.CREATED


@reservas.patch('/consultas/<int:id_consulta>/reservas/<int:id>')
@reservas.put('/consultas/<int:id_consulta>/reservas/<int:id>')
def update(id,id_consulta):
    post_data=None
    
    try:
        post_data=request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
    
    reserva = Reserva.query.filter_by(id=id).first()
    
    if(not reserva):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    if (id_consulta != reserva.id_consulta):
        reserva.documento_cliente = id_consulta

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST
        
    return {"data":reserva_schema.dump(reserva)}, HTTPStatus.OK

@reservas.delete("/reservas/<int:id>")
def delete(id):
    reserva = Reserva.query.filter_by(id=id).first()
    
    if(not reserva):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(reserva)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT

