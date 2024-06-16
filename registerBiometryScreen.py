from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import requests
import user_data
from kivy.clock import Clock  # Importe o Clock

# Carregar o arquivo KV
Builder.load_file('register_biometry_screen.kv')

class RegisterBiometryScreen(Screen):

    def change_screen(self,screen):
        self.manager.current = screen

    def show_message(self, message):
        self.ids.status_label.text = message

    def register_fingerprint(self):
        print("Entrou na função register_fingerprint")
        username = user_data.get_current_user()
        print("Usuário atual:", username)
        if not username:
            self.show_message("Usuário não autenticado.")
            return
        else:
            print("Entrou no else")
            self.show_message("Coloque o dedo no sensor por 1 segundo e, em seguida, coloque novamente...")  # Mostra a mensagem antes da solicitação
            Clock.schedule_once(self.send_fingerprint_request, 0.1)  # Agende a solicitação após um pequeno atraso

    def send_fingerprint_request(self, dt):
        # Fazer a solicitação após um pequeno atraso
        username = user_data.get_current_user()
        response = requests.post(f"{user_data.get_server_url()}/register_fingerprint", json={"username": username})
        print("Resposta da solicitação:", response.text)

        if response.status_code == 201:
            self.show_message("Biometria registrada com sucesso!")
            Clock.schedule_once(lambda dt: self.change_screen('start'), 2)
        elif response.status_code == 404:
            self.show_message("Usuário não encontrado.")
        elif response.status_code == 409:
            self.show_message("Usuário já possui uma biometria registrada.")
        else:
            self.show_message("Erro ao registrar a biometria.")
