# Elaborado por: Hillary Martinez, Jaykel Miranda
# Fecha de creacion:
# Ultima modificacion:
# version de python:
### Nota: mejorar el nombre de las variables
from datetime import datetime
import html

# Funciones principales
# def para cargar los tokens

def procesarLinea(linea, separador):
    """
    Funcionamiento: Procesa una línea del archivo de tokens, extrayendo el token original y su traducción.
    Entradas:
    - linea(str): Una cadena de texto que representa una línea del archivo de tokens.
    - separador(str): El carácter o cadena que separa el token original de su traducción
    Salidas:
    - tuple: Una tupla (token_original, token_traducido) si la línea es válida, o None si la línea es inválida.
     La función valida que la línea contenga el separador y que se puedan extraer exactamente dos partes (original y traducción). 
     Si la línea no cumple con el formato esperado, se imprime un mensaje de error y se devuelve None.
    """
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

def cargarTokens(pnombre, pseparador,tokens,bitacora):
    """
    Funcionamiento: Carga tokens desde un archivo, procesando cada línea para extraer los tokens originales y sus traducciones, y actualizando la lista de tokens.
    Entradas:
    - pnombre(str): El nombre del archivo que contiene los tokens a cargar.
    - pseparador(str): El separador utilizado en el archivo para distinguir entre el token original y su traducción.
    - tokens(list): La lista actual de tokens, que se actualizará con los nuevos tokens cargados del archivo.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de cargar tokens.
    Salidas:
    - tuple: Una tupla (tokens_actualizados, bitacora_actualizada) donde:
        - tokens_actualizados(list): La lista de tokens actualizada con los nuevos tokens cargados del archivo. Si un token ya existe, se reemplaza su traducción.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se cargaron tokens desde el archivo.
    """
    with open(pnombre, "r") as nomarchivo:
        for linea in nomarchivo:
            tupla = procesarLinea(linea, pseparador)
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
    return tokens,bitacora

def cargarTokensAux(tokens, bitacora):
    """
    Funcionamiento: Funcion auxiliar para verificar las entradas del usuario al cargar tokens desde un archivo.
    entradas:
    - tokens(list): La lista actual de tokens, que se actualizará con los nuevos tokens cargados del archivo.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de cargar tokens.
    salidas:
    - tuple: Una tupla (tokens_actualizados, bitacora_actualizada) donde:
        - tokens_actualizados(list): La lista de tokens actualizada con los nuevos tokens cargados del archivo. Si un token ya existe, se reemplaza su traducción.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se cargaron tokens desde el archivo.
    """
    while True:
        try:
            print("\n--- Cargar tokens ---")
            nombre = input("Digite el nombre del archivo de tokens (o 0 para cancelar): ").strip()
            if nombre == "":
                print("Debe digitar un nombre de archivo.")
                continue
            if nombre == "0":
                bitacora.append((datetime.now(), "El usuario canceló la carga de tokens"))
                return tokens, bitacora
            separador = input("Digite el separador usado en el archivo (ej: ->, =, ,): ").strip()
            if separador == "":
                print("Debe digitar un separador válido.")
                continue
            cantidad_antes = len(tokens)
            tokens_actualizados, bitacora_actualizada = cargarTokens(nombre, separador, tokens, bitacora)
            cantidad_despues = len(tokens_actualizados)
            if cantidad_despues > cantidad_antes:
                print("Tokens cargados correctamente.")
            else:
                print("Se actualizaron tokens existentes o no hubo cambios.")
            return tokens_actualizados, bitacora_actualizada
        except FileNotFoundError:
            print("El archivo no existe. Intente de nuevo.")
        except PermissionError:
            print("No tiene permisos para abrir ese archivo.")
        except UnicodeDecodeError:
            print("El archivo no se pudo leer por un problema de codificación.")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return tokens, bitacora

# def mostrar tokens
def mostrarTokens(tokens,bitacora):
    """
    Funcionamiento: Muestra los tokens cargados actualmente en la lista de tokens.
    Entradas:
    - tokens(list): La lista de tokens que se desea mostrar.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de mostrar tokens.
    Salidas:
    - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se mostraron los tokens.
    La función recorre la lista de tokens y los imprime en formato "token_original = token_traducido".
    """
    for i in tokens:
        print(i[0], "=", i[1])
    bitacora.append((datetime.now(), "Se mostraron los tokens"))
    return bitacora

