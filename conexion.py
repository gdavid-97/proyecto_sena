import urllib.request


def verificar(nombre_usuario, clave):
    
    try:
        contenido = urllib.request.urlopen(f"http://127.0.0.1:8000/check/{nombre_usuario}/{clave}").read()

        temp = str(contenido)

        if 'no' in temp:
            return False
        else:
            return True
        
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


def enviar_historial(nombre_usuario, clave, historial):

    try:
        historial = historial.replace(" ", "%20")
        print(historial)
        contenido = urllib.request.urlopen(f"http://127.0.0.1:8000/historial/{nombre_usuario}/{clave}/{historial}").read()

        temp = str(contenido)
        
    except Exception as e:
        print(f'{type(e).__name__}: {e}')