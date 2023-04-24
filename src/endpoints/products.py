from flask import Blueprint, request
from http import HTTPStatus
from src.database import db
from src.models.product import Product

products = Blueprint("products",__name__,url_prefix="/api/v1/products")

@products.get("/")
def read_all():
    pass

@products.get("/<int:id>")
def read_one(id):
    pass


@products.post("/")
def create():
    pass


@products.put('/<int:id>')
@products.patch('/<int:id>')
def update(id):
    pass

@products.delete("/<int:id>")
def delete(id):
    pass
#Proveedores de un producto
@products.get("/<int:id_producto>/providers")
def read_providers(id):
    pass