# agregar o actualizar tokens
def procesarReemplazo(tokens, original, traduccion):
    """
    Funcionamiento: Procesa la adición o actualización de un token en la lista de tokens. Si el token original ya existe, se actualiza su traducción; si no existe, se agrega como un nuevo token.
    Entradas:
    - tokens(list): La lista actual de tokens, que se actualizará con el nuevo token o la traducción actualizada.
    - original(str): El token original que se desea agregar o modificar.
    - traduccion(str): La traducción que se asignará al token original. Si el token ya existe, esta será la nueva traducción; si el token no existe, esta será la traducción del nuevo token agregado.
    Salidas:
    - None: La función no devuelve un valor, pero modifica la lista de tokens en su lugar. Si el token original ya existe en la lista, 
    se actualiza su traducción y se imprime un mensaje indicando que se ha reemplazado el token existente. 
    Si el token original no existe, se agrega como un nuevo token a la lista y se imprime un mensaje indicando que se ha añadido un nuevo token.
    """
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
    return 

def agregarModificarTokens(cadena, separador, tokens, bitacora):
    """
    Funcionamiento: Procesa una cadena de tokens ingresada por el usuario, agregando o modificando los tokens en la lista de tokens según corresponda.
    Entradas:
    - cadena(str): Una cadena de texto que contiene los tokens a agregar o modificar, con un formato específico que puede incluir un separador entre el token original y su traducción.
    - separador(str): El carácter o cadena que separa el token original de su traducción en la cadena ingresada por el usuario.
    - tokens(list): La lista actual de tokens, que se actualizará con los nuevos tokens agregados o las traducciones modificadas.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de agregar o modificar tokens.
    Salidas:
    - tuple: Una tupla (tokens_actualizados, bitacora_actualizada) donde:
        - tokens_actualizados(list): La lista de tokens actualizada con los nuevos tokens agregados o las traducciones modificadas según la cadena ingresada por el usuario.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se agregaron o modificaron tokens.
    """
    if separador.strip() == ",":
        elementos = cadena.split(",")
        if len(elementos) % 2 != 0:
            print("Error: Los tokens están incompletos, no se pudieron formar pares.")
            return tokens
        for i in range(0, len(elementos), 2):
            original = elementos[i].strip()
            traduccion = elementos[i+1].strip()
            procesarReemplazo(tokens, original, traduccion)
    else:
        partes = cadena.split(",")
        for parte in partes:
            datos = parte.split(separador)
            if len(datos) == 2:
                original = datos[0].strip()
                traduccion = datos[1].strip()
                procesarReemplazo(tokens, original, traduccion)
            else:
                print(f"Advertencia: La parte '{parte}' no se pudo procesar correctamente, este token será ignorado.")
    bitacora.append((datetime.now(), "Se agregaron o modificaron los tokens"))
    return tokens,bitacora

def agregarModificarTokensAux(tokens, bitacora):
    """
    Funcionamiento: Funcion auxiliar para verificar las entradas del usuario al agregar o modificar tokens.
    entradas:
    - tokens(list): La lista actual de tokens, que se actualizará con los nuevos tokens agregados o las traducciones modificadas según la cadena ingresada por el usuario.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de agregar o modificar tokens.
    salidas:
    - tuple: Una tupla (tokens_actualizados, bitacora_actualizada) donde:
        - tokens_actualizados(list): La lista de tokens actualizada con los nuevos tokens agregados o las traducciones modificadas según la cadena ingresada por el usuario.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se agregaron o modificaron tokens.
    """
    while True:
        try:
            print("\n--- Agregar o modificar tokens ---")
            cadenaTokens = input("Ingrese los tokens (o 'CANCELAR' para regresar): ")
            if isinstance(cadenaTokens,str) == False:
                return"Los tokens debe ser una cadena de datos"
            elif cadenaTokens.upper() == 'CANCELAR':
                bitacora.append((datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                 "El usuario canceló agregar o modificar tokens"))
                print("Operación cancelada.")
                return tokens, bitacora
            elif cadenaTokens.strip() == "":
                print("Debe ingresar al menos un token.")
                continue
            separador = input("Ingrese el separador entre token y traducción (ej. ->, =, o ,): ").strip()
            if separador == "":
                print("Debe ingresar un separador válido.")
                continue
            elif separador not in cadenaTokens:
                print("El separador no se encuentra en la cadena de tokens.")
                continue

            tokens, bitacora = agregarModificarTokens(cadenaTokens, separador, tokens, bitacora)
            print("Tokens procesados correctamente.")
            return tokens, bitacora
        except IndexError:
            print("Error: faltan datos para formar un par token-traducción.")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return tokens, bitacora

