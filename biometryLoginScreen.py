import requests
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import user_data
from kivy.clock import Clock

Builder.load_file('biometry_login_screen.kv')

class BiometryLoginScreen(Screen):

    def show_message(self, message):
        self.ids.status_label.text = message

    def change_screen(self, screen):
        self.manager.current = screen
        self.show_message("")  # Limpar a mensagem ao mudar de tela

    def fingerprint_login(self):
        self.show_message("Posicione o dedo sobre o leitor...")
        Clock.unschedule(self.send_fingerprint_request)  # Cancelar qualquer agendamento anterior
        Clock.schedule_once(self.send_fingerprint_request, 0.1)

    def handle_login_response(self, dt, response):
        try:
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    # Handle successful login
                    print(data['message'])
                    # Extract the username from the message
                    user_message = data['message']
                    username = user_message.split()[-1]  # Assume the username is the last word in the message
                    
                    # Get user balance
                    balance_response = requests.post(f'{user_data.get_server_url()}/get_balance', json={"username": username})
                    if balance_response.status_code == 200:
                        balance_data = balance_response.json()
                        user_data.update_current_user_balance(balance_data['balance'])
                    
                    self.show_message(f"Login bem sucedido! Bem vindo {username}!")
                    # Update the current user
                    user_data.update_current_user(username)
                    Clock.schedule_once(lambda dt: self.change_screen('mainMenu'), 1)
                    Clock.schedule_once(lambda dt: self.show_message(""), 1)
                    return
            # Handle login failure
            print('Login failed')
            self.show_message("Login falhou! Biometria incorreta ou não cadastrada")
            Clock.schedule_once(lambda dt: self.show_message("Toque no botão abaixo e tente novamente"), 2)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def send_fingerprint_request(self, dt):
        try:
            response = requests.post(f'{user_data.get_server_url()}/fingerprint_login')
            Clock.schedule_once(lambda dt: self.handle_login_response(dt, response))
        except Exception as e:
            print(f"An error occurred: {e}")
            self.show_message("Ocorreu um erro ao tentar fazer login")

