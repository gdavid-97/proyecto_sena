import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text
from functions import onlines
from time import sleep
import concurrent.futures 
import sys
import urllib.request

USUARIO = config('USER')
NOMBRE_APP = config('BOTNAME')

login = True
ciclo = False

"""
import sqlite3
import os
#Conexion con la base de datos
ruta_base_datos = os.path.abspath("E:\\Programacion\\Proyectos\\Sena\\github\\django-sena-VoxNova\\db.sqlite3")

conn = sqlite3.connect(ruta_base_datos)

data_db = conn.cursor()
sql = "select * from auth_user"
data_db.execute(sql)
row= data_db.fetchall()
print(row[1][1])
"""

def verificar(nombre_usuario, password):
    try:
        contents = urllib.request.urlopen(f"http://127.0.0.1:8000/check/{nombre_usuario}/{password}").read()

        temp = str(contents)

        print(temp)

        if 'no' in temp:
            return False
        else:
            return True
        
    except Exception as e:
        print(f'{type(e).__name__}: {e}')

def historial():

    


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

def escribir(texto):
    for char in texto:
        sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()

def paralelo(texto):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_tasks = {executor.submit(hablar, texto), executor.submit(escribir, texto)}
        for future in concurrent.futures.as_completed(future_tasks):
            try:
                data = future.result()
            except Exception as e:
                print(f'{type(e).__name__}: {e}')


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



if __name__ == '__main__':
    
    while login:

        usuario=input("usuario-->")
        clave=input("contraseña-->")

        f = verificar(nombre_usuario=usuario, password=clave)

        if f:
            print("acceso concedido")
            login = False
            ciclo = True
        else:
            print("acceso denegado")

    saludar()
            
    while ciclo:
        
        #query = escuchar().lower()
        
        query = input("--->").lower()

        if 'exit' in query:
            login = True
            ciclo = False

        if 'voxnova' in query: 
            query = query.split("voxnova")
            query = query[1]

            if ' ip ' in query:
                direccion_ip = onlines.buscar_ip()
                paralelo(f'Su Dirección IP es {direccion_ip}')
                print(f'Tu direccion IP es {direccion_ip}')
            
            elif ' whatsapp ' in query:
                hablar('¿A qué número debería enviar el mensaje?, por favor, digítelo en la consola: ')
                number = input("Ingrese el número: ")
                hablar("¿Cúal es el mensaje?")
                message = input("-->")
                onlines.enviar_whatsapp(number, message)
                hablar("El mensaje ha sido enviado")

            elif ' wikipedia ' in query:

                query = query.split("wikipedia")
                query = query[1]

                temp = onlines.buscar_wikipedia(query)
                paralelo(temp)
                print()

            elif ' youtube 'in query:
                query = query.split("youtube")
                query = query[1]
                onlines.youtube(query)

            elif ' noticias 'in query:
                temp = onlines.noticias()
                print(temp)
                hablar(temp)

            else:
                print("Procesando...")
                stream = False
                try:
                    temp = onlines.ai(query, stream)

                    if stream: 
                        for chunk in temp:
                            print(chunk.text)
                            hablar(chunk.text)
                    else:
                        paralelo(temp)
                        print()
                        
                except Exception as e:
                    print(f'{type(e).__name__}: {e}')
            