# def de guardar tokens
def guardarTokens(nomarchivo, tokens, bitacora):
    """
    Funcionamiento: Guarda los tokens en un archivo de texto.
    Entradas:
    - nomarchivo(str): El nombre del archivo donde se guardarán los tokens.
    - tokens(list): La lista de tokens que se desea guardar, donde cada token es una tupla (token_original, token_traducido).
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de guardar tokens.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se guardaron los tokens en el archivo.
    """
    with open(nomarchivo, "w") as archivo:
        for token in tokens:
            linea = token[0] + " -> " + token[1] + "\n"
            archivo.write(linea)
    bitacora.append((datetime.now(), "Se guardaron los tokens"))
    return tokens,bitacora


def guardarTokensAux(tokens, bitacora):
    """
    Funcionamiento: Permite al usuario guardar los tokens en un archivo de texto.
    Entradas:
    - tokens(list): La lista de tokens que se desea guardar.
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de guardar tokens.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se guardaron los tokens en el archivo.
    """
    while True:
        try:
            print("\n--- Guardar tokens ---")
            nombre = input("Digite el nombre del archivo para guardar (o CANCELAR para regresar): ").strip()

            if nombre.upper() == "CANCELAR":
                bitacora.append((datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),"El usuario canceló guardar tokens"))
                return tokens, bitacora
            if nombre == "":
                print("Debe digitar un nombre de archivo válido.")
                continue
            # Opcional: si no trae extensión, se le agrega .txt
            if "." not in nombre:
                print("no se detectó extensión, añada una extensión válida (ej: .txt, .csv)")
                continue
            tokens, bitacora = guardarTokens(nombre, tokens, bitacora)
            print("Tokens guardados correctamente.")
            return tokens, bitacora
        except PermissionError:
            print("No tiene permisos para escribir en ese archivo.")
        except OSError:
            print("No se pudo crear o abrir el archivo.")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return tokens, bitacora
# def traducir codigo

def traducirCodigo (parchivoEntrada,parchivoSalida,tokens,bitacora):
    """
    Funcionamiento: Traduce el contenido de un archivo de entrada utilizando una lista de tokens, y guarda el resultado en un archivo de salida.
    Entradas:
    - parchivoEntrada(str): El nombre del archivo que contiene el código a traducir.
    - parchivoSalida(str): El nombre del archivo donde se guardará el código traducido.
    - tokens(list): La lista de tokens que se utilizará para realizar la traducción, donde cada token es una tupla (token_original, token_traducido).
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de traducir código.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se tradujo el código.
    """
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
    return tokens,bitacora



