from datetime import datetime
from src.database import db, ma
from src.models.consulta import Consulta

class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable = False)
    tipo_viaje = db.Column(db.String(80), nullable = False)
    valor = db.Column(db.Float, nullable = False)
    caracteristicas = db.Column(db.String(80), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now())
    
    consultas = db.relationship('Consulta', backref="viaje_owner")
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Viaje >>> {self.tipo_viaje}"
    
class ViajeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Viaje
        include_fk = True

viaje_schema = ViajeSchema()
viajes_schema = ViajeSchema(many=True)
