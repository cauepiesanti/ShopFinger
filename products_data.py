import requests
import user_data

server_url = user_data.get_server_url()

# Informações sobre os produtos, inicializando vazios
products = [
    {
        'name': '',
        'price': 0,
        'stock': 0
    },
    {
        'name': '',
        'price': 0,
        'stock': 0
    },
    {
        'name': '',
        'price': 0,
        'stock': 0
    },
    {
        'name': '',
        'price': 0,
        'stock': 0
    }
]

shopping_cart = [
    {
        'name': '',
        'price': 0,
        'amount': 0
    },
    {
        'name': '',
        'price': 0,
        'amount': 0
    },
    {
        'name': '',
        'price': 0,
        'amount': 0
    },
    {
        'name': '',
        'price': 0,
        'amount': 0
    }
]

def update_products_data():
    response = requests.get(f"{server_url}/list_products")
    if response.status_code == 200:
        product_list = response.json()
        for i, product in enumerate(product_list):
            if i < len(products):  # Garantir que não vamos tentar acessar um índice fora do range
                products[i]['name'] = product[1]
                products[i]['price'] = product[2]
                products[i]['stock'] = product[3]

# Função para obter o nome do produto
def get_product_name(product_index):
    if 0 <= product_index < len(products):
        return products[product_index]['name']
    return "Produto não encontrado."

# Função para obter o preço do produto
def get_product_price(product_index):
    if 0 <= product_index < len(products):
        return products[product_index]['price']
    return "Produto não encontrado."

# Função para obter o estoque do produto
def get_product_stock(product_index):
    if 0 <= product_index < len(products):
        return products[product_index]['stock']
    return "Produto não encontrado."

# Função para obter o nome do produto do carrinho
def get_shoppingCart_product_name(product_index):
    if 0 <= product_index < len(shopping_cart):
        return shopping_cart[product_index]['name']
    return "Produto não encontrado."

# Função para obter o preço do produto do carrinho
def get_shoppingCart_product_price(product_index):
    if 0 <= product_index < len(shopping_cart):
        return shopping_cart[product_index]['price']
    return "Produto não encontrado."

# Função para obter o estoque do produto do carrinho
def get_shoppingCart_product_amount(product_index):
    if 0 <= product_index < len(shopping_cart):
        return shopping_cart[product_index]['amount']
    return "Produto não encontrado."

# Função para setar o nome do produto do carrinho
def set_shoppingCart_product_name(product_index,product_name):
    if 0 <= product_index < len(shopping_cart):
        shopping_cart[product_index]['name'] = product_name

# Função para setar o preço do produto do carrinho
def set_shoppingCart_product_price(product_index,product_price):
    if 0 <= product_index < len(shopping_cart):
        shopping_cart[product_index]['price'] = product_price

# Função para setar o estoque do produto do carrinho
def set_shoppingCart_product_amount(product_index,product_amount):
    if 0 <= product_index < len(shopping_cart):
        shopping_cart[product_index]['amount'] = product_amount

def update_balance():
    username = user_data.get_current_user()

    product_1_cost = get_product_price(0) * get_shoppingCart_product_amount(0)
    product_2_cost = get_product_price(1) * get_shoppingCart_product_amount(1)
    product_3_cost = get_product_price(2) * get_shoppingCart_product_amount(2)
    product_4_cost = get_product_price(3) * get_shoppingCart_product_amount(3)

    total_cost = product_1_cost + product_2_cost + product_3_cost + product_4_cost

    new_balance = user_data.get_current_user_balance() - total_cost 
    
    if(total_cost>0):
        if(new_balance >= 0):

            #requisição para atualizar o saldo
            try:
                print(f"Atualizando saldo para usuário: {username} com novo saldo: {new_balance}")
                #response = requests.post('http://192.168.0.23:5000/update_balance', json={'username': username, 'new_balance': new_balance})
                response = requests.post(f'{server_url}/update_balance', json={'username': username, 'new_balance': new_balance})
                if response.status_code == 200:
                    print('Saldo atualizado no banco de dados com sucesso.')
                    return ('balance_valid')
                else:
                    print(f'Erro ao atualizar saldo no banco de dados. Status code: {response.status_code}')
                    return ('update_balance_error')
            except Exception as e:
                print(f'Erro ao conectar ao servidor: {e}')
                return ('server_error')

        else:
            return (f'Deposite ${-new_balance}')
    else:
        return('empty_cart')
    
def update_stock():
    product_1_stock = get_product_stock(0) - get_shoppingCart_product_amount(0)
    product_2_stock = get_product_stock(1) - get_shoppingCart_product_amount(1)
    product_3_stock = get_product_stock(2) - get_shoppingCart_product_amount(2)
    product_4_stock = get_product_stock(3) - get_shoppingCart_product_amount(3)

    product_1_name = get_product_name(0)
    product_2_name = get_product_name(1)
    product_3_name = get_product_name(2)
    product_4_name = get_product_name(3)

    if product_1_stock >= 0 and product_2_stock >= 0 and product_3_stock >=0 and product_4_stock>= 0:
        # Se o estoque for válido para todos os produtos
        try:
            print("Atualizando estoque no banco de dados...")
            response = requests.post(f'{server_url}/update_product_stock', json={'name': product_1_name,
                                                                                  'stock': product_1_stock})
            if response.status_code == 200:
                print(f'Estoque de {product_1_name} atualizado com sucesso.')
            else:
                print(f'Erro ao atualizar estoque de {product_1_name}. Status code: {response.status_code}')

            response = requests.post(f'{server_url}/update_product_stock', json={'name': product_2_name,
                                                                                  'stock': product_2_stock})
            if response.status_code == 200:
                print(f'Estoque de {product_2_name} atualizado com sucesso.')
            else:
                print(f'Erro ao atualizar estoque de {product_2_name}. Status code: {response.status_code}')

            response = requests.post(f'{server_url}/update_product_stock', json={'name': product_3_name,
                                                                                  'stock': product_3_stock})
            if response.status_code == 200:
                print(f'Estoque de {product_3_name} atualizado com sucesso.')
            else:
                print(f'Erro ao atualizar estoque de {product_3_name}. Status code: {response.status_code}')

            response = requests.post(f'{server_url}/update_product_stock', json={'name': product_4_name,
                                                                                  'stock': product_4_stock})
            if response.status_code == 200:
                print(f'Estoque de {product_4_name} atualizado com sucesso.')
            else:
                print(f'Erro ao atualizar estoque de {product_4_name}. Status code: {response.status_code}')

        except Exception as e:
            print(f'Erro ao conectar ao servidor: {e}')
            return 'server_error'
        
        return 'stock_valid'
    else:
        stock_string = ''
        if product_1_stock < 0:
            stock_string += f'{product_1_name}/{get_product_stock(0)}    '
        if product_2_stock < 0:
            stock_string += f'{product_2_name}/{get_product_stock(1)}    '
        if product_3_stock < 0:
            stock_string += f'{product_3_name}/{get_product_stock(2)}    '
        if product_4_stock < 0:
            stock_string += f'{product_4_name}/{get_product_stock(3)}'

        return stock_string


        

# Atualizar informações dos produtos ao iniciar
#update_products_data()
