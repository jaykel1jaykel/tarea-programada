# Elaborado por:
# Fecha de creacion:
# Ultima modificacion:
# version de python:
lista = []

# Funciones principales para la tarea programada de traducir codigo
def limpiar_linea(linea):
    return linea.strip()


def procesar_linea(linea, separador):
    if linea == "":
        return None
    
    if separador not in linea:
        print("Línea inválida (sin separador):", linea)
        return None
    
    partes = linea.split(separador)
    
    if len(partes) != 2:
        print("Línea mal formada:", linea)
        return None
    
    token_original = partes[0].strip()
    token_traducido = partes[1].strip()
    
    return (token_original, token_traducido)


def cargarTokens(pnombre, pseparador):
    global lista
    
    with open(pnombre, "r") as archivo:
        for linea in archivo:
            linea = limpiar_linea(linea)
            tupla = procesar_linea(linea, pseparador)
            if tupla is None:
                continue
            # Manejo de duplicados
            reemplazado = False
            for i in range(len(lista)):
                if lista[i][0] == tupla[0]:
                    print("Token repetido, se reemplaza:", lista[i],"por",tupla)
                    lista[i] = tupla
                    reemplazado = True
                    break
            
            if not reemplazado:
                lista.append(tupla)
    
    return lista

cargarTokens("prueba.txt",",")

# Mostrar tokens cargados
def mostrarTokens(tokens):
    for i in tokens:
        print(i[0],"=",i[1])
    return

# Agregar o modificar tokens
