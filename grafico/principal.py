import tkinter as tk
from tkinter.font import BOLD
import util.generico as util

BG_COLOR = '#22A4E0'
BG_COLOR_FONT = '#E6DC75'

FONT= 'Times 14'

import conexion
from functions import onlines
from decouple import config

import util.generico as util

USUARIO = config('USER')
NOMBRE_APP = config('BOTNAME')

login = True
ciclo = False


class MasterPanel:

    def __init__(self):

        width=600
        height=650
        self.ventana = tk.Tk()
        self.ventana.title('principal')
        self.ventana.config(bg='#fcfcfc', width=width,height=height)
        self.ventana.resizable(width=0, height=0)
        util.centar_ventana(self.ventana, width, height)

        util.saludar()

        chat = tk.Frame(self.ventana, bg=BG_COLOR, width=600, height= 600)
        chat.pack(side='top',fill=tk.BOTH, expand=tk.NO)

        self.texto = tk.Text(chat, width=20, height=2, bg=BG_COLOR, fg=BG_COLOR_FONT, font= FONT, padx=5, pady=5)
        self.texto.place(relwidth=0.745, relheight=0.9, rely=0.08, relx=0.08)

        self.texto.config(cursor='arrow', state='disabled')

        scroolbar = tk.Scrollbar(self.texto)
        scroolbar.place(relheight=1, relx=0.974)
        scroolbar.configure(command=self.texto.yview)

        abajo = tk.Frame(self.ventana, bg=BG_COLOR, width=600, height= 50)
        abajo.pack(side='bottom',expand=tk.NO, fill=tk.X)

        boton1 = tk.Button(abajo, text="Audio", fg=BG_COLOR_FONT, height=50, width=20)
        boton1.pack( side = 'left', expand=tk.YES, fill=tk.BOTH)

        texto1 = tk.Text(abajo, width=60, height=50, bg=BG_COLOR, fg=BG_COLOR_FONT, font= FONT, padx=5, pady=5)
        texto1.pack(side = 'left')

        boton2 = tk.Button(abajo, text="Enviar", height=50, width=20)
        boton2.pack( side = 'right', expand=tk.YES, fill=tk.BOTH)


        self.ventana.mainloop()