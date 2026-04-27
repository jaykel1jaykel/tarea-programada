# Elaborado por:
# Fecha de creacion:
# Ultima modificacion:
# version de python:
from datetime import datetime
fecha = datetime.now()
hora = datetime.now().time()
tuplabita = (str(fecha)+"_"+str(hora))
lista = []
bitacora = []
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
    
    with open(pnombre, "r") as nomarchivo:
        for linea in nomarchivo:
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


# Mostrar tokens cargados
def mostrarTokens(tokens):
    global bitacora, tuplabita
    for i in tokens:
        print(i[0],"=",i[1])
    bitacora.append((tuplabita,"se muestraron los tokens cargados"))
    return

# Agregar o modificar tokens
def separarTokens(cadena, separador):
    lista_tuplas = []
    
    partes = cadena.split(",")  # separa cada par
    
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
print(separarTokens("int -> entero, str -> hilera", "->"))


# Def para guardar tokens en nomarchivo
def GuardarTokens():
    global lista, bitacora, tuplabita
    nomarchivo = input("Ingrese el nombre del nombre del archivo: ")
    with open(nomarchivo,"w") as archivo :
        for token in lista:
            linea = token[0]+"->"+token[1]+"\n"
            archivo.write(linea)
    bitacora.append((tuplabita," Se guardaron los tokens"))
    return
nomarchivo = "codigoprueba.txt"
# def generar reporte .csv
def generarCSV(CSV1):
    global lista, nomarchivo, bitacora, tuplabita
    contador = 0
    with open(CSV1,"w") as CSV:
        for tokentra in lista:
            contador = 0
            archivo = open(nomarchivo,"r")
            for linea in archivo:
                if tokentra[0] in linea:
                    contador += 1
            nuevalinea = tokentra[0]+","+tokentra[1]+" = "+str(contador)+"\n"
            CSV.write(nuevalinea)
    bitacora.append((tuplabita,"Se genero el archivo .csv"))
    return
 #Def Bicatora

def crearBitacora():
    global bitacora
    with open("bitacora.txt", "w") as archivo:
        for i in bitacora:
            lineas = i[0]+" "+i[1]+"\n"
            archivo.write(lineas)
    return





cargarTokens("prueba.txt",",")
generarCSV("save.csv")
crearBitacora()