def traducirCodigoAux(tokens, bitacora):
    """
    Funcionamiento: Permite al usuario traducir el contenido de un archivo de entrada utilizando una lista de tokens, y guarda el resultado en un archivo de salida, con validaciones para las entradas del usuario.
    Entradas:
    - tokens(list): La lista de tokens que se utilizará para realizar la traducción, donde cada token es una tupla (token_original, token_traducido).
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de traducir código.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se tradujo el código.
    """
    while True:
        try:
            print("\n--- Traducir código ---")
            archivoEntrada = input("Digite el nombre del archivo de entrada (o CANCELAR para regresar): ").strip()
            if archivoEntrada.upper() == "CANCELAR":
                bitacora.append((datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                 "El usuario canceló traducir código"))
                return tokens, bitacora
            if archivoEntrada == "":
                print("Debe digitar un archivo de entrada válido.")
                continue
            elif "." not in archivoEntrada:
                print("No se detectó extensión en el archivo de entrada, añada una extensión válida (ej: .txt, .csv)")
                continue
            archivoSalida = input("Digite el nombre del archivo de salida: ").strip()
            if archivoSalida == "":
                print("Debe digitar un archivo de salida válido.")
                continue
            if "." not in archivoSalida:
                print("No se detectó extensión en el archivo de salida, añada una extensión válida (ej: .txt, .csv)")
                continue
            tokens, bitacora = traducirCodigo(archivoEntrada, archivoSalida, tokens, bitacora)
            print("Código traducido correctamente.")
            return tokens, bitacora
        except PermissionError:
            print("No tiene permisos para leer o escribir ese archivo.")
        except FileNotFoundError:
            print("No se encontró alguno de los archivos.")
        except UnicodeDecodeError:
            print("El archivo de entrada no se pudo leer correctamente.")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return tokens, bitacora

# def generar csv
def separarPalabras(texto):
    """
    Funcionamiento: Separa un texto en palabras individuales, utilizando caracteres no alfanuméricos como delimitadores.
    Entradas:
    - texto(str): Una cadena de texto que se desea separar en palabras.
    Salidas:
    - list: Una lista de palabras extraídas del texto, donde cada palabra es una secuencia de caracteres alfanuméricos.

    """
    palabras = []
    palabra_actual = ""
    for caracter in texto:
        if caracter.isalnum():  
            palabra_actual += caracter
        else:
            if palabra_actual != "":
                palabras.append(palabra_actual)
                palabra_actual = ""
    if palabra_actual != "":
        palabras.append(palabra_actual)
    return palabras

def generarCSV(CSV1,nomarchivo,tokens,bitacora):
    """
    Funcionamiento: Genera un archivo CSV que contiene los tokens y la cantidad de veces que cada token aparece en un archivo de entrada.
    Entradas:
    - CSV1(str): El nombre del archivo CSV que se generará con los tokens y sus conteos.
    - nomarchivo(str): El nombre del archivo de entrada que se analizará para contar las apariciones de los tokens.
     - tokens(list): La lista de tokens que se desea contar en el archivo de entrada, donde cada token es una tupla (token_original, token_traducido).
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de generar el archivo CSV.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se generó el archivo CSV.
    """
    with open(nomarchivo, "r") as archivo:
        lineas = archivo.readlines()
    with open(CSV1, "w") as CSV:
        for tokentra in tokens:
            contador = 0
            for linea in lineas:
                palabras = separarPalabras(linea)
                if tokentra[0] in palabras:
                    contador += 1
            nuevalinea = tokentra[0] + "," + tokentra[1] + "," + str(contador) + "\n"
            CSV.write(nuevalinea)
    bitacora.append((datetime.now(), "Se genero el archivo CSV"))
    return tokens,bitacora

def generarCSVAux(tokens, bitacora):
    """
    Funcionamiento: Permite al usuario generar un archivo CSV que contiene los tokens y la cantidad de veces que cada token aparece en un archivo de entrada, con validaciones para las entradas del usuario.
    Entradas:
    - tokens(list): La lista de tokens que se desea contar en el archivo de entrada, donde cada token es una tupla (token_original, token_traducido).
    - bitacora(list): La lista de bitácora, que se actualizará con un registro de la acción de generar el archivo CSV.
    Salidas:
    - tuple: Una tupla (tokens, bitacora_actualizada) donde:
        - tokens(list): La misma lista de tokens que se pasó como entrada, ya que esta función no modifica la lista de tokens.
        - bitacora_actualizada(list): La lista de bitácora actualizada con un nuevo registro que indica que se generó el archivo CSV.
    """
    while True:
        try:
            print("\n--- Generar CSV ---")
            archivo_entrada = input("Digite el archivo a analizar (o CANCELAR para regresar): ").strip()
            if archivo_entrada.upper() == "CANCELAR":
                bitacora.append((datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                 "El usuario canceló generar CSV"))
                return tokens, bitacora
            if archivo_entrada == "":
                print("Debe digitar un archivo de entrada válido.")
                continue
            elif "." not in archivo_entrada:
                print("No se detectó extensión en el archivo de entrada, añada una extensión válida (ej: .txt, .csv)")
                continue
            archivo_salida = input("Digite el nombre del archivo CSV de salida: ").strip()
            if archivo_salida == "":
                print("Debe digitar un nombre de archivo válido.")
                continue
            if not archivo_salida.lower().endswith(".csv"):
                print("No se detectó extensión .csv, se añadirá automáticamente.")
                archivo_salida += ".csv"
            tokens, bitacora = generarCSV(archivo_salida, archivo_entrada, tokens, bitacora)
            print("CSV generado correctamente.")
            return tokens, bitacora

        except PermissionError:
            print("No tiene permisos para leer o escribir ese archivo.")
        except FileNotFoundError:
            print("No se encontró el archivo indicado.")
        except UnicodeDecodeError:
            print("El archivo no se pudo leer correctamente.")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return tokens, bitacora

