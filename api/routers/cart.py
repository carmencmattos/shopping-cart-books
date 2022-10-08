from fastapi import APIRouter, status
from pydantic.networks import EmailStr
from api.cruds.cart import add_product_cart, calculate_cart, create_cart, get_cart_by_email, insert_product, remove_item_from_cart, update_product_cart
from api.cruds.inventory import get_inventory_by_isbn
from api.cruds.product import get_product_by_isbn
from api.schemas.cart import CartListSchema
from api.utils import serialize
from starlette.responses import JSONResponse

router = APIRouter(tags=['Cart'], prefix='/cart')

@router.post('/{email}/create')
async def create(email: EmailStr, cart_list: CartListSchema):
    new_cart = await create_cart({ email, cart_list })
    if new_cart:
        cart = serialize.cart(new_cart)
        return JSONResponse(status_code=status.HTTP_200_OK, content=cart)

@router.post('/{email}/additem')
async def additem(email: EmailStr, item: CartListSchema ):
    # Verificar se existe o item no estoque
    inventory = await get_inventory_by_isbn(item.isbn)
    
    # Se existir o item no estoque
    if inventory:
            
        # Verifica se q quantidade do item solicitada pelo usuario é menor ou igual a quantidade do item encontrado no estoque 
        if item.quantity <= inventory['inventory']:

            # Se SIM, vrificar se existe carrinho aberto para o usuario, que esta adicionando o produto, por email
            has_cart = await get_cart_by_email(email)

            # Apenas declara a variavel has_product de forma global para funcionar fora do laco do FOR
            has_product = False

            # Se existir carrinho aberto para este usuário
            if has_cart:

                # Verifica em todos os possiveis produtos adicionados no carrinho encontrado se algum é igual ao produto que o ususario esta tentnado adicionar
                for found_product in has_cart['product']:
                    
                    # Caso encontre algum produto no carrinho que tenha o mesmo ISBN do produto que o usuario esta tentando adicionar no carrinho
                    if found_product['isbn'] == item.isbn:
                        
                        # Coloca o produto encontrado, igual ao do usuario, para dentro da variável has_product
                        has_product = found_product

                # Se tiver encontrado algum produto no carrinho igual ao do usuario        
                if has_product:

                    # Atualiza a quantidade do produto no carrinho com os dados de produto enviados pelo usuario (quantitity)
                    update_product = await update_product_cart(item.dict(), has_cart)

                    # Se a atualização foi realizada com sucesso
                    if update_product:

                        calculate = await calculate_cart(update_product)

                        # Retorna o carrinho atualizado e serializado
                        return_object = { 'cart': serialize.cart(calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total'] }
                        return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)

                # Se NÃO tiver encontrado algum produto no carrinho igual ao do usuário    
                else:

                    # ADICIONA o produto enviado pelo usuário no carrinho
                    add_product_in_cart = await add_product_cart(email, item.dict())

                    # Se adicionou o produto com sucesso
                    if add_product_in_cart:

                        calculate = await calculate_cart(add_product_in_cart)

                        # Retorna o carrinho atualizado e serializado
                        return_object = { 'cart': serialize.cart(calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total'] }
                        return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)

            # Se não tiver carrinho aberto para o usuário
            else:

                # Cria um carrinho aberto com o produto que o usuário enviou
                create = await create_cart(email, item)

                # Se criou o carrinho aberto com o produto adicionado com suceeeo
                if create:
                    calculate = await calculate_cart(create)
                    return_object = { 'cart': serialize.cart(calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total'] }
                    return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Este produto ultrapassa o limite do estoque.'})

@router.patch('/{email}/removeitem')
async def removeitem(email: EmailStr, isbn: str):
    remove = await remove_item_from_cart(email, isbn)