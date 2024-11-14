from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import sqlite3

class LoginScreen(MDScreen):  # Define a classe LoginScreen que herda de MDScreen.
    dialog = None  # 'dialog' é um atributo da classe que inicialmente é None e será usado para armazenar o diálogo de erro.

    user = "renan.ramos"
    passw = "bjnubin8"
    
    is_logged_in = False  # Novo atributo para armazenar o estado de login
    
    def verificar_login(self):  # Método para verificar as credenciais de login.
        username = self.ids.username.text.strip()  # Obtém o texto do campo de usuário e remove espaços extras.
        password = self.ids.password.text.strip()  # Obtém o texto do campo de senha e remove espaços extras.

        if username == self.user and password == self.passw:  # Se a consulta retornar um resultado (ou seja, um usuário com essas credenciais foi encontrado):
            self.is_logged_in = True  # Define que o usuário está logado
            self.manager.get_screen('Form').set_username(username)  # Passa o nome de usuário para a tela 'Form' chamando o método 'set_username'.
            self.manager.current = 'Form'  # Navega para a tela 'Form', que é a tela principal após o login.
        else:
            self.exibir_erro_login()  # Se não houver um usuário com essas credenciais, exibe o diálogo de erro.


    def exibir_erro_login(self):  # Método para exibir um diálogo de erro de login.
        if not self.dialog:  # Se o diálogo ainda não foi criado:
            self.dialog = MDDialog(  # Cria um novo diálogo.
                text="Credenciais inválidas. Tente novamente.",  # Define o texto do diálogo.
                buttons=[  # Adiciona botões ao diálogo.
                    MDRaisedButton(  # Cria um botão "OK" elevado.
                        text="OK",  # Define o texto do botão.
                        on_release=self.fechar_dialog,  # Define a ação para fechar o diálogo quando o botão for pressionado.
                    ),
                ],
            )
        self.dialog.open()  # Abre o diálogo.

    def fechar_dialog(self, instance):  # Método para fechar o diálogo.
        self.dialog.dismiss()  # Fecha o diálogo quando o botão "OK" é pressionado.