# Generar html

def obtenerPalabras(archivoTraducido):
    with open(archivoTraducido, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    return separarPalabras(texto)


def contarReemplazos(listaTokens, palabras):
    conteos = []
    totalReemplazos = 0
    for token in listaTokens:
        cantidad = 0
        for palabra in palabras:
            if palabra == token[1]:
                cantidad += 1
        conteos.append((token[0], token[1], cantidad))
        totalReemplazos += cantidad
    return conteos, totalReemplazos

def crearFilasHTML(conteos):
    filas = ""
    i = 0
    for token in conteos:
        if i % 2 == 0:
            color = "#85a9cc"
        else:
            color = "#9C8FE6"
        filas += f"""
        <tr style="background-color:{color};">
            <td>{html.escape(str(token[0]))}</td>
            <td>{html.escape(str(token[1]))}</td>
            <td>{token[2]}</td>
        </tr>
        """
        i += 1
    return filas


def generarHTML(listaTokens, archivoTraducido, tituloReporte, bitacora):
    inicio = datetime.now()
    ahora = datetime.now()
    nombreArchivo = "reporteHTML_" + ahora.strftime("%d-%m-%y_%H-%M-%S") + ".html"
    try:
        palabras = obtenerPalabras(archivoTraducido)
    except FileNotFoundError:
        print("El archivo traducido no existe.")
        return listaTokens, bitacora
    except UnicodeDecodeError:
        print("No se pudo leer el archivo traducido por un problema de codificación.")
        return listaTokens, bitacora
    except Exception as error:
        print(f"Ocurrió un error al leer el archivo: {error}")
        return listaTokens, bitacora
    conteos, totalReemplazos = contarReemplazos(listaTokens, palabras)
    totalPalabras = len(palabras)
    if totalPalabras > 0:
        porcentaje = (totalReemplazos / totalPalabras) * 100
    else:
        porcentaje = 0
    filasHTML = crearFilasHTML(conteos)
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write("<!DOCTYPE html>\n")
            archivo.write("<html lang='es'>\n")
            archivo.write("<head>\n")
            archivo.write("<meta charset='UTF-8'>\n")
            archivo.write(f"<title>{html.escape(tituloReporte)}</title>\n")
            archivo.write("</head>\n")
            archivo.write("<body style='font-family: Arial, sans-serif;'>\n")
            archivo.write("<h1>Reporte de Traducción</h1>\n")
            archivo.write(f"<h2>Generado el {ahora.strftime('%d/%m/%y %H:%M:%S')}</h2>\n")
            final = datetime.now()
            duracion = final-inicio
            archivo.write(f"<p><strong>Duración total:</strong> {duracion}</p>\n")
            archivo.write(f"<p><strong>Cantidad total de reemplazos:</strong> {totalReemplazos}</p>\n")
            archivo.write(f"<p><strong>Porcentaje de palabras reemplazadas:</strong> {porcentaje:.2f}%</p>\n")
            archivo.write("<table border='1' style='border-collapse:collapse; text-align:center; width:100%;'>\n")
            archivo.write("<tr style='background-color:#cccccc;'>\n")
            archivo.write("<th>Original</th>\n")
            archivo.write("<th>Reemplazo</th>\n")
            archivo.write("<th>Cantidad</th>\n")
            archivo.write("</tr>\n")
            archivo.write(filasHTML)
            archivo.write("</table>\n")
            archivo.write("</body>\n")
            archivo.write("</html>\n")
    except PermissionError:
        print("No tiene permisos para escribir el archivo HTML.")
        return listaTokens, bitacora
    except OSError:
        print("No se pudo crear el archivo HTML.")
        return listaTokens, bitacora
    except Exception as error:
        print(f"Ocurrió un error al escribir el HTML: {error}")
        return listaTokens, bitacora
    bitacora.append((datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), "Se generó el reporte HTML"))
    print("Reporte HTML generado correctamente:", nombreArchivo)
    return listaTokens, bitacora

