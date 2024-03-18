import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generico as util
import conexion
from grafic.principal import MasterPanel

class App:

    def verificar(self):
        usua = self.usuario.get()
        clave = self.clave.get()
        if(conexion.verificar(nombre_usuario=usua, clave=clave)):
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message="La contraseña no es correcta", title="Mensaje") 

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de Sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        util.centar_ventana(self.ventana, 800, 500)

        logo = util.leer_imagen(path="img/icono-s.png",size=(200,200))

        #Frame Imagen parte izquierda
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#3a7ff6")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        #Frame parte derecha
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side='right', expand=tk.YES, fill=tk.BOTH)

        #Frame Titulo
        frame_form_top = tk.Frame (frame_form, height= 50, bd=0, relief=tk.SOLID, bg = 'black')
        frame_form_top.pack(side='top', fill=tk.X)
        titulo = tk.Label(frame_form_top, text="Inicio de sesion", font=('Times', 30), fg='#666a88', bg='#fcfcfc', pady=50)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        #Frame Parte drecha abajo
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side='bottom', expand=tk.YES, fill=tk.BOTH)

        #Frame usuario
        etiqueta_usuario = tk.Label(frame_form_fill, text='Usuario', font=('Times',14), fg='#666a88', bg='#fcfcfc', anchor='w')
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=10)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        #Frame clave
        etiqueta_clave = tk.Label(frame_form_fill, text='contraseña', font=('Times',14), fg='#666a88', bg='#fcfcfc', anchor='w')
        etiqueta_clave.pack(fill=tk.X, padx=20, pady=5)
        self.clave = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.clave.pack(fill=tk.X, padx=20, pady=10)
        self.clave.config(show='*')

        #Frame boton
        inicio = tk.Button(frame_form_fill, text="Iniciar sesion", font=('Times', 15, BOLD), bg='#3a7ff6',bd=0, fg='#fff', command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind('<Return>', (lambda event: self.verificar()))


        self.ventana.mainloop()
