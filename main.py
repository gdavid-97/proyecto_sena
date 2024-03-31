import conexion
from functions import onlines
import util.generico as util
import requests

from grafico.inicio import App
from grafico.principal import MasterPanel

def sin_grafico():
    usuario=""
    clave=0

    login = True
    ciclo = False
    
    while login:

        usuario=input("usuario-->")
        clave=input("contraseña-->")

        f = conexion.verificar(nombre_usuario=usuario, clave=clave)

        if f:
            print("acceso concedido")
            login = False
            ciclo = True
        else:
            print("acceso denegado")

    util.saludar()
            
    while ciclo:
        
        #query = util.escuchar().lower()
        
        query = input("--->").lower()

        if 'exit' in query:
            login = True
            ciclo = False

        if 'voxnova' in query: 
            query = query.split("voxnova")
            query = query[1]

            conexion.enviar_historial(usuario, clave, str(query))

            if ' ip ' in query:
                direccion_ip = onlines.buscar_ip()
                util.paralelo(f'Su Dirección IP es {direccion_ip}')
                print(f'Tu direccion IP es {direccion_ip}')
            
            elif 'whatsapp' in query:
                util.hablar('¿A qué número debería enviar el mensaje?, por favor, digítelo en la consola: ')
                number = input("Ingrese el número: ")
                util.hablar("¿Cúal es el mensaje?")
                message = input("-->")
                onlines.enviar_whatsapp(number, message)
                util.hablar("El mensaje ha sido enviado")

            elif 'wikipedia' in query:

                query = query.split("wikipedia")
                query = query[1]

                temp = onlines.buscar_wikipedia(query)
                util.paralelo(temp)

            elif 'youtube'in query:
                query = query.split("youtube")
                query = query[1]
                onlines.youtube(query)

            elif 'noticias'in query:
                temp = onlines.noticias()
                print(temp)
                util.hablar(temp)

            elif 'clima' in query:
                city = "Bogotá"
                util.paralelo(f"Obteneniendo el informe meteorológico de la ciudad de {city}")
                print()
                clima, temperatura, feels_like = onlines.clima(city)
                util.paralelo(f"La temperatura es {temperatura}, pero se siente como {feels_like}")
                print()
                util.paralelo(f"el parte meteorológico habla de {clima}")
                print()

            else:
                print("Procesando...")
                try:
                    temp = onlines.ai(query)

                    util.paralelo(temp[0])
                    print()
                        
                except Exception as e:
                    print(f'{type(e).__name__}: {e}')
            


if __name__ == '__main__':

    temporal = input("Grafica -->")
    if temporal == "si":
        App()
    else:
        sin_grafico()
