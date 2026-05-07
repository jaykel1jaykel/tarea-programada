from Funciones import *
def menu():
    tokens = []
    bitacora = []
    while True:
        opcion = input("Ingrese su opcion:\n1: Cargar archivo de tokens\n2: Mostrar tokens cargados\n3: Agregar o modificar tokens\n4: Guardar tokens en archivo \n5: Traducir codigo\n6: Generar reporte CSV\n7: Generar reporte HTML\n8: Buscar en bitacoras\n9: Salir\n")   
        if opcion == "1":
            tokens,bitacora= cargarTokens(tokens,bitacora) 
            crearBitacora(bitacora)
            continue
        elif opcion == "2":
            bitacora = mostrarTokens(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "3":
            tokens,bitacora = agregarModificarTokens(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "4":
            tokens,bitacora = guardarTokens(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "5":
            tokens,bitacora = traducirCodigo(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "6":
            tokens,bitacora = generarCSV(tokens, bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "7":
            "generarHTML()"
            crearBitacora(bitacora)
            continue
        elif opcion == "8":
            while True:
                subopcion = input("Ingrese su opcion para buscar en la bitacora: \nA.Buscar por fecha \nB.Buscar por palabras claves\nC.Salir del submenu\n")
                if subopcion == "A" or subopcion == "a":
                    buscarConFecha(bitacora)
                    continue
                elif subopcion == "B" or subopcion == "b":
                    buscarConPalabrasClave(bitacora)
                    continue
                elif subopcion == "C" or subopcion == "c":
                    break
                else:
                    print("Opcion invalida")
        elif opcion == "9":
            print("Saliendo...")
            return
        else:
            print("Opción inválida")
            continue
menu()