def generarHTMLAux(listaTokens, bitacora):
    while True:
        try:
            if not isinstance(listaTokens, list):
                print("Error: la lista de tokens debe ser una lista.")
                return listaTokens, bitacora
            if not isinstance(bitacora, list):
                print("Error: la bitácora debe ser una lista.")
                return listaTokens, bitacora
            print("\n--- Generar HTML ---")
            archivoTraducido = input("Digite el archivo traducido o CANCELAR para regresar: ").strip()
            if archivoTraducido.upper() == "CANCELAR":
                return listaTokens, bitacora
            if archivoTraducido == "":
                print("Debe digitar un archivo válido.")
                continue
            tituloReporte = input("Digite el título del reporte o CANCELAR para regresar: ").strip()
            if tituloReporte.upper() == "CANCELAR":
                return listaTokens, bitacora
            if tituloReporte == "":
                print("Debe digitar un título válido.")
                continue
            return generarHTML(listaTokens, archivoTraducido, tituloReporte, bitacora)
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            return listaTokens, bitacora
        except FileNotFoundError:
            print("El archivo no existe.")

# def buscar en bitacoras
def crearBitacora(bitacora):
    """
    Funcionamiento: Crea o actualiza un archivo de texto llamado "bitacora.txt" con los registros de la lista de bitácora.
    Entradas:
    - bitacora(list): La lista de bitácora que contiene los registros a guardar en el archivo. Cada registro es una tupla (fecha_hora, mensaje).
    Salidas:
    - None: La funcion no devuelve un valor pero crea o actualiza el archivo "bitacora.txt" con los registros de la lista de bitácora. 
      Si el archivo no existe, se crea uno nuevo; si ya existe, se añaden los nuevos registros al final del archivo.
    """
    if bitacora != []:
        with open("bitacora.txt", "a", encoding="utf-8") as archivo:
            i = bitacora[-1]
            linea = str(i[0]) + " " + i[1] + "\n"
            archivo.write(linea)
    return

def buscarConFecha(fechaBuscar, bitacora):
    """
    Funcionamiento: Busca y muestra los registros de la bitácora que coincidan con una fecha específica ingresada por el usuario.
    Entradas:
    - fecha_buscar(str): La fecha que se desea buscar en la bitácora, en formato "YYYY-MM-DD".
    - bitacora(list): La lista de bitácora que contiene los registros a buscar, donde cada registro es una tupla (fecha_hora, mensaje).
    Salidas:
    - print: La función no devuelve un valor, pero imprime en la consola los registros de la bitácora que coincidan con la fecha ingresada por el usuario. 
      Si no se encuentran registros para esa fecha, se imprime un mensaje indicando que no hay datos de esa fecha.
     La función recorre la lista de bitácora y compara la fecha de cada registro (formateada como "YYYY-MM-DD") con la fecha ingresada por el usuario. 
     Si hay coincidencias, se muestra la fecha completa (con hora) y el mensaje del registro. Si no se encuentra ningún registro para esa fecha, se muestra un mensaje informando al usuario.
    """
    encontrado = False
    for i in bitacora:
        fechaCompleta = i[0]  # solo la fecha
        fechaRegistro = fechaCompleta.strftime("%Y-%m-%d")
        if fechaRegistro == fechaBuscar:
            fechaCompleta = i[0]
            print(f"{fechaCompleta} - {i[1]}")
            encontrado = True
    if not encontrado:
        print("No hay datos de esa fecha")
    return

