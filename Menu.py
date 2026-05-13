# Elaborado por: Hillary Matinez, Jaykel Miranda
# Fecha de creacion: 24-04-2026
# Ultima modificacion:12-05-2026
# version de pyrhon:3.14

from Funciones import *
def menu():
    tokens = []
    bitacora = []
    while True:
        opcion = input("1: Cargar archivo de tokens\n2: Mostrar tokens cargados\n3: Agregar o modificar tokens\n4: Guardar tokens en archivo \n5: Traducir codigo\n6: Generar reporte CSV\n7: Generar reporte HTML\n8: Buscar en bitacoras\n9: Salir\nIngrese su opcion:")   
        if opcion == "1":
            tokens,bitacora = cargarTokensAux(tokens,bitacora) 
            crearBitacora(bitacora)
            continue
        elif opcion == "2":
            bitacora = mostrarTokens(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "3":
            tokens,bitacora = agregarModificarTokensAux(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "4":
            tokens,bitacora = guardarTokensAux(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "5":
            tokens,bitacora = traducirCodigoAux(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "6":
            tokens,bitacora = generarCSVAux(tokens, bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "7":
            tokens,bitacora =generarHTMLAux(tokens,bitacora)
            crearBitacora(bitacora)
            continue
        elif opcion == "8":
            while True:
                subopcion = input("A.Buscar por fecha \nB.Buscar por palabras claves\nC.Salir del submenu\nIngrese su opcion para buscar en la bitacora: ")
                if subopcion == "A" or subopcion == "a":
                    buscarConFechaAux(bitacora)
                    continue
                elif subopcion == "B" or subopcion == "b":
                    buscarConPalabrasClaveAux(bitacora)
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