# Clasifica el número de casos de enfermedades infecciosas en niveles de riesgo
def clasificar_casos(casos):
   
    if casos < 100:
        return "Bajo"
    elif casos < 1000:
        return "Moderado"
    elif casos < 10000:
        return "Alto"
    else:
        return "Crítico"


# Valida y limpia nombres de medicamentos
def limpiar_nombre(nombre):
    
    #Limpia un nombre de medicamento eliminando caracteres no deseados y espacios en blanco.
    #nombre (str): Nombre del medicamento.
    #Returns:
    #str: Nombre limpio, o 'Desconocido' si está vacío o inválido.

    if isinstance(nombre, str) and nombre.strip():
        return nombre.strip().title()
    return "Desconocido"


# Clasifica si una advertencia es seria con base en palabras clave
def advertencia_seria(texto):

    #Evalúa si una advertencia médica debe considerarse seria.
    # texto (str): Texto de advertencia.

    texto = texto.lower()
    palabras_clave = ["riesgo de muerte", "letal", "hospitalización", "emergencia", "daño permanente"]
    return any(palabra in texto for palabra in palabras_clave)


# Cuenta cuántas personas hay por nave espacial
def contar_personas_por_nave(lista_personas):
    
    #Calcula cuántas personas hay por nave espacial.
    #lista_personas (list): Lista de diccionarios con campos 'name' y 'craft'.
    #Returns:
    #dict: Nave como clave y número de personas como valor.
    
    conteo = {}
    for persona in lista_personas:
        nave = persona.get("craft", "Desconocida")
        conteo[nave] = conteo.get(nave, 0) + 1
    return conteo
