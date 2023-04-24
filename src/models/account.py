from datetime import datetime
from src.database import db, ma

class Account(db.Model):
    code = db.Column(db.String(5), primary_key = True)
    observation = db.Column(db.String(100), nullable = False)
    balance = db.Column(db.Double, nullable = False)
    registered_phone = db.Column(db.String(10), unique = True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    user_id = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE",ondelete="RESTRICT"), nullable = False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"User >>> {self.name}"

class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Account
        include_fk = True

account_schema = AccountSchema() #uno solo 
accounts_schema = AccountSchema(many = True) #listado
