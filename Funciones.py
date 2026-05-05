# Elaborado por:
# Fecha de creacion:
# Ultima modificacion:
# version de python:
### Nota: mejorar el nombre de las variables
from datetime import datetime

tokens = []
bitacora = []

# Funciones principales
# def para cargar los tokens
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
    global tokens
    pnombre = input("Ingrese el nombre del archivo donde se encuentran los tokens: ")
    pseparador = input("Ingrese el separador: ")
    with open(pnombre, "r") as nomarchivo:
        for linea in nomarchivo:
            linea = limpiar_linea(linea)
            tupla = procesar_linea(linea, pseparador)
            if tupla is None:
                continue
            reemplazado = False
            for i in range(len(tokens)):
                if tokens[i][0] == tupla[0]:
                    print("Token repetido, se reemplaza:", tokens[i], "por", tupla)
                    tokens[i] = tupla
                    reemplazado = True
                    break
            if not reemplazado:
                tokens.append(tupla)
    bitacora.append((datetime.now(), "Se cargaron tokens desde archivo"))
    return tokens

# def mostrar tokens
def mostrarTokens():
    global tokens, bitacora
    for i in tokens:
        print(i[0], "=", i[1])
    bitacora.append((datetime.now(), "Se mostraron los tokens"))
    return


# agregar o actualizar tokens
def procesar_reemplazo(tokens, original, traduccion):
    encontrado = False
    for i in range(len(tokens)):
        if tokens[i][0] == original:
            print(f"Actualizando token existente: {original} -> {traduccion}")
            tokens[i] = (original, traduccion)
            encontrado = True
            break
    if not encontrado:
        print(f"Añadiendo nuevo token: {original} -> {traduccion}")
        tokens.append((original, traduccion))


def agregarModificarTokens():
    global tokens, bitacora
    cadena = input("Ingrese los tokens (o 'CANCELAR' para regresar): ")
    if cadena == 'CANCELAR':
        return tokens
    separador = input("Ingrese el separador entre token y traducción (ej. ->, =, o ,): ")
    if separador.strip() == ",":
        elementos = cadena.split(",")
        if len(elementos) % 2 != 0:
            print("Error: Los tokens están incompletos, no se pudieron formar pares.")
            return tokens
        for i in range(0, len(elementos), 2):
            original = elementos[i].strip()
            traduccion = elementos[i+1].strip()
            procesar_reemplazo(tokens, original, traduccion)
    else:
        partes = cadena.split(",")
        for parte in partes:
            datos = parte.split(separador)
            if len(datos) == 2:
                original = datos[0].strip()
                traduccion = datos[1].strip()
                procesar_reemplazo(tokens, original, traduccion)
            else:
                print(f"Par mal formado o separador incorrecto en: {parte}")
    return tokens


# def de guardar tokens
def guardarTokens():
    global tokens, bitacora
    nomarchivo = input("Ingrese el nombre del archivo: ")
    with open(nomarchivo, "w") as archivo:
        for token in tokens:
            linea = token[0] + " -> " + token[1] + "\n"
            archivo.write(linea)
    bitacora.append((datetime.now(), "Se guardaron los tokens"))
    return
nomarchivo = "codigoprueba.txt"

# def traducir codigo

def traducirCodigo ():
    global tokens, bitacora
    parchivoEntrada = input("Ingrese el nombre del archivo de entrada: ")
    parchivoSalida = input("Ingrese el nombre del archivo de salida: ")
    parchivoEntrada = open(parchivoEntrada, "r")
    parchivoSalida = open(parchivoSalida, "w")
    for linea in parchivoEntrada:
        lineaNueva = ""
        palabra = ""
        for caracter in linea:
            if caracter.isalnum():
                palabra+=caracter
            else:
                if palabra != "":
                    nueva= palabra
                    for token in tokens:
                        if token[0] == palabra:
                            nueva = token[1]
                            break
                    lineaNueva +=nueva
                    palabra= ""
                lineaNueva+= caracter
        if palabra != "":
            nueva = palabra
            for token in tokens:
                if token[0] == palabra:
                    nueva= token[1]
                    break
            lineaNueva += nueva
        parchivoSalida.write(lineaNueva)
    parchivoEntrada.close()
    parchivoSalida.close()
    bitacora.append((datetime.now(), "Se tradujo el código"))
    return "Traducción completa"


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

def generarCSV():
    global tokens, bitacora
    CSV1 = input("Ingrese el nombre del CSV: ")
    nomarchivo = input("Ingrese el nombre del archivo a analizar: ")
    with open(nomarchivo, "r") as archivo:
        lineas = archivo.readlines()
    with open(CSV1, "w") as CSV:
        for tokentra in tokens:
            contador = 0
            for linea in lineas:
                palabras = separar_palabras(linea)
                if tokentra[0] in palabras:
                    contador += 1
            nuevalinea = tokentra[0] + "," + tokentra[1] + "," + str(contador) + "\n"
            CSV.write(nuevalinea)
    bitacora.append((datetime.now(), "Se genero el archivo CSV"))
    

# def buscar en bitacoras
def crearBitacora():
    global bitacora
    if bitacora != []:
        with open("bitacora.txt", "a") as archivo:
            i = bitacora[-1]
            linea = str(i[0]) + " " + i[1] + "\n"
            archivo.write(linea)
    return

def buscarConFecha():
    global bitacora

    fecha_buscar = input("Ingrese la fecha (AAAA-MM-DD): ").strip()
    encontrado = False

    for i in bitacora:
        fecha_registro = i[0].strftime("%Y-%m-%d")  # solo la fecha

        if fecha_registro == fecha_buscar:
            fecha_completa = i[0].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{fecha_completa} - {i[1]}")
            encontrado = True

    if not encontrado:
        print("No hay datos de esa fecha")
    
def buscarConPalabrasClave():
    global bitacora

    palabra_clave = input("Ingrese la palabra clave: ").strip().lower()
    encontrado = False
    for i in bitacora:
        mensaje = i[1] 
        palabras = mensaje.split()
        for palabra in palabras:
            if palabra.lower() == palabra_clave:
                fecha = i[0].strftime("%Y-%m-%d %H:%M:%S")
                print(f"{fecha} - {mensaje}")
                encontrado = True
                break  
    if not encontrado:
        print("No hay datos con esa palabra clave")