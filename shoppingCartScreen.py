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
        self.init_balance()
        Clock.schedule_interval(self.update_balance,5)

    def update_buy_list(self):
        self.ids.nome_produto_1.text = products_data.get_shoppingCart_product_name(0)
        self.ids.nome_produto_2.text = products_data.get_shoppingCart_product_name(1)
        self.ids.nome_produto_3.text = products_data.get_shoppingCart_product_name(2)
        self.ids.nome_produto_4.text = products_data.get_shoppingCart_product_name(3)

        self.ids.qtd_produto_1.text = str(products_data.get_shoppingCart_product_amount(0))
        self.ids.qtd_produto_2.text = str(products_data.get_shoppingCart_product_amount(1))
        self.ids.qtd_produto_3.text = str(products_data.get_shoppingCart_product_amount(2))
        self.ids.qtd_produto_4.text = str(products_data.get_shoppingCart_product_amount(3))

        self.ids.preco_produto_1.text = "{:.2f}".format(products_data.get_shoppingCart_product_price(0))
        self.ids.preco_produto_2.text = "{:.2f}".format(products_data.get_shoppingCart_product_price(1))
        self.ids.preco_produto_3.text = "{:.2f}".format(products_data.get_shoppingCart_product_price(2))
        self.ids.preco_produto_4.text = "{:.2f}".format(products_data.get_shoppingCart_product_price(3))

        product_1_total_price = products_data.get_shoppingCart_product_amount(0) * products_data.get_shoppingCart_product_price(0)
        product_2_total_price = products_data.get_shoppingCart_product_amount(1) * products_data.get_shoppingCart_product_price(1)
        product_3_total_price = products_data.get_shoppingCart_product_amount(2) * products_data.get_shoppingCart_product_price(2)
        product_4_total_price = products_data.get_shoppingCart_product_amount(3) * products_data.get_shoppingCart_product_price(3)

        self.ids.preco_total_produto_1.text = "{:.2f}".format(product_1_total_price)
        self.ids.preco_total_produto_2.text = "{:.2f}".format(product_2_total_price)
        self.ids.preco_total_produto_3.text = "{:.2f}".format(product_3_total_price)
        self.ids.preco_total_produto_4.text = "{:.2f}".format(product_4_total_price)

        self.ids.preco_total.text = "{:.2f}".format(product_1_total_price+product_2_total_price+product_3_total_price+product_4_total_price)

        current_balance = user_data.get_current_user_balance()

        self.ids.future_balance.text = 'Saldo após a compra: $ '+"{:.2f}".format(current_balance - (product_1_total_price+product_2_total_price+product_3_total_price+product_4_total_price))

        product_1_amount = products_data.get_shoppingCart_product_amount(0)
        product_2_amount = products_data.get_shoppingCart_product_amount(1)
        product_3_amount = products_data.get_shoppingCart_product_amount(2)
        product_4_amount = products_data.get_shoppingCart_product_amount(3)

        products = [
            (product_1_amount, self.ids.product_1_row),
            (product_2_amount, self.ids.product_2_row),
            (product_3_amount, self.ids.product_3_row),
            (product_4_amount, self.ids.product_4_row)
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
        products_data.set_shoppingCart_product_amount(3, 0)

        self.update_buy_list()

        mainMenu = self.manager.get_screen('mainMenu')
        mainMenu.ids['preco_total_produto_1'].text = "{:.2f}".format(0)
        mainMenu.ids['preco_total_produto_2'].text = "{:.2f}".format(0)
        mainMenu.ids['preco_total_produto_3'].text = "{:.2f}".format(0)
        mainMenu.ids['preco_total_produto_4'].text = "{:.2f}".format(0)

        mainMenu.ids['qtd_produto_1'].text = str(0)
        mainMenu.ids['qtd_produto_2'].text = str(0)
        mainMenu.ids['qtd_produto_3'].text = str(0)
        mainMenu.ids['qtd_produto_4'].text = str(0)

        mainMenu.ids.add_to_cart_button.text = 'Adicionar ao carrinho'
        self.update_status_label("Itens do carrinho removidos!")
        Clock.schedule_once(lambda dt: self.update_status_label('') , 2)
        mainMenu.update_shopping_cart()

    def update_balance(self,dt):
        user_data.update_user_balance_from_db()
        self.init_balance()

    def init_balance(self):
        balance = user_data.get_current_user_balance()
        self.ids.balance_button.text = f'Saldo: ${balance:.2f}'


    def confirm_purchase(self):
        
        #REFAZER A LÓGICA: ESTÁ ATUALIZANDO O SALDO QUANDO NÃO TEM ESTOQUE E ATUALIZANDO O ESTOQUE QUANDO NÃO TEM SALDO
        
        #Atualizando o estoque antes de confirmar a compra
        products_data.update_products_data()

        product_1_name = products_data.get_product_name(0)
        product_2_name = products_data.get_product_name(1)
        product_3_name = products_data.get_product_name(2)
        product_4_name = products_data.get_product_name(3)

        product_1_stock = products_data.get_product_stock(0) - products_data.get_shoppingCart_product_amount(0)
        product_2_stock = products_data.get_product_stock(1) - products_data.get_shoppingCart_product_amount(1)
        product_3_stock = products_data.get_product_stock(2) - products_data.get_shoppingCart_product_amount(2)
        product_4_stock = products_data.get_product_stock(3) - products_data.get_shoppingCart_product_amount(3)

        product_1_cost = products_data.get_product_price(0) * products_data.get_shoppingCart_product_amount(0)
        product_2_cost = products_data.get_product_price(1) * products_data.get_shoppingCart_product_amount(1)
        product_3_cost = products_data.get_product_price(2) * products_data.get_shoppingCart_product_amount(2)
        product_4_cost = products_data.get_product_price(3) * products_data.get_shoppingCart_product_amount(3)

        total_cost = product_1_cost + product_2_cost + product_3_cost + product_4_cost

        new_balance = user_data.get_current_user_balance() - total_cost

        stock_string = ''
        if product_1_stock < 0:
            stock_string += f'{product_1_name}/{products_data.get_product_stock(0)}    '
        if product_2_stock < 0:
            stock_string += f'{product_2_name}/{products_data.get_product_stock(1)}    '
        if product_3_stock < 0:
            stock_string += f'{product_3_name}/{products_data.get_product_stock(2)}     '
        if product_4_stock < 0:
            stock_string += f'{product_4_name}/{products_data.get_product_stock(3)}'

        #Se tem estoque
        if(product_1_stock >= 0 and product_2_stock >= 0 and product_3_stock >= 0 and product_4_stock >=0):
            #carrinho não vazio e tem saldo
            if(total_cost>0 and new_balance>=0):
                self.ids.status_label.text = 'Compra bem sucedida!'
                self.activate_motors()
                self.print_receipt()
                self.print_ru()
                products_data.update_stock()
                products_data.update_balance()
                self.clear_shopping_cart()
                Clock.schedule_once(lambda dt: self.change_screen('start'),3)
            #carrinho vazio e tem saldo
            elif(total_cost == 0 and new_balance>=0):
                self.ids.status_label.text = 'Adicione algo ao carrinho!'
            #carrinho não vazio e não tem saldo
            elif(total_cost > 0 and new_balance <0):
                self.ids.status_label.text = f'Deposite ${-new_balance}'
            #carrinho vazio e não tem saldo
            elif(total_cost == 0 and new_balance <0):
                self.ids.status_label.text = f'Adicione saldo e adicione algo ao carrinho!'
        # Se não tem estoque
        else:
            if(new_balance >= 0):
                self.ids.status_label.text = f'Estoque insufuciente! {stock_string}'
            else:
                self.ids.status_label.text = f'Saldo insuficiente! Deposite ${-new_balance}.\nEstoque insuficiente! {stock_string}'
            
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

        product_1_qtd = products_data.get_shoppingCart_product_amount(0)
        product_2_qtd = products_data.get_shoppingCart_product_amount(1)
        product_3_qtd = products_data.get_shoppingCart_product_amount(2)
        product_4_qtd = products_data.get_shoppingCart_product_amount(3)

        product_1_name = products_data.get_shoppingCart_product_name(0)
        product_2_name = products_data.get_shoppingCart_product_name(1)
        product_3_name = products_data.get_shoppingCart_product_name(2)
        product_4_name = products_data.get_shoppingCart_product_name(3)


        product_1_cost = products_data.get_product_price(0) * products_data.get_shoppingCart_product_amount(0)
        product_2_cost = products_data.get_product_price(1) * products_data.get_shoppingCart_product_amount(1)
        product_3_cost = products_data.get_product_price(2) * products_data.get_shoppingCart_product_amount(2)
        product_4_cost = products_data.get_product_price(3) * products_data.get_shoppingCart_product_amount(3)

        total_cost = product_1_cost + product_2_cost + product_3_cost + product_4_cost

        new_balance = user_data.get_current_user_balance() - total_cost

        myString =f'Comprovante de compra:\n\nUsuario: {user_data.get_current_user()}\n\n'

        if(product_1_qtd>0):
            myString += f'{product_1_qtd}X {product_1_name}\n'
        if(product_2_qtd>0):
            myString += f'{product_2_qtd}X {product_2_name}\n'
        if(product_3_qtd>0):
            myString += f'{product_3_qtd}X {product_3_name}\n'
        if(product_4_qtd>0):
            myString += f'{product_4_qtd}X {product_4_name}\n'

        myString+=f'\nValor total: {total_cost:.2f}\n'
        myString+=f'\nNovo Saldo: {new_balance:.2f}\n'
        myString+='--------------------------------'
        myString+='\n\n\n\n\n'

        url = f'{user_data.get_server_url()}/print_receipt'
        data = {'print_string': myString}

        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print('Receipt printed successfully')
        else:
            print(f'Failed to print receipt: {response.json()}')

        print(f'\n{myString}\n')

    def print_ru(self):

        qtd_ru = products_data.get_shoppingCart_product_amount(3)

        if(qtd_ru>0):
            qtd_ticket_ru = products_data.get_shoppingCart_product_amount(3)
            myString = f"{qtd_ticket_ru}X Ticket refeicao RU\n"
            myString+='--------------------------------'
            myString+='\n\n\n\n\n'

            url = f'{user_data.get_server_url()}/print_receipt'
            data = {'print_string': myString}

            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                print('Receipt printed successfully')
            else:
                print(f'Failed to print receipt: {response.json()}')
            
            print(f'{myString}\n')


    def ativar_motor(self, id):
        url = f'{user_data.get_server_url()}/activate_motor'
        data = {'id': id}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f'Motor {id} activated successfully')
        else:
            print(f'Failed to activate motor: {response.json()}')




        
