from datetime import datetime
from src.database import db, ma

class Reserva(db.Model):
    id = db.Column(db.String(5), primary_key = True)
    origen = db.Column(db.String(100), nullable = False)
    destino = db.Column(db.String(100), nullable = False)
    fecha = db.Column(db.Date, nullable = True)
    estado = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    id_consulta = db.Column(db.String(10), db.ForeignKey('consulta.id', onupdate="CASCADE",ondelete="RESTRICT"), nullable = False)
    #consultas = db.relationship('Consulta', backref="reserva_owner")
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Reserva >>> {self.origen}"

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Reserva
        include_fk = True

reserva_schema = ReservaSchema() #uno solo 
reservas_schema = ReservaSchema(many = True) #listado
