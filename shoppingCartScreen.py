from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import user_data
import products_data
import requests

Builder.load_file('shopping_cart_screen.kv')

class ShoppingCartScreen(Screen):

    def on_enter(self):
        self.update_buy_list()

    def update_buy_list(self):
        self.ids.nome_produto_1.text = products_data.get_shoppingCart_product_name(0)
        self.ids.nome_produto_2.text = products_data.get_shoppingCart_product_name(1)
        self.ids.nome_produto_3.text = products_data.get_shoppingCart_product_name(2)

        self.ids.qtd_produto_1.text = str(products_data.get_shoppingCart_product_amount(0))
        self.ids.qtd_produto_2.text = str(products_data.get_shoppingCart_product_amount(1))
        self.ids.qtd_produto_3.text = str(products_data.get_shoppingCart_product_amount(2))

        self.ids.preco_produto_1.text = str(products_data.get_shoppingCart_product_price(0))
        self.ids.preco_produto_2.text = str(products_data.get_shoppingCart_product_price(1))
        self.ids.preco_produto_3.text = str(products_data.get_shoppingCart_product_price(2))

        product_1_total_price = products_data.get_shoppingCart_product_amount(0) * products_data.get_shoppingCart_product_price(0)
        product_2_total_price = products_data.get_shoppingCart_product_amount(1) * products_data.get_shoppingCart_product_price(1)
        product_3_total_price = products_data.get_shoppingCart_product_amount(2) * products_data.get_shoppingCart_product_price(2)

        self.ids.preco_total_produto_1.text = str(product_1_total_price)
        self.ids.preco_total_produto_2.text = str(product_2_total_price)
        self.ids.preco_total_produto_3.text = str(product_3_total_price)

        self.ids.preco_total.text = str(product_1_total_price+product_2_total_price+product_3_total_price)

        product_1_amount = products_data.get_shoppingCart_product_amount(0)
        product_2_amount = products_data.get_shoppingCart_product_amount(1)
        product_3_amount = products_data.get_shoppingCart_product_amount(2)

        products = [
            (product_1_amount, self.ids.product_1_row),
            (product_2_amount, self.ids.product_2_row),
            (product_3_amount, self.ids.product_3_row)
        ]

        # Reset visibility and positions
        y_position = 0.75  # Starting position from the top

        for amount, product_row in products:
            if amount > 0:
                product_row.opacity = 1
                product_row.size_hint_y = 0.25
                product_row.pos_hint = {'x': 0, 'y': y_position}
                y_position -= 0.25  # Move down for the next product
            else:
                product_row.opacity = 0
                product_row.size_hint_y = None
                product_row.height = 0





    def update_status_label(self,text):
        self.ids.status_label.text = text

    def change_screen(self,screen):
        self.manager.current = screen    
    
    def clear_shopping_cart(self):
        products_data.set_shoppingCart_product_amount(0, 0)
        products_data.set_shoppingCart_product_amount(1, 0)
        products_data.set_shoppingCart_product_amount(2, 0)

        self.update_buy_list()

        mainMenu = self.manager.get_screen('mainMenu')
        mainMenu.ids['preco_total_produto_1'].text = str(0)
        mainMenu.ids['preco_total_produto_2'].text = str(0)
        mainMenu.ids['preco_total_produto_3'].text = str(0)

        mainMenu.ids['qtd_produto_1'].text = str(0)
        mainMenu.ids['qtd_produto_2'].text = str(0)
        mainMenu.ids['qtd_produto_3'].text = str(0)

        mainMenu.ids.add_to_cart_button.text = 'Adicionar ao carrinho'
        mainMenu.update_shopping_cart()


    def confirm_purchase(self):
        
        #REFAZER A LÓGICA: ESTÁ ATUALIZANDO O SALDO QUANDO NÃO TEM ESTOQUE E ATUALIZANDO O ESTOQUE QUANDO NÃO TEM SALDO



        #Atualizando o estoque antes de confirmar a compra
        products_data.update_products_data()
        stock_string = products_data.update_stock()
        stock_valid = 0

        if(stock_string == 'stock_valid'):
            stock_valid = 1
        else:
            prefix = '    Produto/Estoque:    '
            stock_string = prefix + stock_string 

        balance_string = products_data.update_balance()
        balance_valid = 0

        if(balance_string == 'balance_valid'):
            balance_valid = 1
        elif(balance_string == 'update_balance_error'):
            balance_string = 'Erro no banco de dados!'
            balance_valid = -1
        elif(balance_string == 'server_error'):
            balance_string = 'Erro no servidor!'
            balance_valid = -2
        elif(balance_string =='empty_cart'):
            balance_string = 'Carrinho vazio!'
            balance_valid = -3
        else:
            pass
            

        if(stock_valid == 1 and balance_valid == 1):
            self.ids.status_label.text = 'Compra bem sucedida!'
            self.activate_motors()
            self.print_receipt()
            self.clear_shopping_cart()
            Clock.schedule_once(lambda dt: self.change_screen('start'),3)
        elif(stock_valid == 1 and balance_valid == 0):
            self.ids.status_label.text = f'Saldo insuficiente! {balance_string} e tente novamente.' 
        elif(stock_valid == 0 and balance_valid == 1):
            self.ids.status_label.text = f'Estoque insufuciente! {stock_string}'
        elif(stock_valid == 0 and balance_valid == 0):
            self.ids.status_label.text = f'Saldo insuficiente! {balance_string}.\nEstoque insuficiente! {stock_string}'                     
        elif(balance_valid == -1):
            self.ids.status_label.text = balance_string
        elif(balance_valid == -2):
            self.ids.status_label.text = balance_string
        elif(balance_valid == -3):
            self.ids.status_label.text = balance_string

        #Clock.schedule_once(lambda dt: self.change_screen('start'),3)

        Clock.schedule_once(lambda dt: self.update_status_label(''),3)


    def activate_motors(self):
        product_1_qtd = products_data.get_shoppingCart_product_amount(0)
        product_2_qtd = products_data.get_shoppingCart_product_amount(1)
        product_3_qtd = products_data.get_shoppingCart_product_amount(2)

        if(product_1_qtd>0):
            for i in range(product_1_qtd):
                self.ativar_motor(1)
        if(product_2_qtd>0):
            for i in range(product_2_qtd):
                self.ativar_motor(2)
        if(product_3_qtd>0):
            for i in range(product_3_qtd):
                self.ativar_motor(3)

        #self.ativar_motor(1)
        #self.ativar_motor(2)
        #self.ativar_motor(3)
        #self.print_receipt()

    def print_receipt(self):
        url = f'{user_data.get_server_url()}/print_receipt'
        response = requests.post(url)
        
        if response.status_code == 200:
            print('Receipt printed successfully')
        else:
            print(f'Failed to print receipt: {response.json()}')

    def ativar_motor(self, id):
        url = f'{user_data.get_server_url()}/activate_motor'
        data = {'id': id}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print('Motor activated successfully')
        else:
            print(f'Failed to activate motor: {response.json()}')




        
