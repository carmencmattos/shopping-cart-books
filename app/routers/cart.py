from fastapi import APIRouter, status
from pydantic.networks import EmailStr
from app.controllers.cart import add_product_cart, calculate_cart, create_cart_by_email, closed_cart_by_email, drop_cart_by_email, get_cart_by_email, get_closed_cart_by_email, remove_item_from_cart, update_product_cart
from app.controllers.inventory import get_inventory_by_isbn
from app.controllers.user import get_user_by_email
from app.schemas.cart import CartListSchema
from app.utils import serialize
from starlette.responses import JSONResponse

router = APIRouter(tags=['Cart'], prefix='/cart')


@router.post('/{email}/create')
async def create_cart(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        cart_opened = await get_cart_by_email(email)
        if cart_opened:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Ja existe um carrinho vinculado a este usuario'})
        create = await create_cart_by_email(email)
        if create:
            cart = serialize.cart(create)
            return JSONResponse(status_code=status.HTTP_200_OK, content=cart)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistente'})


@router.post('/{email}/additem')
async def additem(email: EmailStr, item: CartListSchema):
    user = await get_user_by_email(email)
    if user:
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
                            return_object = {'cart': serialize.cart(
                                calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total']}
                            return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)

                    # Se NÃO tiver encontrado algum produto no carrinho igual ao do usuário
                    else:

                        # ADICIONA o produto enviado pelo usuário no carrinho
                        add_product_in_cart = await add_product_cart(email, item.dict())

                        # Se adicionou o produto com sucesso
                        if add_product_in_cart:

                            calculate = await calculate_cart(add_product_in_cart)

                            # Retorna o carrinho atualizado e serializado
                            return_object = {'cart': serialize.cart(
                                calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total']}
                            return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)

                # Se não tiver carrinho aberto para o usuário
                else:

                    # Cria um carrinho aberto com o produto que o usuário enviou
                    create = await create_cart(email, item)

                    # Se criou o carrinho aberto com o produto adicionado com suceeeo
                    if create:
                        calculate = await calculate_cart(create)
                        return_object = {'cart': serialize.cart(
                            calculate['data_cart']), 'payments': calculate['total_info'], 'total_cart': calculate['total']}
                        return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Este produto ultrapassa o limite do estoque.'})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'O produto enviado não existe no estoque'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistente'})


@router.patch('/{email}/removeitem/{isbn}')
async def removeitem(email: EmailStr, isbn: str):
    user = get_user_by_email(email)
    if user:
        cart = await get_cart_by_email(email)
        if cart:
            remove = await remove_item_from_cart(email, isbn)
            if remove:
                return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Item removido do carrinho com sucesso'})
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'O produto enviado não existe no carrinho'})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Usuário ou Carrinho inexistente'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistente'})


@router.get('/{email}')
async def get_cart(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        get_cart = await get_cart_by_email(email)
        if get_cart:
            cart = await calculate_cart(get_cart)
            return_object = {'cart': serialize.cart(
                cart['data_cart']), 'payments': cart['total_info'], 'total_cart': cart['total']}
            return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email ou Carrinho inexistentes'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistentes'})


@router.get('/{email}/closed')
async def get_cart(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        get_cart = await get_closed_cart_by_email(email)
        if get_cart:
            cart = await calculate_cart(get_cart)
            return_object = {'cart': serialize.cart(
                cart['data_cart']), 'payments': cart['total_info'], 'total_cart': cart['total']}
            return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email ou Carrinho inexistentes'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistente'})


@router.patch('/{email}')
async def close_cart(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        get_cart = await get_cart_by_email(email)
        if get_cart:
            close_cart = await closed_cart_by_email(get_cart)
            if close_cart:
                cart = await calculate_cart(get_cart)
                return_object = {'cart': serialize.cart(
                    cart['data_cart']), 'payments': cart['total_info'], 'total_cart': cart['total']}
                return JSONResponse(status_code=status.HTTP_200_OK, content=return_object)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email ou Carrinho inexistentes'})


@router.delete('/{email}/drop')
async def drop_cart(email: EmailStr):
    user = await get_user_by_email(email)
    if user:
        drop = await drop_cart_by_email(email)
        if drop:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Carrinho excluído com sucesso'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Email inexistente'})
