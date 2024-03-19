from datetime import datetime
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr

import concurrent.futures 
import sys
import util.generico as util

from time import sleep

from decouple import config

USUARIO = config('USER')
NOMBRE_APP = config('BOTNAME')

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))

def centar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2) - (aplicacion_ancho/2))
    y = int((pantalla_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")


def escribir(texto):
    for char in texto:
        sleep(0.06)
        sys.stdout.write(char)
        sys.stdout.flush()

def paralelo(texto):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_tasks = {executor.submit(util.hablar, texto), executor.submit(escribir, texto)}
        for future in concurrent.futures.as_completed(future_tasks):
            try:
                data = future.result()
            except Exception as e:
                print(f'{type(e).__name__}: {e}')



# Conversión Texto a Voz
def hablar(texto):
    engine = pyttsx3.init('sapi5')

    # Set Rate
    engine.setProperty('rate', 190)

    # Set Volume
    engine.setProperty('volume', 1.0)

    """
    for voice in engine.getProperty('voices'):
        print(voice)
    """

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    engine.say(texto)
    engine.runAndWait()
    del engine

def saludar():
    """Saluda al usuario de acuerdo al horario"""
    
    hour = datetime.now().hour
    if (hour >= 0) and (hour < 12):
        hablar(f"Buenos días {USUARIO}")
    elif (hour >= 12) and (hour < 16):
        hablar(f"Buenas tardes {USUARIO}")
    elif (hour >= 16) and (hour < 24):
        hablar(f"Buenas noches {USUARIO}")
    hablar(f"Yo soy {NOMBRE_APP}. ¿Cómo puedo asistirle?")

def escuchar():
    """Toma las entradas del usuario, las reconoce utilizando el módulo de reconocimiento de voz y lo transforma a texto"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-es')
        print(query)
        if not 'Salir' in query or 'Alto' in query:
            print("Dice: {}".format(query))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                hablar("Buenas noches")
            else:
                hablar('¡Tenga un buen día!')
            return "exit"
    except Exception:
        hablar('Disculpe, no he podido entender. ¿Podría decirlo de nuevo?')
        query = 'None'
    return query

