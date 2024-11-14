from kivy.uix.screenmanager import ScreenManager    # Importa a classe ScreenManager do módulo kivy.uix.screenmanager.
# ScreenManager é responsável por gerenciar diferentes telas em um aplicativo Kivy.

sm = ScreenManager()    # Cria uma instância de ScreenManager e a armazena na variável 'sm'.
# Isso configura o gerenciador de telas que pode ser usado para alternar entre diferentes telas.

class MainScreenManager(ScreenManager):    # Define uma classe chamada MainScreenManager que herda de ScreenManager.
    
    def on_pre_switch(self, *args):
        # Impede a navegação de volta para a tela de login se o usuário estiver logado
        if self.current == 'LoginScreen' and self.get_screen('LoginScreen').is_logged_in:
            self.current = 'Form'  # Redireciona para a tela Form se já estiver logado