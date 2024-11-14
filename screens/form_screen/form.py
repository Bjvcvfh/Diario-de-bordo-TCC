from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from jnius import autoclass  # Para usar chamadas de Java
import csv
import os

class Form(MDScreen):  # Define a classe Form que herda de MDScreen.
    dialog = None  # Atributo para armazenar o diálogo, inicialmente definido como None.
    refeicoes_contadas = 0  # Atributo para contar o número de refeições.

    def set_username(self, username):  # Método para definir o nome de usuário.
        self.username = username  # Armazena o nome de usuário na instância.

    def criar_csv(self):
    # Verifica se o arquivo CSV existe; caso contrário, cria com os cabeçalhos corretos.
        if not os.path.exists('marcacoes.csv'):
            with open('marcacoes.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                # Escreve os cabeçalhos.
                writer.writerow([
                    'Dia', 'Primeira_Marcacao', 'Segunda_Marcacao', 
                    'Terceira_Marcacao', 'Quarta_Marcacao', 'Quinta_Marcacao', 
                    'Sexta_Marcacao', 'Refeicoes', 'Usuario'
                ])

    def coletar_data_hora(self):  # Método para coletar a data e a hora atuais e registrar no banco de dados.
        agora = datetime.now()  # Obtém a data e hora atuais.
        data_formatada = agora.strftime("%d/%m/%Y")  # Formata a data no formato 'dd/mm/aaaa'.
        hora_formatada = agora.strftime("%H:%M")  # Formata a hora no formato 'hh:mm'.

        self.criar_csv()  # Verifica ou cria o arquivo CSV.

       # Lê todas as linhas do arquivo CSV.
        with open('marcacoes.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            linhas = list(reader)  # Converte o conteúdo do CSV em uma lista de linhas.

        # Verifica se há uma linha correspondente ao dia e usuário.
        linha_encontrada = None
        for linha in linhas:
            if linha[0] == data_formatada and linha[8] == self.username:
                linha_encontrada = linha
                break

        if linha_encontrada:  # Se uma linha foi encontrada, atualiza as marcações.
            marcações = linha_encontrada[1:7]  # Pega as marcações (Primeira até Sexta).
            for i, marcacao in enumerate(marcações):
                if not marcacao:  # Verifica se a marcação está vazia (None ou '').
                    linha_encontrada[i+1] = hora_formatada  # Atualiza com a nova marcação.
                    break
        else:
            # Adiciona uma nova linha se não houver marcações anteriores.
            nova_linha = [
                data_formatada, hora_formatada, '', '', '', '', '', '', self.username
            ]
            linhas.append(nova_linha)

        # Reescreve o arquivo CSV com as alterações.
        with open('marcacoes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(linhas)  # Escreve todas as linhas de volta no arquivo.

        # Exibe o diálogo de confirmação.
        self.mostrar_confirmacao_data(hora_formatada)

    def mostrar_confirmacao_data(self, hora_formatada):  # Método para exibir um diálogo de confirmação de marcação.
            self.dialog = MDDialog(  # Cria um novo diálogo de confirmação.
                title="Confirmação de Marcação",  # Define o título do diálogo.
                text=f"Horário registrado: {hora_formatada}",  # Define o texto do diálogo com o horário registrado.
                buttons=[  # Adiciona botões ao diálogo.
                    MDRaisedButton(  # Cria um botão "OK" elevado.
                        text="OK",  # Define o texto do botão.
                        on_release=self.fechar_dialog  # Define a ação para fechar o diálogo quando o botão for pressionado.
                    ),
                ],
            )
            self.dialog.open()  # Abre o diálogo.

    def fechar_dialog(self, *args):  # Método para fechar o diálogo.
        if self.dialog:
            self.dialog.dismiss()  # Fecha o diálogo quando o botão "OK" é pressionado.
            self.dialog = None #Define o dialogo como None apos o fechamento

    def coletar_refeicao(self):
        agora = datetime.now()  # Obtém a data e hora atuais.
        data_formatada = agora.strftime("%d/%m/%Y")  # Formata a data no formato 'dd/mm/aaaa'.
        
        # Caminho do arquivo CSV
        caminho_csv = 'marcacoes.csv'

        registros = []
        # Lê o conteúdo do arquivo CSV para verificar refeições existentes
        with open(caminho_csv, mode='r', newline='') as file:
            reader = csv.reader(file)
            registros = list(reader)

        # Procura por uma entrada existente para o dia e o usuário
        encontrado = False
        for i, linha in enumerate(registros):
            if linha[0] == data_formatada and linha[8] == self.username:
                encontrado = True
                refeicoes_atual = int(linha[7]) if linha[7] else 0  # Verifica e incrementa o número de refeições
                registros[i][7] = refeicoes_atual + 1
                break

        # Se não encontrou uma entrada, cria uma nova com uma refeição
        if not encontrado:
            nova_linha = [data_formatada, '', '', '', '', '', '', 1, self.username]
            registros.append(nova_linha)

        # Reescreve o arquivo CSV com os dados atualizados
        with open(caminho_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros)

        # Exibe o diálogo de confirmação de refeição
        self.mostrar_confirmacao_refeicao()

    def mostrar_confirmacao_refeicao(self):  # Método para exibir um diálogo de confirmação de refeição.
            self.dialog = MDDialog(  # Cria um novo diálogo de confirmação.
                title="Confirmação Refeição",  # Define o título do diálogo.
                text=f"Refeição Registrada!",  # Define o texto do diálogo com a mensagem de refeição registrada.
                buttons=[  # Adiciona botões ao diálogo.
                    MDRaisedButton(  # Cria um botão "OK" elevado.
                        text="OK",  # Define o texto do botão.
                        on_release=self.fechar_dialog  # Define a ação para fechar o diálogo quando o botão for pressionado.
                    ),
                ],
            )
            self.dialog.open()  # Abre o diálogo.
        
    def compartilhar_csv(self):
        # Caminho para o arquivo CSV que você deseja compartilhar
        caminho_csv = 'marcacoes.csv'  # Atualize para o caminho correto do seu arquivo

        # Verifica se o arquivo existe
        if os.path.exists(caminho_csv):
            try:
                # Chama a funcionalidade de compartilhamento do Android
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                context = autoclass('org.kivy.android.PythonActivity').mActivity

                # Prepara o arquivo para compartilhamento
                file_uri = Uri.fromFile(Uri.parse(caminho_csv))

                # Cria a intenção para compartilhar o arquivo
                intent = Intent(Intent.ACTION_SEND)
                intent.setType('text/csv')
                intent.putExtra(Intent.EXTRA_STREAM, file_uri)
                intent.putExtra(Intent.EXTRA_SUBJECT, "Compartilhar CSV")
                context.startActivity(Intent.createChooser(intent, "Compartilhar CSV via WhatsApp"))
            except Exception as e:
                print(f"Erro ao compartilhar o arquivo: {e}")
        else:
            print("O arquivo CSV não foi encontrado.")

        
    
