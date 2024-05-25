import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import config

def criar_conexao():
    try:
        conexao = config.create_connection()
        mensagem_conexao = "Conexão com MySQL estabelecida"
        cor_mensagem = "green"
    except Exception as e:
        conexao = None
        mensagem_conexao = f"Erro ao conectar ao MySQL: {e}"
        cor_mensagem = "red"
    return conexao, mensagem_conexao, cor_mensagem

def obter_anos(conexao):
    anos = []
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT ano FROM natalidade_pais")
        anos = cursor.fetchall()
    return anos

def obter_paises(conexao):
    paises = []
    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT pais FROM natalidade_pais")
        paises = cursor.fetchall()
    return paises

def criar_janela():
    raiz = tk.Tk()
    raiz.title("Meu Dashboard")
    raiz.state('zoomed')

    largura_janela = raiz.winfo_screenwidth()
    altura_janela = raiz.winfo_screenheight()
    posicao_topo = int(altura_janela / 2 - altura_janela / 2)
    posicao_direita = int(largura_janela / 2 - largura_janela / 2)
    raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_direita}+{posicao_topo}")

    return raiz, largura_janela, altura_janela

def criar_canvas(raiz, largura_janela, altura_janela):
    canvas = tk.Canvas(raiz, width=largura_janela, height=altura_janela)
    canvas.pack(fill="both", expand=True)

    imagem = Image.open(r"imgs/foto1.png")
    imagem = imagem.resize((largura_janela, altura_janela))
    canvas.imagem_de_fundo = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, image=canvas.imagem_de_fundo, anchor="nw")

    return canvas

def criar_menu_opcoes_anos(raiz, anos):
    anos.sort(key=lambda x: x[0])

    ano_selecionado = tk.StringVar(raiz)
    ano_selecionado.set(anos[0][0])

    menu_opcoes = ttk.Combobox(raiz, textvariable=ano_selecionado, values=[ano[0] for ano in anos])
    menu_opcoes.state(["readonly"])
    return menu_opcoes, ano_selecionado

def criar_menu_opcoes_paises(raiz, paises):
    paises.sort(key=lambda x: x[0])

    pais_selecionado = tk.StringVar(raiz)
    pais_selecionado.set(paises[0][0])

    menu_opcoes = ttk.Combobox(raiz, textvariable=pais_selecionado, values=[pais[0] for pais in paises])
    menu_opcoes.state(["readonly"])
    return menu_opcoes, pais_selecionado

def criar_botao_fechar(raiz, conexao, canvas, largura_janela, altura_janela):
    def fechar_janela():
        if conexao and conexao.is_connected():
            conexao.close()
        raiz.destroy()

    botao_fechar = tk.Button(raiz, text="Sair", command=fechar_janela)
    canvas.create_window(largura_janela - 100, altura_janela - 100, anchor="se", window=botao_fechar)
    return botao_fechar

def principal():
    conexao, mensagem_conexao, cor_mensagem = criar_conexao()
    anos = obter_anos(conexao)
    paises = obter_paises(conexao)
    raiz, largura_janela, altura_janela = criar_janela()
    canvas = criar_canvas(raiz, largura_janela, altura_janela)

    menu_opcoes_anos, ano_selecionado = criar_menu_opcoes_anos(raiz, anos)
    menu_opcoes_paises, pais_selecionado = criar_menu_opcoes_paises(raiz, paises)
    botao_fechar = criar_botao_fechar(raiz, conexao, canvas, largura_janela, altura_janela)

    canvas.create_window(largura_janela / 2, 20, anchor="n", window=menu_opcoes_anos)
    canvas.create_window(20, 20, anchor="nw", window=menu_opcoes_paises)
    canvas.create_window(largura_janela - 100, altura_janela - 100, anchor="se", window=botao_fechar)

    label_conexao = tk.Label(raiz, text=mensagem_conexao, fg=cor_mensagem, bg="white", font=("Helvetica", 10, "bold"))
    canvas.create_window(20 + botao_fechar.winfo_reqwidth(), altura_janela - 10, anchor="sw", window=label_conexao)

    raiz.mainloop()

if __name__ == "__main__":
    principal()
