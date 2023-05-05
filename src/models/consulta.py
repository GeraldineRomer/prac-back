from datetime import datetime
from src.database import db, ma
from src.models.reserva import Reserva

class Consulta(db.Model):
    id = db.Column(db.String(5), primary_key = True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    documento_cliente = db.Column(db.String(10), db.ForeignKey('cliente.documento', onupdate="CASCADE",ondelete="RESTRICT"), nullable = False)
    id_viaje = db.Column(db.String(10), db.ForeignKey('viaje.id', onupdate="CASCADE",ondelete="RESTRICT"), nullable = False)
    
    reservas = db.relationship('Reserva', foreign_keys="Reserva.id_consulta")
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Reserva >>> {self.origen}"

class ConsultaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Consulta
        include_fk = True

consulta_schema = ConsultaSchema() #uno solo 
consultas_schema = ConsultaSchema(many = True) #listado
