import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import config

# Função para criar uma conexão com o banco de dados
def criar_conexao():
    try:
        conexao = config.create_connection()
        mensagem_conexao = "MySQL OK"
        cor_mensagem = "White"
    except Exception as e:
        conexao = None
        mensagem_conexao = f"Erro ao conectar ao MySQL: {e}"
        cor_mensagem = "red"
    return conexao, mensagem_conexao, cor_mensagem

# Função para obter todos os países disponíveis no banco de dados
def obter_paises(conexao):
    paises = []
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT pais FROM natalidade_pais")
        paises = cursor.fetchall()
    return paises

# Função para obter todos os anos disponíveis no banco de dados
def obter_anos(conexao):
    anos = []
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT ano FROM natalidade_pais")
        anos = cursor.fetchall()
    return anos

# Função para obter todos os anos disponíveis para um país específico
def obter_anos_por_pais(conexao, pais):
    anos = []
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT ano FROM natalidade_pais WHERE pais = %s", (pais,))
        anos = cursor.fetchall()
    return anos

# Função para obter a taxa de natalidade adolescente para um país e ano específicos
def obter_taxa_natalidade_adolescente(conexao, pais, ano):
    taxa = None
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT TaxaNatalidadeAdolescente FROM natalidade_pais WHERE pais = %s AND ano = %s", (pais, ano))
        resultado = cursor.fetchall()  # Use fetchall() para ler todos os resultados
        if resultado:
            taxa = resultado[0][0]  # Supondo que TaxaNatalidadeAdolescente seja a primeira coluna
    return taxa

# Função para criar a janela principal
def criar_janela():
    raiz = tk.Tk()
    raiz.title("Análise Big Data A3")
    raiz.configure(bg="white")
    raiz.geometry("1000x600")
    raiz.minsize(1000, 600)
    raiz.maxsize(1000, 600)
    raiz.resizable(False, False)

    largura_janela = raiz.winfo_screenwidth()
    altura_janela = raiz.winfo_screenheight()
    largura_janela_raiz = 1000
    altura_janela_raiz = 600
    posicao_topo = (altura_janela - altura_janela_raiz) // 2 - 30 # Ajuste de 30 pixels para considerar a barra de tarefas
    posicao_direita = (largura_janela - largura_janela_raiz) // 2
    raiz.geometry(f"{largura_janela_raiz}x{altura_janela_raiz}+{posicao_direita}+{posicao_topo}")

    return raiz

# Função para criar um canvas para a janela principal
def criar_canvas(raiz):
    canvas = tk.Canvas(raiz, width=1000, height=600, bg="white")
    canvas.pack(fill="both", expand=True)

    imagem = Image.open(r"imgs/foto1.png")
    imagem = imagem.resize((1000, 600))
    canvas.imagem_de_fundo = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, image=canvas.imagem_de_fundo, anchor="nw")

    return canvas

# Função para criar um menu de opções para selecionar o país
def criar_menu_opcoes_paises(raiz, paises):
    paises.sort(key=lambda x: x[0])

    pais_selecionado = tk.StringVar(raiz)
    pais_selecionado.set(paises[0][0])

    estilo = ttk.Style()
    estilo.configure('TCombobox', font=("Helvetica", 10, "bold"), background="white", foreground="black")

    menu_opcoes = ttk.Combobox(raiz, textvariable=pais_selecionado, values=[pais[0] for pais in paises], style='TCombobox')
    menu_opcoes.state(["readonly"])

    return menu_opcoes, pais_selecionado

# Função para criar um menu de opções para selecionar o ano
def criar_menu_opcoes_anos(raiz):
    ano_selecionado = tk.StringVar(raiz)
    ano_selecionado.set('')

    menu_opcoes = ttk.Combobox(raiz, textvariable=ano_selecionado)
    menu_opcoes.state(["readonly"])
    return menu_opcoes, ano_selecionado

# Função para criar um campo de saída para exibir a taxa de natalidade adolescente
def criar_campo_saida(raiz):
    valor_saida = tk.StringVar(raiz)
    campo_saida = tk.Label(raiz, textvariable=valor_saida, bg="white", fg="black", font=("Helvetica", 10, "bold"))
    campo_saida.config(width=10)  # Definir uma largura fixa
    return campo_saida, valor_saida

# Função para atualizar a lista de anos com base no país selecionado
def atualizar_anos(event, conexao, valor_saida):
    pais_selecionado = menu_opcoes_paises.get()
    anos = obter_anos_por_pais(conexao, pais_selecionado)
    menu_opcoes_anos['values'] = [ano[0] for ano in anos]
    menu_opcoes_anos.set('')  # Limpar a seleção atual
    valor_saida.set('')  # Limpar o campo de saída

# Função para atualizar a taxa de natalidade adolescente com base no país e ano selecionados
def atualizar_taxa_natalidade_adolescente(event, conexao, valor_saida):
    pais_selecionado = menu_opcoes_paises.get()
    ano_selecionado = menu_opcoes_anos.get()
    taxa = obter_taxa_natalidade_adolescente(conexao, pais_selecionado, ano_selecionado)
    valor_saida.set(taxa)

# Função para criar um botão para fechar a janela
def criar_botao_fechar(raiz, conexao):
    def fechar_janela():
        if conexao and conexao.is_connected():
            conexao.close()
        raiz.destroy()

    botao_fechar = tk.Button(raiz, text="Sair", command=fechar_janela, bg="#007BFF", fg="white", font=("Helvetica", 16, "bold"), padx=10, pady=5)
    botao_fechar.place(relx=0.95, rely=0.95, anchor="se")
    return botao_fechar

# Função principal para executar o programa
def principal():
    conexao, mensagem_conexao, cor_mensagem = criar_conexao()
    paises = obter_paises(conexao)
    raiz = criar_janela()
    canvas = criar_canvas(raiz)

    global menu_opcoes_anos, menu_opcoes_paises

    menu_opcoes_paises, pais_selecionado = criar_menu_opcoes_paises(raiz, paises)
    menu_opcoes_paises.bind('<<ComboboxSelected>>', lambda event: atualizar_anos(event, conexao, valor_saida))

    menu_opcoes_anos, ano_selecionado = criar_menu_opcoes_anos(raiz)
    menu_opcoes_anos.bind('<<ComboboxSelected>>', lambda event: atualizar_taxa_natalidade_adolescente(event, conexao, valor_saida))

    campo_saida, valor_saida = criar_campo_saida(raiz)

    botao_fechar = criar_botao_fechar(raiz, conexao)

    campo_saida.place(relx=0.5, rely=0.4, anchor="center")
    menu_opcoes_paises.place(relx=0.5, rely=0.5, anchor="center")
    menu_opcoes_anos.place(relx=0.5, rely=0.6, anchor="center")

    botao_fechar.place(relx=0.95, rely=0.95, anchor="se")

    label_conexao = tk.Label(raiz, text=mensagem_conexao, fg=cor_mensagem, bg="black", font=("Helvetica", 10, "bold"))
    label_conexao.place(x=20, rely=0.98, anchor="sw")

    raiz.mainloop()

if __name__ == "__main__":
    principal()
