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

def verificar(username, password):
    try:
        contents = urllib.request.urlopen(f"http://127.0.0.1:8000/check/{username}/{password}").read()

        temp = str(contents)

        print(temp)

        if 'no' in temp:
            return False
        else:
            return True
        
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


# Conversión Texto a Voz
def speak(text):
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
    
    engine.say(text)
    engine.runAndWait()
    del engine

def typing(text):
    for char in text:
        sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()

def parallel(text):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_tasks = {executor.submit(speak, text), executor.submit(typing, text)}
        for future in concurrent.futures.as_completed(future_tasks):
            try:
                data = future.result()
            except Exception as e:
                print(f'{type(e).__name__}: {e}')


def greet_user():
    """Saluda al usuario de acuerdo al horario"""
    
    hour = datetime.now().hour
    if (hour >= 0) and (hour < 12):
        speak(f"Buenos días {USUARIO}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Buenas tardes {USUARIO}")
    elif (hour >= 16) and (hour < 24):
        speak(f"Buenas noches {USUARIO}")
    speak(f"Yo soy {NOMBRE_APP}. ¿Cómo puedo asistirle?")


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
                speak("Buenas noches")
            else:
                speak('¡Tenga un buen día!')
            return "exit"
    except Exception:
        speak('Disculpe, no he podido entender. ¿Podría decirlo de nuevo?')
        query = 'None'
    return query



if __name__ == '__main__':
    
    while login:

        usename=input("usuario-->")
        password=input("contraseña-->")

        f = verificar(username=usename, password=password)

        if f:
            print("acceso concedido")
            login = False
            ciclo = True
        else:
            print("acceso denegado")

    greet_user()
            
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
                ip_address = onlines.buscar_ip()
                parallel(f'Su Dirección IP es {ip_address}')
                print(f'Tu direccion IP es {ip_address}')
            
            elif ' whatsapp ' in query:
                speak('¿A qué número debería enviar el mensaje?, por favor, digítelo en la consola: ')
                number = input("Ingrese el número: ")
                speak("¿Cúal es el mensaje?")
                message = input("-->")
                onlines.enviar_whatsapp(number, message)
                speak("El mensaje ha sido enviado")

            elif ' wikipedia ' in query:

                query = query.split("wikipedia")
                query = query[1]

                temp = onlines.buscar_wikipedia(query)
                parallel(temp)
                print()

            elif ' youtube 'in query:
                query = query.split("youtube")
                query = query[1]
                onlines.youtube(query)

            elif ' noticias 'in query:
                temp = onlines.noticias()
                print(temp)
                speak(temp)

            else:
                print("Procesando...")
                stream = False
                try:
                    temp = onlines.ai(query, stream)

                    if stream: 
                        for chunk in temp:
                            print(chunk.text)
                            speak(chunk.text)
                    else:
                        parallel(temp)
                        print()
                        
                except Exception as e:
                    print(f'{type(e).__name__}: {e}')
            