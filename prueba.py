# Elaborado por :
# Fecha de creacion:
# Ultima modificacion:
# Version de python:

#Librerias
import re

# FUNCIONES DE MEDICAMENTOS

def limpiarComillas(lista):
    """
    Funcionamiento: Limpia comillas, espacios y convierte numeros.
    Entradas:
    lista(list): lista con datos del CSV.
    Salidas:
    nuevaLista(list): lista limpia y convertida.
    """
    nuevaLista = []
    for palabra in lista:
        nuevaPalabra = ""
        for letra in palabra:
            if letra == '"':
                continue
            else:
                nuevaPalabra += letra
        nuevaPalabra = " ".join(nuevaPalabra.split())
        if nuevaPalabra.isdigit():
            nuevaLista += [int(nuevaPalabra)]
        else:
            numero = True
            puntos = 0
            for caracter in nuevaPalabra:
                if caracter == ".":
                    puntos += 1
                elif caracter.isdigit() == False:
                    numero = False
            if numero == True and puntos <= 1 and nuevaPalabra != "":
                nuevaLista += [float(nuevaPalabra)]
            else:
                nuevaLista += [nuevaPalabra.title()]
    return nuevaLista

def normalizarMedicamento(nombre):
    """
    Funcionamiento: Limpia espacios y normaliza nombres de medicamentos.
    Entradas:
    nombre(str): nombre del medicamento.
    Salidas:
    nombre(str): nombre limpio.
    """
    nombre = " ".join(nombre.split())
    return nombre.title()


def validarCodigoMedicamento(codigo):
    """
    Funcionamiento: Valida el formato del codigo del medicamento.
    Entradas:
    codigo(str): codigo a revisar.
    Salidas:
    True o False segun el formato sea valido.
    """
    patron = r"^[A-Z]{3}-[0-9]{3}[a-z]{2}$"
    if re.fullmatch(patron, codigo):
        return True
    return False


