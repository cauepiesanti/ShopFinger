from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

#importing classes

from startScreen import StartScreen
from biometryLoginScreen import BiometryLoginScreen
from loginScreen import LoginScreen
from registerBiometryScreen import RegisterBiometryScreen
from mainMenuScreen import MainMenuScreen  
from shoppingCartScreen import ShoppingCartScreen
from waitingScreen import WaitingScreen


class MyApp(App):
    def build(self):
        sm =ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(BiometryLoginScreen(name='biometry_login'))
        sm.add_widget(LoginScreen(name ='login'))
        sm.add_widget(RegisterBiometryScreen(name='register_biometry'))
        sm.add_widget(MainMenuScreen(name='mainMenu'))
        sm.add_widget(ShoppingCartScreen(name='shopping_cart'))
        #sm.add_widget(WaitingScreen(name='waitingScreen'))
        
        return sm

if __name__ == '__main__':
    MyApp().run()
