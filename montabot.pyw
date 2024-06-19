# Importe os módulos necessários
from curses.textpad import Textbox
import subprocess
import customtkinter
import threading
import time
from tkinter import *
from PIL import Image, ImageTk
from PIL.Image import open as pil_open
from logging import root
from multiprocessing import process
from tkinter import Image
import customtkinter 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from curses.textpad import Textbox
from _curses import *

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("dark-blue")  

# Defina uma função para ler o arquivo de log e exibir seu conteúdo na caixa de texto
def update_log_text():
    try:
        # Abra o arquivo de log em modo de leitura
        with open("app_log.txt", "r") as log_file:
            # Limpe o conteúdo atual da caixa de texto
            text_widget.config(state=NORMAL)
            text_widget.delete("1.0", END)
            # Leia todas as linhas do arquivo de log e exiba-as na caixa de texto
            for line in log_file:
                text_widget.insert(END, line)
            text_widget.config(state=DISABLED)
    except FileNotFoundError:
        # Se o arquivo de log não for encontrado, exiba uma mensagem na caixa de texto
        text_widget.config(state=NORMAL)
        text_widget.insert(END, "Log file not found.")
        text_widget.config(state=DISABLED)
    except Exception as e:
        # Se ocorrer algum outro erro, exiba uma mensagem de erro na caixa de texto
        text_widget.config(state=NORMAL)
        text_widget.insert(END, f"Error: {str(e)}")
        text_widget.config(state=DISABLED)

    # Role a caixa de texto para o final para mostrar as últimas mensagens
    text_widget.see(END)

# Defina uma função para atualizar periodicamente o log
def periodic_log_update():
    while True:
        # Chame a função de atualização do log
        update_log_text()
        # Aguarde alguns segundos antes de atualizar novamente
        time.sleep(5)

# Crie a janela principal
root = customtkinter.CTkToplevel()
root.title("InstaBot v1.0")
root.geometry("400x500")

frame = customtkinter.CTkLabel(root, text="INSTABOT", font=('Roboto', 20))
frame.pack(pady=10)

pais_label = customtkinter.CTkLabel(root, text="Servidores Conectar", font=('Roboto', 15))
pais_label.pack(pady=5)

bandeira_brasil = pil_open("./images/brasil.png")
bandeira_brasil = bandeira_brasil.resize((20, 20))
bandeira_brasil_tk = ImageTk.PhotoImage(bandeira_brasil)

dot_image = pil_open("./images/red_dot.png")
dot_image = dot_image.resize((10, 10))
dot_image_tk = ImageTk.PhotoImage(dot_image)

bandeira_label = customtkinter.CTkLabel(root, image=bandeira_brasil_tk, text="")
bandeira_label.image = bandeira_brasil_tk
bandeira_label.pack(side="top")

brazil_label = customtkinter.CTkLabel(root, text="Brazil", font=('Roboto', 12))
brazil_label.pack(side="top")

resultado_label = customtkinter.CTkLabel(root, text="")
resultado_label.pack()


# Função para iniciar ou pausar o bot
def iniciar_bot():
    global text_widget
    global resultado_label
    global dot_image_label
    global subprocesses
    global iniciar_bot_button  

    if iniciar_bot_button.cget("text") == "PLAY BOT":
        try:
            process = subprocess.Popen(["python", "montador.pyw"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            subprocesses.append(process)  

            def update_text_widget():
                while True:
                    try:
                        stdout_line = process.stdout.readline()
                        if not stdout_line:
                            break
                        text_widget.insert("end", stdout_line)  
                    except UnicodeDecodeError as e:
                        stdout_line = f"Erro de codificação: {str(e)}"
                        text_widget.insert("end", stdout_line)  

                process.wait()

            thread = threading.Thread(target=update_text_widget)
            thread.start()

            resultado_label.configure(text="Bot iniciado e conectado ao Brasil.")
            dot_image = pil_open("./images/green_dot.png")  
            dot_image = dot_image.resize((10, 10))  
            dot_image_tk = ImageTk.PhotoImage(dot_image)  
            dot_image_label.configure(image=dot_image_tk)
            dot_image_label.image = dot_image_tk

        except Exception as e:
            resultado_label.configure(text=f"Erro ao iniciar o bot: {str(e)}")
            print(f"Error: {str(e)}")  

        iniciar_bot_button.config(text="PAUSE BOT")
    else:
        for process in subprocesses:
            process.terminate()
        subprocesses.clear()  

        resultado_label.configure(text="Bot pausado.")
        dot_image = pil_open("./images/red_dot.png")  
        dot_image = dot_image.resize((10, 10))  
        dot_image_tk = ImageTk.PhotoImage(dot_image)  
        dot_image_label.configure(image=dot_image_tk)
        dot_image_label.image = dot_image_tk

        iniciar_bot_button.config(text="PLAY BOT")

# Botão para iniciar ou pausar o bot
iniciar_bot_button = customtkinter.CTkButton(root, text="PLAY BOT", command=iniciar_bot, height=45, width=180)
iniciar_bot_button.pack(pady=10)

dot_image_label = customtkinter.CTkLabel(root, image=dot_image_tk, text="")
dot_image_label.image = dot_image_tk
dot_image_label.pack(side="bottom", pady="10")

# Defina a largura da borda e a cor da borda para a janela principal
root.configure(bd=2, highlightthickness=0, highlightbackground="black")

# Defina o fundo preto da janela principal
root.configure(background="black")

# Função para criar uma caixa de texto com fundo preto, texto branco e bordas arredondadas

text_widget = Text(root, height=120, width=250, bg="black", fg="white", bd=0, relief="flat", font=("Helvetica", 10))
text_widget.pack(pady=5)
text_widget.configure(state='disabled')
# Defina o estilo da borda
text_widget.config(highlightbackground="gray", highlightcolor="gray", highlightthickness=2)

# Crie uma thread para atualizar periodicamente o log
subprocesses = []  # Lista para manter referências aos subprocessos em execução
log_update_thread = threading.Thread(target=periodic_log_update)
log_update_thread.start()

# Impede que a janela seja redimensionada
root.resizable(False, False)

customtkinter.CTkLabel(root, text="", ).pack()

# Inicie o loop principal da interface gráfica
root.mainloop()
