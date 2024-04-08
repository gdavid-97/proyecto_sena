import tkinter as tk
from tkinter.font import BOLD
import util.generico as util

import sys
import concurrent.futures 

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

    query = ""
    usuario = ""
    clave = ""

    def escribir(self, msg):
        self.texto.config(cursor='arrow', state="normal")
        self.texto.insert(tk.END, msg)
        self.texto.insert(tk.END, '\n')
        self.texto.config(cursor='arrow', state="disabled")

    def paralelo(self, texto):
        self.escribir(texto)
        util.hablar(texto)



    def funcion(self):
        self.query = util.escuchar()
        self.funciona()
        


    def funcion1(self):
        self.query = self.texto1.get("1.0","end")
        self.funciona()


    def funciona(self):

        query = self.query

        print(query, self.usuario, self.clave)

        conexion.enviar_historial(self.usuario, self.clave, str(query))

        if ' ip ' in query:
            direccion_ip = onlines.buscar_ip()
            self.paralelo(f'Su Dirección IP es {direccion_ip}')
            
        elif 'whatsapp' in query:
            self.paralelo('¿A qué número debería enviar el mensaje?, por favor, digítelo en la consola: ')
            number = input("Ingrese el número: ")
            self.paralelo("¿Cúal es el mensaje?")
            message = input("-->")
            onlines.enviar_whatsapp(number, message)
            self.paralelo("El mensaje ha sido enviado")

        elif 'wikipedia' in query:
            query = query.split("wikipedia")
            query = query[1]
            temp = onlines.buscar_wikipedia(query)
            self.paralelo(temp)

        elif 'youtube'in query:
            query = query.split("youtube")
            query = query[1]
            onlines.youtube(query)

        elif 'noticias'in query:
            temp = onlines.noticias()
            self.paralelo(temp)
            self.texto1.delete('1.0',tk.END)
        
        elif 'clima' in query:
            city = "Bogotá"
            self.paralelo(f"Obteneniendo el informe meteorológico de la ciudad de {city}")
            clima, temperatura, feels_like = onlines.clima(city)
            self.paralelo(f"La temperatura es {temperatura}, pero se siente como {feels_like}")
            self.paralelo(f"el parte meteorológico habla de {clima}")

        else:
            print("Procesando...")
            try:
                temp = onlines.ai(query)
                self.paralelo(temp[0])
                self.texto1.delete('1.0',tk.END)

            except Exception as e:
                print(f'{type(e).__name__}: {e}')


    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave
        self.ventana = tk.Tk()
        self.ventana.title('principal')
        self.ventana.config(bg='#fcfcfc', width=600, height=700)
        self.ventana.resizable(width=0, height=0)
        util.centar_ventana(self.ventana, 600, 700)
        
        self.chat = tk.Frame(self.ventana, bg=BG_COLOR, width=600, height= 600)
        self.chat.pack(side='top',fill=tk.NONE, expand=tk.NO)

        self.texto = tk.Text(self.chat, width=20, height=2, bg=BG_COLOR, fg=BG_COLOR_FONT, font= FONT, padx=5, pady=5)
        self.texto.place(relwidth=0.745, relheight=0.9, rely=0.08, relx=0.08)

        self.texto.config(cursor='arrow', state="disabled")

        """
        self.scroolbar = tk.Scrollbar(self.texto)
        self.scroolbar.place(relheight=1, relx=0.974)
        self.scroolbar.configure(command=self.texto.yview)
        """

        self.abajo = tk.Frame(self.ventana, bg=BG_COLOR, width=600, height= 100)
        self.abajo.pack(side='bottom', expand=tk.NO, fill=tk.NONE)
        
        boton1 = tk.Button(self.abajo, text="Audio", font= FONT, command=self.funcion)
        boton1.grid(column=0, row=0, sticky="nsew")
        boton1.bind('<Return>', (lambda event: self.funcion()))

        self.texto1 = tk.Text(self.abajo, bg=BG_COLOR, fg=BG_COLOR_FONT, font= FONT, padx=5, pady=5, width=52)
        self.texto1.grid(column=1, row=0, sticky="nsew")
        
        self.boton2 = tk.Button(self.abajo, text="Enviar", font= FONT, command=self.funcion1)
        self.boton2.grid(column=2, row=0, sticky="nsew")
        self.boton2.bind('<Return>', (lambda event: self.funcion1()))
        
        self.abajo.grid_columnconfigure(0, weight=0)
        self.abajo.grid_columnconfigure(1, weight=0)
        self.abajo.grid_columnconfigure(2, weight=0)

        self.abajo.grid_rowconfigure(0, weight=1)

        util.saludar()

        if self.query != '':
            self.funciona()

        self.ventana.mainloop()