def cargarMedicamentos(inventario,nombreArchivo):
    """
    Funcionamiento: Carga medicamentos desde un archivo CSV.
    Entradas:
    inventario(list): lista donde se guardan medicamentos.
    nombreArchivo(str): nombre del archivo CSV.
    Salidas:
    inventario(list): lista actualizada.
    """
    with open(nombreArchivo,"r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            medicamentos = linea.split(",")
            medicamentos = limpiarComillas(medicamentos)
            if len(medicamentos) != 4:
                continue
            medicamentos[0] = normalizarMedicamento(medicamentos[0])
            if validarCodigoMedicamento(medicamentos[1]) == False:
                continue
            if isinstance(medicamentos[2],int) == False:
                continue
            if isinstance(medicamentos[3],float) == False and isinstance(medicamentos[3],int) == False:
                continue
            inventario.append(medicamentos)
    print("Medicamentos cargados de manera exitosa.")
    return inventario

    
def cargarMedicamentosAux(inventario):
    while True:
        try:
            while True:
                nombreArchivo = input("Ingrese el nombre del CSV donde se encuentran los medicamentos: ")
                f =open(nombreArchivo,"r")
                inventario= cargarMedicamentos(inventario,nombreArchivo)
                if inventario == [] :
                    print("El archivo debe tener medicamentos guardados")
                    continue
                break
            return inventario
        except FileNotFoundError:
            print("El archivo ingresado no existe")
            continue


# FUNCIONES DEL PABELLON


def crearPabellon(pabellon):
    """
    Funcionamiento: Crea la matriz del pabellon con camas libres.
    Entradas:
    pabellon(list): matriz vacia del pabellon.
    Salidas:
    pabellon(list): matriz llena con 'Libre'.
    """
    while True:
        fila = input("Ingrese el numero de secciones: ")
        if fila.isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        fila = int(fila)
        if fila <= 0:
            print("Debe ser mayor que 0.")
            continue
        break
    while True:
        columna = input("Ingrese el numero de camas por seccion: ")
        if columna.isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        columna = int(columna)
        if columna <= 0:
            print("Debe ser mayor que 0.")
            continue
        break
    contFila = 0
    while contFila < fila:
        filas = []
        contColumnas = 0
        while contColumnas < columna:
            filas += ["Libre"]
            contColumnas += 1
        pabellon.append(filas)
        contFila += 1
    return pabellon


def visualizarPabellon(pabellon):
    """
    Funcionamiento: Muestra el contenido actual del pabellon.
    Entradas:
    pabellon(list): matriz con las camas.
    Salidas:
    No retorna nada, solo imprime el pabellon.
    """
    if pabellon == []:
        print("No existe un pabellon creado.")
        return
    for fila in pabellon:
        for cama in fila:
            print("[", cama, "]", end=" ")
        print()
    return


# FUNCIONES DE PACIENTES


def validarExpediente(expediente):
    """
    Funcionamiento: Valida el formato del expediente del paciente.
    Entradas:
    expediente(str): numero de expediente.
    Salidas:
    True o False segun sea valido.
    """
    patron = r"^[A-Z]{3}#[0-9]{4}$"
    if re.fullmatch(patron, expediente):
        return True
    return False


def normalizarNombre(nombre):
    """
    Funcionamiento: Ordena el nombre y lo deja en formato titulo.
    Entradas:
    nombre(str): nombre completo del paciente.
    Salidas:
    resultado(str): nombre normalizado.
    """
    palabras = nombre.split()
    resultado = ""
    for palabra in palabras:
        nuevaPalabra = palabra[0].upper() + palabra[1:].lower()
        resultado += nuevaPalabra + " "
    return resultado.strip()


def expedienteRepetido(expediente, pacientesRegistrados):
    """
    Funcionamiento: Revisa si un expediente ya fue registrado.
    Entradas:
    expediente(str): numero de expediente.
    pacientesRegistrados(list): lista de pacientes.
    Salidas:
    True o False segun ya exista.
    """
    for paciente in pacientesRegistrados:
        if paciente[1] == expediente:
            return True
    return False


def pedirExpediente(pacientesRegistrados):
    """
    Funcionamiento: Pide y valida el expediente del paciente.
    Entradas:
    pacientesRegistrados(list): pacientes ya guardados.
    Salidas:
    expediente(str) o None si el usuario cancela.
    """
    while True:
        expediente = input("Ingrese el expediente o escriba CANCELAR: ")
        if expediente.upper() == "CANCELAR":
            return None
        if validarExpediente(expediente) == False:
            print("Formato invalido. Ejemplo: AAA#0000")
            continue
        if expedienteRepetido(expediente, pacientesRegistrados):
            print("El expediente ya existe.")
            continue
        return expediente


def pedirNombre():
    """
    Funcionamiento: Pide el nombre del paciente y lo normaliza.
    Entradas:
    No recibe entradas.
    Salidas:
    nombre(str): nombre limpio y ordenado.
    """
    while True:
        nombre = input("Ingrese el nombre completo: ")
        if nombre.strip() == "":
            print("Ingrese un nombre valido.")
            continue
        return normalizarNombre(nombre)


def pedirPrioridad():
    """
    Funcionamiento: Pide la prioridad del paciente.
    Entradas:
    No recibe entradas.
    Salidas:
    prioridad(int): valor entre 1 y 3.
    """
    while True:
        prioridad = input("Ingrese la prioridad (1-3): ")
        if prioridad.isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        prioridad = int(prioridad)
        if prioridad < 1 or prioridad > 3:
            print("La prioridad debe ser del 1 al 3.")
            continue
        return prioridad


def pedirSeveridad():
    """
    Funcionamiento: Pide la severidad del paciente.
    Entradas:
    No recibe entradas.
    Salidas:
    severidad(int): valor entre 1 y 10.
    """
    while True:
        severidad = input("Ingrese la severidad (1-10): ")
        if severidad.isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        severidad = int(severidad)
        if severidad < 1 or severidad > 10:
            print("La severidad debe ser entre 1 y 10.")
            continue
        return severidad


def pedirPeso():
    """
    Funcionamiento: Pide el peso del paciente.
    Entradas:
    No recibe entradas.
    Salidas:
    peso(float): peso valido mayor que cero.
    """
    while True:
        peso = input("Ingrese el peso del paciente: ")
        numero = True
        puntos = 0
        for caracter in peso:
            if caracter == ".":
                puntos += 1
            elif caracter.isdigit() == False:
                numero = False
        if numero == False or puntos > 1:
            print("Ingrese un peso valido.")
            continue
        peso = float(peso)
        if peso <= 0:
            print("El peso debe ser mayor que 0.")
            continue
        return peso


def ubicarPaciente(fila, columna, expediente, pabellon):
    """
    Funcionamiento: Ubica el expediente en una cama libre.
    Entradas:
    fila(int): fila elegida.
    columna(int): columna elegida.
    expediente(str): numero de expediente.
    pabellon(list): matriz de camas.
    Salidas:
    pabellon(list), False o 'Ocupado' segun el resultado.
    """
    if fila < 1 or fila > len(pabellon):
        return False
    if columna < 1 or columna > len(pabellon[0]):
        return False
    if pabellon[fila - 1][columna - 1] != "Libre":
        return "Ocupado"
    pabellon[fila - 1][columna - 1] = expediente
    return pabellon


def pedirUbicacion(expediente, pabellon):
    """
    Funcionamiento: Pide la fila y la columna para ubicar al paciente.
    Entradas:
    expediente(str): numero de expediente.
    pabellon(list): matriz de camas.
    Salidas:
    pabellon(list): matriz actualizada.
    """
    while True:
        visualizarPabellon(pabellon)
        fila = input("Ingrese la fila: ")
        columna = input("Ingrese la columna: ")
        if fila.isdigit() == False or columna.isdigit() == False:
            print("Fila y columna deben ser numeros enteros.")
            continue
        fila = int(fila)
        columna = int(columna)
        resultado = ubicarPaciente(fila, columna, expediente, pabellon)
        if resultado == False:
            print("La ubicacion no existe.")
            continue
        elif resultado == "Ocupado":
            print("La cama esta ocupada.")
            continue
        return resultado


def ingresarPacientesAux(pacientesRegistrados, pabellon):
    """
    Funcionamiento: Recolecta datos y registra un paciente.
    Entradas:
    pacientesRegistrados(list): lista de pacientes.
    pabellon(list): matriz de camas.
    Salidas:
    pacientesRegistrados(list), pabellon(list) actualizados.
    """
    if pabellon == []:
        print("Primero debe crear el pabellon.")
        return pacientesRegistrados, pabellon
    expediente = pedirExpediente(pacientesRegistrados)
    if expediente == None:
        return pacientesRegistrados, pabellon
    nombre = pedirNombre()
    prioridad = pedirPrioridad()
    severidad = pedirSeveridad()
    peso = pedirPeso()
    pabellon = pedirUbicacion(expediente, pabellon)
    paciente = [nombre, expediente, prioridad, severidad, peso]
    pacientesRegistrados.append(paciente)
    print("Paciente registrado correctamente.")
    return pacientesRegistrados, pabellon


# SUMINISTRAR MEDICAMENTOS


def buscarMedicamento(nombreMedicamento, inventario):
    """
    Funcionamiento: Busca un medicamento por nombre.
    Entradas:
    nombreMedicamento(str): nombre a buscar.
    inventario(list): lista de medicamentos.
    Salidas:
    medicamento(list) o None si no existe.
    """
    for medicamento in inventario:
        if medicamento[0].lower() == nombreMedicamento.lower():
            return medicamento
    return None


def calcularDosis(peso, severidad):
    """
    Funcionamiento: Calcula la dosis del medicamento.
    Entradas:
    peso(float): peso del paciente.
    severidad(int): severidad del paciente.
    Salidas:
    dosis(float): dosis calculada.
    """
    dosis = (peso * 0.5) + (severidad * 10)
    return dosis


def calcularFactura(dosis, prioridad, precio):
    """
    Funcionamiento: Calcula subtotal, ajuste y total.
    Entradas:
    dosis(float): dosis calculada.
    prioridad(int): prioridad del paciente.
    precio(float): precio unitario.
    Salidas:
    subtotal, ajuste y total.
    """
    subtotal = dosis * precio
    ajuste = 0
    if prioridad == 1:
        ajuste -= subtotal * 0.10
    elif prioridad == 3:
        ajuste += subtotal * 0.20
    total = subtotal + ajuste
    return subtotal, ajuste, total


def suministrarMedicamentos(inventario):
    """
    Funcionamiento: Busca el medicamento y descuenta stock.
    Entradas:
    inventario(list): lista de medicamentos.
    Salidas:
    inventario(list) actualizado.
    """
    nombreMedicamento = input("Ingrese el nombre del medicamento: ")
    medicamento = buscarMedicamento(nombreMedicamento, inventario)
    if medicamento == None:
        print("El medicamento no existe.")
        return inventario
    if medicamento[2] <= 0:
        print("No hay stock disponible.")
        return inventario
    peso = pedirPeso()
    severidad = pedirSeveridad()
    prioridad = pedirPrioridad()
    dosis = calcularDosis(peso, severidad)
    if medicamento[2] - dosis < 0:
        print("No hay suficiente stock.")
        return inventario
    subtotal, ajuste, total = calcularFactura(dosis, prioridad, medicamento[3])
    medicamento[2] -= int(dosis)
    print("Dosis:", dosis)
    print("Subtotal:", subtotal)
    print("Ajuste:", ajuste)
    print("Total:", total)
    if medicamento[2] <= 5:
        print("ALERTA: Punto de reorden alcanzado.")
    return inventario


# PROCESAR ALTA


def buscarPaciente(expediente, pacientes):
    """
    Funcionamiento: Busca un paciente por expediente.
    Entradas:
    expediente(str): numero de expediente.
    pacientes(list): lista de pacientes.
    Salidas:
    paciente(list) o None si no existe.
    """
    for paciente in pacientes:
        if paciente[1] == expediente:
            return paciente
    return None


def liberarCama(expediente, pabellon):
    """
    Funcionamiento: Libera la cama donde esta el expediente.
    Entradas:
    expediente(str): numero de expediente.
    pabellon(list): matriz de camas.
    Salidas:
    pabellon(list) o False si no se encuentra.
    """
    fila = 0
    while fila < len(pabellon):
        columna = 0
        while columna < len(pabellon[fila]):
            if pabellon[fila][columna] == expediente:
                pabellon[fila][columna] = "Libre"
                return pabellon
            columna += 1
        fila += 1
    return False


def pedirFechaAlta():
    """
    Funcionamiento: Pide la fecha de alta o acepta HOY.
    Entradas:
    No recibe entradas.
    Salidas:
    fecha(str): fecha valida o la palabra HOY.
    """
    while True:
        fecha = input("Ingrese la fecha dd/mm/aaaa o escriba HOY: ")
        if fecha.upper() == "HOY":
            return "HOY"
        patron = r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$"
        if re.fullmatch(patron, fecha):
            return fecha
        print("Formato invalido.")


def procesarAlta(bitacoraHistorica, pacientesRegistrados, pabellon):
    """
    Funcionamiento: Libera la cama y guarda la alta en la bitacora.
    Entradas:
    bitacoraHistorica(list): historial de altas.
    pacientesRegistrados(list): lista de pacientes.
    pabellon(list): matriz de camas.
    Salidas:
    bitacoraHistorica(list), pabellon(list) actualizados.
    """
    expediente = input("Ingrese el expediente del paciente: ")
    paciente = buscarPaciente(expediente, pacientesRegistrados)
    if paciente == None:
        print("El paciente no existe.")
        return bitacoraHistorica, pabellon
    confirmacion = input("Desea confirmar el alta? (S/N): ")
    if confirmacion.upper() != "S":
        print("Alta cancelada.")
        return bitacoraHistorica, pabellon
    resultado = liberarCama(expediente, pabellon)
    if resultado == False:
        print("El paciente no se encuentra en el pabellon.")
        return bitacoraHistorica, pabellon
    fechaAlta = pedirFechaAlta()
    historial = (paciente[1], paciente[0], fechaAlta)
    bitacoraHistorica.append(historial)
    print("Alta procesada correctamente.")
    return bitacoraHistorica, pabellon


# ADMINISTRACION


def guardarPabellon(pabellon):
    """
    Funcionamiento: Guarda el pabellon en un archivo de texto.
    Entradas:
    pabellon(list): matriz de camas.
    Salidas:
    "Hola" luego de guardar el archivo.
    """
    nomArchivo = input("Ingrese el nombre del archivo: ")
    with open(nomArchivo, "w") as arvhivo:
        contFil = 1
        contColum = 1
        for seccion in pabellon:
            for cama in seccion:
                if cama == "Libre":
                    arvhivo.write("En la fila " + str(contFil) + " y en la columna " + str(contColum) + " se encuebtra libre.\n")
                else:
                    arvhivo.write("En la fila " + str(contFil) + " y en la columna " + str(contColum) + " se encuebtra el paciente" + str(cama) + ".\n")
                contColum += 1
            contFil += 1
    print("pabellon guardado exitosamente")
    return "Hola"


def redimencionarPabellon(pabellon):
    """
    Funcionamiento: Crea un pabellon nuevo y permite guardar el anterior.
    Entradas:
    pabellon(list): matriz actual.
    Salidas:
    nuevoPabellon(list) o None si se cancela.
    """
    nuevoPabellon = []
    archivo = ""
    nuevoPabellon = crearPabellon(nuevoPabellon)
    confirmacion = input("Esta seguro de que quiere redimencionar el pabellon, ya que se pueden eliminar datos(SI/NO): ")
    if confirmacion.upper() == "NO":
        return
    guardar = input("desea guardar el antiguo pabellon(SI/NO): ")
    if guardar.upper() == "SI":
        archivo = guardarPabellon(pabellon)
    print(archivo)
    return nuevoPabellon


# REPORTE ESTADISTICO


def reporteEstadistico(bitacoraHistorica):
    """
    Funcionamiento: Muestra la bitacora y la semana con mas altas.
    Entradas:
    bitacoraHistorica(list): historial de altas.
    Salidas:
    No retorna nada, solo imprime resultados.
    """
    if bitacoraHistorica == []:
        print("No hay pacientes dados de alta.")
        return
    print("\nBITACORA HISTORICA")
    for paciente in bitacoraHistorica:
        print("Expediente:", paciente[0])
        print("Nombre:", paciente[1])
        print("Fecha:", paciente[2])
        print()
    semanas = {}
    mayor = 0
    semanaMayor = ""
    for paciente in bitacoraHistorica:
        fecha = paciente[2]
        if fecha == "HOY":
            continue
        partes = fecha.split("/")
        dia = int(partes[0])
        semana = ((dia - 1) // 7) + 1
        llave = "Semana " + str(semana)
        if llave in semanas:
            semanas[llave] += 1
        else:
            semanas[llave] = 1
    for llave in semanas:
        if semanas[llave] > mayor:
            mayor = semanas[llave]
            semanaMayor = llave
    if semanaMayor != "":
        print("La semana con mas altas fue:", semanaMayor)


# SUBMENU ADMINISTRACION


def menuAdministracion(pabellon, inventario, pacientesRegistrados, bitacora):
    """
    Funcionamiento: Muestra el submenu de administracion.
    Entradas:
    pabellon(list): matriz de camas.
    inventario(list): lista de medicamentos.
    pacientesRegistrados(list): lista de pacientes.
    bitacora(list): historial de altas.
    Salidas:
    pabellon(list), inventario(list) actualizados.
    """
    while True:
        subopcion = input(
        "\nA: Redimensionar pabellon\n"
        "B: Agregar medicamento\n"
        "C: Modificar stock\n"
        "D: Modificar precio\n"
        "E: Buscar paciente\n"
        "F: Estadias\n"
        "0: Salir\n"
        "Ingrese una opcion: "
        )
        if subopcion.upper() == "A":
            nuevo = redimencionarPabellon(pabellon)
            if nuevo != None:
                pabellon = nuevo
        elif subopcion.upper() == "B":
            inventario = agregarMedicamento(inventario)
        elif subopcion.upper() == "C":
            inventario = modificarStock(inventario)
        elif subopcion.upper() == "D":
            inventario = modificarPrecio(inventario)
        elif subopcion.upper() == "E":
            buscarPacienteSistema(pacientesRegistrados, pabellon, bitacora)
        elif subopcion.upper() == "F":
            menuEstadias(pabellon, pacientesRegistrados)
        elif subopcion == "0":
            return pabellon, inventario
        else:
            print("Opcion invalida.")


# AGREGAR MEDICAMENTO


def medicamentoExiste(nombre, inventario):
    """
    Funcionamiento: Revisa si el medicamento ya existe.
    Entradas:
    nombre(str): nombre del medicamento.
    inventario(list): lista de medicamentos.
    Salidas:
    True o False segun exista.
    """
    for medicamento in inventario:
        if medicamento[0].lower() == nombre.lower():
            return True
    return False


def agregarMedicamentoAux():
    """
    Funcionamiento: Pide y valida el codigo del medicamento.
    Entradas:
    No recibe entradas.
    Salidas:
    codigo(str): codigo valido.
    """
    while True:
        codigo = input("Ingrese el codigo o 'CANCELAR' para salir: ")
        if codigo.upper() == "CANCELAR":
            return False
        if validarCodigoMedicamento(codigo) == False:
            print("Codigo invalido.")
            continue
        return codigo


def agregarMedicamento(inventario):
    """
    Funcionamiento: Agrega un medicamento al inventario.
    Entradas:
    inventario(list): lista de medicamentos.
    Salidas:
    inventario(list) actualizado.
    """
    nombre = input("Ingrese el nombre del medicamento o 'CANCELAR' para salir: ")
    if nombre.upper() == "CANCELAR":
        return inventario
    if medicamentoExiste(nombre, inventario):
        print("El medicamento ya existe.")
        return inventario
    codigo = agregarMedicamentoAux()
    if codigo == False:
        return inventario
    while True:
        stock = input("Ingrese el stock o 'CANCELAR' para salir: ")
        if stock.isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        stock = int(stock)
        if stock < 0:
            print("No puede ser negativo.")
            continue
        break
    while True:
        precio = input("Ingrese el precio o 'CANCELAR' para salir: ")
        if precio.upper() == "CANCELAR":
            return inventario
        try:
            precio = float(precio)
            if precio <= 0:
                print("Debe ser mayor que 0.")
                continue
            break
        except:
            print("Precio invalido.")
    medicamento = [nombre, codigo, stock, precio]
    inventario.append(medicamento)
    print("Medicamento agregado correctamente.")
    return inventario


# MODIFICAR STOCK

def modificarStockAux(inventario):
    """
    Funcionamiento: Pide la cantidad para modificar el stock.
    Entradas:
    medicamento(list): medicamento seleccionado.
    Salidas:
    cantidad(int): cambio de stock permitido.
    """
    while True:
        nombre = input("Ingrese el medicamento o 'CANCELAR' para salir: ")
        if nombre.upper == "CANCELAR":
            return inventario
        cantidad = input("Ingrese la cantidad o 'CANCELAR' para salir: ")
        if cantidad.upper() == "CANCELAR":
            return inventario
        if cantidad.lstrip("-").isdigit() == False:
            print("Ingrese un numero entero.")
            continue
        cantidad = int(cantidad)
        medicamento =buscarMedicamento(nombre, inventario)
        if medicamento == None:
            print("El medicamento no existe.")
            return inventario
        if cantidad <= 0:
            print("La cantidad ingresada tiene que ser mayor a 0.")
        inventario = modificarStock(inventario,medicamento,cantidad)
        return inventario


def modificarStock(inventario,medicamento,cantidad):
    """
    Funcionamiento: Modifica el stock de un medicamento.
    Entradas:
    inventario(list): lista de medicamentos.
    Salidas:
    inventario(list) actualizado.
    """
    if medicamento == None:
        print("El medicamento no existe.")
        return inventario
    medicamento[2] += cantidad
    print("Stock actualizado.")
    return inventario


# MODIFICAR PRECIO


def modificarPrecioAux():
    """
    Funcionamiento: Pide el nuevo precio del medicamento.
    Entradas:
    No recibe entradas.
    Salidas:
    precio(float): nuevo precio valido.
    """
    while True:
        precio = input("Ingrese el nuevo precio: ")
        try:
            precio = float(precio)
            if precio <= 0:
                print("Debe ser mayor que 0.")
                continue
            return precio
        except:
            print("Precio invalido.")


def modificarPrecio(inventario):
    """
    Funcionamiento: Cambia el precio de un medicamento.
    Entradas:
    inventario(list): lista de medicamentos.
    Salidas:
    inventario(list) actualizado.
    """
    nombre = input("Ingrese el medicamento: ")
    medicamento = buscarMedicamento(nombre, inventario)
    if medicamento == None:
        print("El medicamento no existe.")
        return inventario
    precio = modificarPrecioAux()
    medicamento[3] = precio
    print("Precio actualizado.")
    return inventario


# BUSCAR PACIENTE


def buscarUbicacionPaciente(expediente, pabellon):
    """
    Funcionamiento: Busca la ubicacion del expediente en el pabellon.
    Entradas:
    expediente(str): numero de expediente.
    pabellon(list): matriz de camas.
    Salidas:
    tupla(fila,columna) o None si no existe.
    """
    fila = 0
    while fila < len(pabellon):
        columna = 0
        while columna < len(pabellon[fila]):
            if pabellon[fila][columna] == expediente:
                return fila, columna
            columna += 1
        fila += 1
    return None


def buscarPacienteSistema(pacientesRegistrados, pabellon, bitacora):
    """
    Funcionamiento: Busca un paciente en el pabellon o en la bitacora.
    Entradas:
    pacientesRegistrados(list): lista de pacientes.
    pabellon(list): matriz de camas.
    bitacora(list): historial de altas.
    Salidas:
    No retorna nada, solo muestra el resultado.
    """
    expediente = input("Ingrese el expediente: ")
    paciente = buscarPaciente(expediente, pacientesRegistrados)
    if paciente == None:
        print("El paciente no existe.")
        return
    ubicacion = buscarUbicacionPaciente(expediente, pabellon)
    if ubicacion != None:
        print("Paciente internado.")
        print("Nombre:", paciente[0])
        print("Prioridad:", paciente[2])
        print("Fila:", ubicacion[0] + 1)
        print("Columna:", ubicacion[1] + 1)
        return
    for alta in bitacora:
        if alta[0] == expediente:
            print("Paciente dado de alta.")
            print("Nombre:", alta[1])
            print("Fecha:", alta[2])
            return
    print("El paciente no se encontro.")


# ESTADIAS


def menuEstadias(pabellon, pacientesRegistrados):
    """
    Funcionamiento: Muestra el menu de busqueda por ubicacion.
    Entradas:
    pabellon(list): matriz de camas.
    pacientesRegistrados(list): lista de pacientes.
    Salidas:
    No retorna nada, solo llama a otra funcion.
    """
    opcion = input(
    "\n1. Buscar fila\n"
    "2. Buscar columna\n"
    "3. Buscar ubicacion puntual\n"
    "Ingrese opcion: "
    )
    if opcion == "1":
        buscarFila(pabellon, pacientesRegistrados)
    elif opcion == "2":
        buscarColumna(pabellon, pacientesRegistrados)
    elif opcion == "3":
        buscarUbicacionPuntual(pabellon, pacientesRegistrados)
    else:
        print("Opcion invalida.")


def buscarFila(pabellon, pacientesRegistrados):
    """
    Funcionamiento: Muestra los pacientes de una fila.
    Entradas:
    pabellon(list): matriz de camas.
    pacientesRegistrados(list): lista de pacientes.
    Salidas:
    No retorna nada, solo imprime la fila.
    """
    fila = input("Ingrese la fila: ")
    if fila.isdigit() == False:
        print("Ingrese un numero.")
        return
    fila = int(fila)
    if fila < 1 or fila > len(pabellon):
        print("La fila no existe.")
        return
    fila -= 1
    for cama in pabellon[fila]:
        if cama == "Libre":
            print("Libre")
        else:
            paciente = buscarPaciente(cama, pacientesRegistrados)
            print(paciente)


def buscarColumna(pabellon, pacientesRegistrados):
    """
    Funcionamiento: Muestra los pacientes de una columna.
    Entradas:
    pabellon(list): matriz de camas.
    pacientesRegistrados(list): lista de pacientes.
    Salidas:
    No retorna nada, solo imprime la columna.
    """
    columna = input("Ingrese la columna: ")
    if columna.isdigit() == False:
        print("Ingrese un numero.")
        return
    columna = int(columna)
    if columna < 1 or columna > len(pabellon[0]):
        print("La columna no existe.")
        return
    columna -= 1
    fila = 0
    while fila < len(pabellon):
        cama = pabellon[fila][columna]
        if cama == "Libre":
            print("Libre")
        else:
            paciente = buscarPaciente(cama, pacientesRegistrados)
            print(paciente)
        fila += 1


def buscarUbicacionPuntual(pabellon, pacientesRegistrados):
    """
    Funcionamiento: Muestra el paciente de una ubicacion puntual.
    Entradas:
    pabellon(list): matriz de camas.
    pacientesRegistrados(list): lista de pacientes.
    Salidas:
    No retorna nada, solo imprime el resultado.
    """
    fila = input("Ingrese la fila: ")
    columna = input("Ingrese la columna: ")
    if fila.isdigit() == False or columna.isdigit() == False:
        print("Datos invalidos.")
        return
    fila = int(fila)
    columna = int(columna)
    if fila < 1 or fila > len(pabellon):
        print("Fila invalida.")
        return
    if columna < 1 or columna > len(pabellon[0]):
        print("Columna invalida.")
        return
    cama = pabellon[fila - 1][columna - 1]
    if cama == "Libre":
        print("La cama esta libre.")
        return
    paciente = buscarPaciente(cama, pacientesRegistrados)
    print(paciente)

def visualizarInventario(inventario):
    for i in inventario:
        print(i)
    