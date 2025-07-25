import requests  # Importamos la librería 'requests' para hacer peticiones HTTP a APIs.

def fetch_json(url, params=None, timeout=10):
    #la funcion fetch_json recibe 3 parametros
    #la direccion de la API
    #parametros que pueden ser enviados junto con la URL
    #el tiempo que estamos esperando, por default son 10 
    try:
        response = requests.get(url, params=params, timeout=timeout) #Aquí hacemos una petición GET al API usando la URL y parámetros que pasamos.
        #El timeout asegura que no se quede esperando eternamente si el servidor no responde.
        response.raise_for_status() #Esta línea revisa si la respuesta tiene un error HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        #Si la petición falla por algún motivo (no hay internet, la URL está mal, etc.), se captura el error aquí.
        #e contiene el error 
        print(f"[ERROR] HTTP error while accessing {url}: {e}")
        raise
    #RAISE: Esta línea vuelve a lanzar el error para que el programa que usa esta función sepa que falló.
    except ValueError as e:
        print(f"[ERROR] Failed to parse JSON from {url}: {e}")
        raise
#como dato importante, estoy usando raise en los codigos en lugar de return porque de esta manera al usar airflow puedo ver los errores, ya que se interrumpe la ejecucion
#en cambio si uso return, el error no es visible 