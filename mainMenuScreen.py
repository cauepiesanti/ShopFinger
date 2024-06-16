from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import user_data
import products_data

Builder.load_file('main_menu_screen.kv')

class MainMenuScreen(Screen):   

    def on_enter(self):
        self.init_balance()
        self.init_table()
        # Atualizar o estoque a cada 5 segundos
        #Clock.schedule_interval(self.update_table,5)

    def init_table(self):
        self.update_all_names()
        self.update_all_quantities()
        self.update_all_prices()

    def update_table(self,dt):
        products_data.update_products_data()

    def change_screen(self, screen_name):
        self.manager.current = screen_name
    
    def increment_qtd(self, produto_id):
        quantidade_id = f'qtd_produto_{produto_id}'
        quantidade_input = self.ids[quantidade_id]
        quantidade = int(quantidade_input.text) + 1
        quantidade_input.text = str(quantidade)
        self.update_price(produto_id,quantidade)

    def decrement_qtd(self, produto_id):
        quantidade_id = f'qtd_produto_{produto_id}'
        quantidade_input = self.ids[quantidade_id]
        quantidade = int(quantidade_input.text)
        if quantidade > 0:
            quantidade -= 1
        quantidade_input.text = str(quantidade)
        self.update_price(produto_id,quantidade)

    def update_price(self,produto_id,quantidade):
        preco_id = f'preco_produto_{produto_id}'
        preco = float(self.ids[preco_id].text)
        preco_total_id = f'preco_total_produto_{produto_id}'
        self.ids[preco_total_id].text = str(quantidade*preco)


    def reset_text(self, dt):
        self.change_screen('shopping_cart')
        self.ids.add_to_cart_button.text = "Atualizar carrinho"
        self.update_status_message('')

    def change_text(self,text):
        self.update_status_message(text)
        Clock.schedule_once(self.reset_text, 2)

    def update_balance(self, new_balance):
        self.ids.balance_button.text = f'Saldo: ${new_balance:.2f}'

    def init_balance(self):
        balance = user_data.get_current_user_balance()
        self.ids.balance_button.text = f'Saldo: ${balance:.2f}'

    def update_shopping_cart(self):
        # Atualizar o produto 1
        nome_produto_1 = self.ids.nome_produto_1.text
        preco_produto_1 = float(self.ids.preco_produto_1.text)
        qtd_produto_1 = int(self.ids.qtd_produto_1.text)
        products_data.set_shoppingCart_product_name(0, nome_produto_1)
        products_data.set_shoppingCart_product_price(0, preco_produto_1)
        products_data.set_shoppingCart_product_amount(0, qtd_produto_1)

        # Atualizar o produto 2
        nome_produto_2 = self.ids.nome_produto_2.text
        preco_produto_2 = float(self.ids.preco_produto_2.text)
        qtd_produto_2 = int(self.ids.qtd_produto_2.text)
        products_data.set_shoppingCart_product_name(1, nome_produto_2)
        products_data.set_shoppingCart_product_price(1, preco_produto_2)
        products_data.set_shoppingCart_product_amount(1, qtd_produto_2)

        # Atualizar o produto 3
        nome_produto_3 = self.ids.nome_produto_3.text
        preco_produto_3 = float(self.ids.preco_produto_3.text)
        qtd_produto_3 = int(self.ids.qtd_produto_3.text)
        products_data.set_shoppingCart_product_name(2, nome_produto_3)
        products_data.set_shoppingCart_product_price(2, preco_produto_3)
        products_data.set_shoppingCart_product_amount(2, qtd_produto_3)


    def clear_shopping_cart(self):
        self.ids['qtd_produto_1'].text = str(0)
        self.ids['qtd_produto_2'].text = str(0)
        self.ids['qtd_produto_3'].text = str(0)

        self.ids['preco_total_produto_1'].text = str(0)
        self.ids['preco_total_produto_2'].text = str(0)
        self.ids['preco_total_produto_3'].text = str(0)

        self.update_shopping_cart()

        self.update_status_message("Itens do carrinho removidos!")
        self.ids.add_to_cart_button.text = 'Adicionar ao carrinho'
        Clock.schedule_once(lambda dt: self.update_status_message('') , 2)

    def update_all_names(self):
        self.ids.nome_produto_1.text = products_data.get_product_name(0)
        self.ids.nome_produto_2.text = products_data.get_product_name(1)
        self.ids.nome_produto_3.text = products_data.get_product_name(2)

    def update_all_prices(self):
        self.ids.preco_produto_1.text = str(products_data.get_product_price(0))
        self.ids.preco_produto_2.text = str(products_data.get_product_price(1))
        self.ids.preco_produto_3.text = str(products_data.get_product_price(2))

    def update_all_quantities(self):
        self.ids.qtd_produto_1.text = str(products_data.get_shoppingCart_product_amount(0))
        self.ids.qtd_produto_2.text = str(products_data.get_shoppingCart_product_amount(1))
        self.ids.qtd_produto_3.text = str(products_data.get_shoppingCart_product_amount(2))

    def verify_empty_cart(self):
        qtd_1 = int(self.ids.qtd_produto_1.text)
        qtd_2 = int(self.ids.qtd_produto_2.text)
        qtd_3 = int(self.ids.qtd_produto_3.text)
        if(qtd_1 == 0 and qtd_2 == 0 and qtd_3 == 0):
            return ('empty_cart')
        else:
            return ('not_empty_cart')
        
    def add_to_cart(self):
        self.update_shopping_cart()
        empty_cart = self.verify_empty_cart()
        if(empty_cart == 'not_empty_cart'):
            self.change_text('Itens adicionados ao carrinho!')
        else:
            self.update_status_message('Não é possível adicionar 0 itens ao carrinho!')
            Clock.schedule_once(lambda dt: self.update_status_message(''),2)
    def update_status_message(self,message):
        self.ids.status_message.text = message



        

