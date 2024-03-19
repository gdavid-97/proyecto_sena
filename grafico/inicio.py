import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generico as util
import conexion
from grafico.principal import MasterPanel

BG_COLOR = '#3a7ff6'
BG_COLOR_BLANCO = '#fcfcfc'
BG_COLOR_FONT = '#666a88'

class App:

    def verificar(self):
        usua = self.usuario.get()
        clave = self.clave.get()
        if(conexion.verificar(nombre_usuario=usua, clave=clave)):
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message="La contraseña o usuario no es correcto", title="Mensaje") 

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de Sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        util.centar_ventana(self.ventana, 800, 500)

        logo = util.leer_imagen(path="img/icono-s.png",size=(200,200))

        #Imagen parte izquierda
        marco_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=BG_COLOR)
        marco_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label( marco_logo, image=logo, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        #parte derecha
        marco_formulario = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg=BG_COLOR_BLANCO)
        marco_formulario.pack(side='right', expand=tk.YES, fill=tk.BOTH)

        #Titulo
        marco_formulario_arriba = tk.Frame (marco_formulario, height= 50, bd=0, relief=tk.SOLID, bg = 'black')
        marco_formulario_arriba.pack(side='top', fill=tk.X)
        titulo = tk.Label(marco_formulario_arriba, text="Inicio de sesion", font=('Times', 30), fg=BG_COLOR_FONT, bg=BG_COLOR_BLANCO, pady=50)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        #Parte drecha abajo
        marco_dormulario_abajo = tk.Frame(marco_formulario, height=50, bd=0, relief=tk.SOLID, bg=BG_COLOR_BLANCO)
        marco_dormulario_abajo.pack(side='bottom', expand=tk.YES, fill=tk.BOTH)

        #Usuario
        etiqueta_usuario = tk.Label(marco_dormulario_abajo, text='Usuario', font=('Times',14), fg=BG_COLOR_FONT, bg=BG_COLOR_BLANCO, anchor='w')
        etiqueta_usuario.pack(fill=tk.X, padx=100, pady=10)
        self.usuario = ttk.Entry(marco_dormulario_abajo, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=100, pady=10)

        #Clave
        etiqueta_clave = tk.Label(marco_dormulario_abajo, text='contraseña', font=('Times',14), fg=BG_COLOR_FONT, bg=BG_COLOR_BLANCO, anchor='w')
        etiqueta_clave.pack(fill=tk.X, padx=100, pady=5)
        self.clave = ttk.Entry(marco_dormulario_abajo, font=('Times', 14))
        self.clave.pack(fill=tk.X, padx=100, pady=10)
        self.clave.config(show='*')

        #Boton
        inicio = tk.Button(marco_dormulario_abajo, text="Iniciar sesion", font=('Times', 15, BOLD), bg=BG_COLOR,bd=0, fg='#fff', command=self.verificar)
        inicio.pack(fill=tk.X, padx=100, pady=20)
        inicio.bind('<Return>', (lambda event: self.verificar()))


        self.ventana.mainloop()
