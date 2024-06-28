from fastapi import APIRouter
from src.schemas.product import Product
from src.config.database import db
import json

router = APIRouter()

# Montagem do SQL de insert no banco
def builder_register_product_query(product: Product):

    pricing = f"""{json.dumps({"amount": product.pricing['amount'], "currency": f"{product.pricing['currency']}"})}"""
    
    availability = f"""{json.dumps({"quantity": product.availability['quantity'], "timestamp": f"{product.availability['timestamp']}"})}"""

    return f"""
                INSERT INTO products (id, name, description, pricing, availability, category)
                VALUES (
                    '{product.id}',
                    '{product.name}',
                    '{product.description}',
                    '{pricing}',
                    '{availability}',
                    '{product.category}'
                );
                """


#  Rota para inserção dos dados
@router.post("/register", status_code=201)
async def register_product(product: Product):

    """
    Rota utilizada para registrar um novo produto no sistema.

    Args:
        product: Objeto contendo os detalhes do produto a ser registrado.

    Returns:
        Retorna uma mensagem de confirmação após o registro bem-sucedido do produto.
    """

    query = builder_register_product_query(product)
    db.execute(query)
    return {"message": "Product registed with successfully"}