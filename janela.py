import tkinter as tk
from PIL import Image, ImageTk
import config  # importa o módulo de configuração

def criarjanela():
    root = tk.Tk()  # Cria uma nova janela
    root.title("Meu Dashboard")  # Define o título da janela

    # Maximiza a janela
    root.state('zoomed')

    # configurações da janela
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    position_top = int(window_height / 2 - window_height / 2)
    position_right = int(window_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Cria um canvas e adiciona uma imagem de fundo
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)

    # Carrega a imagem de fundo
    image = Image.open(r"imgs\foto1.png")
    image = image.resize((window_width, window_height))
    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Obtém a lista de anos do banco de dados
    years = config.main()

    # Cria uma variável de controle para o OptionMenu
    selected_year = tk.StringVar(root)
    selected_year.set(years[0])  # define o valor inicial

    # Cria o OptionMenu
    option_menu = tk.OptionMenu(root, selected_year, *years)
    option_menu.pack()

    root.mainloop()  # Inicia o loop principal da janela

if __name__ == "__main__":
    main()
