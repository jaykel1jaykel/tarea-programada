from Funciones import *
def menu():
    opcion = input("Ingrese su opcion:\n1: Cargar archivo de tokens\n2: Mostrar tokens cargados\n3: Agregar o modificar tokens\n4: Guardar tokens en archivo \n5: Traducir codigo\n6: Generar reporte CSV\n7: Generar reporte HTML\n9: Salir\n")   
    if opcion == "1":
        cargarTokens() 
        menu()
    elif opcion == "2":
        mostrarTokens()
        menu()
    elif opcion == "3":
        "agregarModificarTokens()"
        menu()
    elif opcion == "4":
        guardarTokens()
        menu()
    elif opcion == "5":
        "traducirCodigo()"
        menu()
    elif opcion == "6":
        generarCSV()
        menu()
    elif opcion == "7":
        "generarHTML()"
        menu()
    elif opcion == "8":
        subopcion = input("Ingrese su opcion para buscar en la bitacora: \n 1. Buscar por fecha \n 2. Buscar por palabras claves")
        if subopcion == "1":
            buscarConFecha()
    elif opcion == "9":
        print("Saliendo...")
        return
    else:
        print("Opción inválida")
        menu()

menu()