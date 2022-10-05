from fastapi import APIRouter
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(tags=['Cart'], prefix='/cart')

@router.get('/')
async def get_carts():
    logging.info('Acesso ao Módulo do Carrinho')
    return "Módulo do Carrinho"