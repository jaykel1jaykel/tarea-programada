from Funciones import *
def menu():
    opcion = input("Ingrese su opcion:\n1: Cargar archivo de tokens\n2: Mostrar tokens cargados\n3: Agregar o modificar tokens\n4: Guardar tokens en archivo \n5: Traducir codigo\n6: Generar reporte CSV\n7: Generar reporte HTML\n8: Buscar en bitacoras\n9: Salir\n")   
    if opcion == "1":
        cargarTokens() 
        crearBitacora()
        menu()
    elif opcion == "2":
        mostrarTokens()
        crearBitacora()
        menu()
    elif opcion == "3":
        agregarModificarTokens()
        crearBitacora()
        menu()
    elif opcion == "4":
        guardarTokens()
        crearBitacora()
        menu()
    elif opcion == "5":
        traducirCodigo()
        crearBitacora()
        menu()
    elif opcion == "6":
        generarCSV()
        crearBitacora()
        menu()
    elif opcion == "7":
        "generarHTML()"
        crearBitacora()
        menu()
    elif opcion == "8":
        while True:
            subopcion = input("Ingrese su opcion para buscar en la bitacora: \nA.Buscar por fecha \nB.Buscar por palabras claves\nC.Salir del submenu\n")
            if subopcion == "A" or subopcion == "a":
               buscarConFecha()
            elif subopcion == "B" or subopcion == "b":
                buscarConPalabrasClave()
            elif subopcion == "C" or subopcion == "c":
                break
            else:
                print("Opcion invalida")
        menu()
        
    elif opcion == "9":
        print("Saliendo...")
        return
    else:
        print("Opción inválida")
        menu()

menu()