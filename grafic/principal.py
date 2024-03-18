import tkinter as tk
from tkinter.font import BOLD
import util.generico as util

BG_COLOR = '#22A4E0'
BG_COLOR_FONT = '#E6DC75'

FONT= 'Times 14'
class MasterPanel:

    def __init__(self):
        width=600
        height=600
        self.ventana = tk.Tk()
        self.ventana.title('principal')
        self.ventana.config(bg='#fcfcfc', width=width,height=height)
        self.ventana.resizable(width=0, height=0)
        util.centar_ventana(self.ventana, width, height)

        chat = tk.Frame(self.ventana, bg=BG_COLOR, width=600, height= 500)
        chat.pack(side='top',expand=tk.NO)

        inicio= tk.Label(chat, bg=BG_COLOR, fg= BG_COLOR_FONT, text='Bienvendio', font= FONT, pady=10)
        inicio.place(relwidth=1)

        linea = tk.Label(chat,width=450,bg=BG_COLOR_FONT)
        linea.place(relwidth=1, rely=0.07, relheight=0.0012)

        self.texto_widget = tk.Text(chat, width=20, height=2, bg=BG_COLOR, fg=BG_COLOR_FONT, font= FONT, padx=5, pady=5)
        self.texto_widget.place(relwidth=0.745, relheight=1, rely=0.08, relx=0.08)
        self.texto_widget.config(cursor='arrow', state='disabled')

        scroolbar = tk.Scrollbar(self.texto_widget)
        scroolbar.place(relheight=1, relx=0.974)
        scroolbar.configure(command=self.texto_widget.yview)


        self.ventana.mainloop()