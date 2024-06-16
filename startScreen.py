from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder
import requests
import user_data
import products_data

Builder.load_file('start_screen.kv')

class StartScreen(Screen):

    #Atualiza nome,preço e estoque de acordo com o banco de dados
    def on_enter(self):
        products_data.update_products_data()
    
    def change_screen(self,screen):
        self.manager.current = screen

    def login_caueps(self):
        username = 'caueps'
        user_data.update_current_user(username)
        # Get user balance
        balance_response = requests.post(f'{user_data.get_server_url()}/get_balance', json={"username": username})
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            user_data.update_current_user_balance(balance_data['balance'])
        self.change_screen('mainMenu')