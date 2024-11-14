import os  # Importa o módulo os para interagir com o sistema operacional.
from kivymd.app import MDApp  # Importa a classe MDApp do KivyMD para criar o aplicativo.
from kaki.app import App  # Importa a classe App da biblioteca Kaki para gerenciamento de aplicativos.
from kivy.factory import Factory  # Importa a Factory para instanciar widgets a partir de arquivos .kv.
from kivy.core.window import Window  # Importa o Window para manipular a janela do aplicativo.
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horas.

class LiveApp(MDApp, App):
    # Define a classe LiveApp que herda de MDApp e App.
    DEBUG = 1  # Define o modo de depuração como ativo.
    
    logged_in_user = None  # Atributo para armazenar o usuário logado

    # Define os arquivos .kv a serem monitorados para mudanças.
    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login_screen/loginscreen.kv"),
        os.path.join(os.getcwd(), "screens/form_screen/form.kv")
    }

    # Define as classes a serem monitoradas nos arquivos .py.
    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "LoginScreen": "screens.login_screen.loginscreen",
        "Form": "screens.form_screen.form",
    }

    # Define os caminhos a serem monitorados para reloading automático.
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self, **kwargs):
        if LiveApp.logged_in_user:  # Verifica se há um usuário logado
            return Factory.Form()  # Se sim, inicia diretamente na tela Form
        return Factory.MainScreenManager()  # Caso contrário, inicia na tela de l
    
#Executa o aplicativo.
if __name__ == "__main__":
    LiveApp().run()  # Cria uma instância de LiveApp e executa o aplicativo.