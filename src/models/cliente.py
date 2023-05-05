from datetime import datetime
from src.database import db, ma
from src.models.consulta import Consulta

class Cliente(db.Model):
    documento = db.Column(db.String(10), primary_key = True)
    tipo_documento = db.Column(db.String(80),nullable = False)
    nombre = db.Column(db.String(80), nullable = True)
    apellido = db.Column(db.String(80), nullable = True)
    telefono = db.Column(db.String(80), nullable = True, unique = True)
    email = db.Column(db.String(60), nullable = True)
    ciudad_residencia = db.Column(db.String(60), nullable = True)
    edad = db.Column(db.Integer, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    consultas = db.relationship('Consulta', backref="owner")
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Cliente >>> {self.nombre}"

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Cliente
        include_fk = True

cliente_schema = ClienteSchema() #uno solo 
clientes_schema = ClienteSchema(many = True) #listado
