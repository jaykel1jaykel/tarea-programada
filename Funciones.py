# Elaborado por:
# Fecha de creacion:
# Ultima modificacion:
# version de python:
from datetime import datetime

lista = []
bitacora = []

# Funciones principales

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

def cargarTokens():
    global lista
    pnombre = input("Ingrese el nombre del archivo donde se encuentran los tokens: ")
    pseparador = input("Ingrese el separador: ")
    with open(pnombre, "r") as nomarchivo:
        for linea in nomarchivo:
            linea = limpiar_linea(linea)
            tupla = procesar_linea(linea, pseparador)
            if tupla is None:
                continue
            reemplazado = False
            for i in range(len(lista)):
                if lista[i][0] == tupla[0]:
                    print("Token repetido, se reemplaza:", lista[i], "por", tupla)
                    lista[i] = tupla
                    reemplazado = True
                    break
            if not reemplazado:
                lista.append(tupla)
    bitacora.append((datetime.now(), "Se cargaron tokens desde archivo"))
    return lista

def mostrarTokens():
    global lista, bitacora
    for i in lista:
        print(i[0], "=", i[1])
    bitacora.append((datetime.now(), "Se mostraron los tokens"))
    return

def separarTokens(cadena, separador):
    lista_tuplas = []
    partes = cadena.split(",")
    for parte in partes:
        parte = parte.strip()
        if separador not in parte:
            print("Formato inválido:", parte)
            continue
        datos = parte.split(separador)
        if len(datos) != 2:
            print("Par mal formado:", parte)
            continue
        token_original = datos[0].strip()
        token_traducido = datos[1].strip()
        lista_tuplas.append((token_original, token_traducido))
    return lista_tuplas

def guardarTokens():
    global lista, bitacora
    nomarchivo = input("Ingrese el nombre del archivo: ")
    with open(nomarchivo, "w") as archivo:
        for token in lista:
            linea = token[0] + " -> " + token[1] + "\n"
            archivo.write(linea)
    bitacora.append((datetime.now(), "Se guardaron los tokens"))
    return
nomarchivo = "codigoprueba.txt"

# def generar csv
def separar_palabras(texto):
    palabras = []
    palabra_actual = ""
    for caracter in texto:
        if caracter.isalnum():  # letras o números
            palabra_actual += caracter
        else:
            if palabra_actual != "":
                palabras.append(palabra_actual)
                palabra_actual = ""
    # agregar última palabra si quedó algo
    if palabra_actual != "":
        palabras.append(palabra_actual)
    return palabras

def generarCSV(CSV1):
    global lista, nomarchivo, bitacora
    with open(nomarchivo, "r") as archivo:
        lineas = archivo.readlines()
    with open(CSV1, "w") as CSV:
        for tokentra in lista:
            contador = 0
            for linea in lineas:
                palabras = separar_palabras(linea)
                if tokentra[0] in palabras:
                    contador += 1
            nuevalinea = tokentra[0] + "," + tokentra[1] + "," + str(contador) + "\n"
            CSV.write(nuevalinea)
    bitacora.append((datetime.now(), "Se generó el archivo CSV"))

def crearBitacora():
    global bitacora
    with open("bitacora.txt", "w") as archivo:
        for i in bitacora:
            linea = str(i[0]) + " " + i[1] + "\n"
            archivo.write(linea)
    return

guardarTokens()