def buscarConFechaAux(bitacora):
    """
    Funcionamiento: Permite al usuario ingresar una fecha para buscar registros en la bitácora, con validaciones para el formato de la fecha y la opción de cancelar la búsqueda.
    Entradas:
    - bitacora(list): La lista de bitácora que contiene los registros a buscar, donde cada registro es una tupla (fecha_hora, mensaje).
    Salidas:
    - print: La función no devuelve un valor, pero imprime en la consola los registros de la bitácora que coincidan con la fecha ingresada por el usuario.
    """
    while True:
        fechaInput = input("Ingrese la fecha a buscar (YYYY-MM-DD) o CANCELAR para regresar: ").strip()
        if fechaInput.upper() == "CANCELAR":
            print("Búsqueda cancelada.")
            return
        try:
            datetime.strptime(fechaInput, "%Y-%m-%d")
            buscarConFecha(fechaInput, bitacora)
            return
        except ValueError:
            print("Formato de fecha inválido. Por favor ingrese la fecha en formato YYYY-MM-DD.")
    
def buscarConPalabrasClave(palabraClave, bitacora):
    """
    Funcionamiento: Busca y muestra los registros de la bitácora que contengan una palabra clave específica ingresada por el usuario.
    Entradas:
    - palabraClave(str): La palabra clave que se desea buscar en los mensajes de la bitácora.
    - bitacora(list): La lista de bitácora que contiene los registros a buscar
    Salidas:
    - str: La función devuelve una cadena de texto que contiene los registros de la bitácora que coincidan con la palabra clave ingresada por el usuario. 
      Si no se encuentran registros para esa palabra clave, se devuelve un mensaje indicando que no hay datos con esa palabra clave.
    """
    encontrado = False
    for i in bitacora:
        mensaje = i[1] 
        palabras = mensaje.split()
        for palabra in palabras:
            if palabra.lower() == palabraClave:
                fecha = i[0].strftime("%Y-%m-%d %H:%M:%S")
                print(f"{fecha} - {mensaje}")
                encontrado = True
                break  
    if not encontrado:
        return"No hay datos con esa palabra clave"

def buscarConPalabrasClaveAux(bitacora):
    """
    Funcionamiento: Permite al usuario ingresar una palabra clave para buscar registros en la bitácora, con validaciones para la entrada de la palabra clave y la opción de cancelar la búsqueda.
    Entradas:
    - bitacora(list): La lista de bitácora que contiene los registros a buscar, donde cada registro es una tupla (fecha_hora, mensaje).
    Salidas:
    - print: La función no devuelve un valor, pero imprime en la consola los registros de la bitácora que contengan la palabra clave ingresada por el usuario. 
      Si no se encuentra ningún registro para esa palabra clave, se muestra un mensaje informando al usuario.
     La función solicita al usuario que ingrese una palabra clave para buscar en los mensajes de la bitácora. Si el usuario ingresa "CANCELAR", se cancela la búsqueda y se muestra un mensaje indicando que la búsqueda fue cancelada. 
     Si el usuario ingresa una cadena vacía, se le solicita que ingrese una palabra clave válida. Si se ingresa una palabra clave válida, se llama a la función buscarConPalabrasClave para realizar la búsqueda y mostrar los resultados. 
     Si no se encuentran registros para esa palabra clave, se muestra un mensaje informando al usuario.
    """
    while True:
        palabrainput = input("Ingrese la palabra clave a buscar (o CANCELAR para regresar): ").strip()
        if palabrainput.upper() == "CANCELAR":
            print("Búsqueda cancelada.")
            return
        elif palabrainput == "":
            print("Debe ingresar una palabra clave válida.")
            continue
        else:
            resultado = buscarConPalabrasClave(palabrainput, bitacora)
            if resultado is None:
                print("No se encontraron registros con esa palabra clave.")
            else:
                print(resultado)
            return