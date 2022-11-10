"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from datetime import datetime as dt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#================[Funciones Adicionales]=====================

def str_to_date_2(string): 
    return dt.strptime(string, "%Y-%m-%d").date()

def getFirtLastN(lista, N):
    FirstLast =  lt.newList(datastructure = "ARRAY_LIST")
    size = lt.size(lista)
    for i in range(1,N+1):
        lt.addLast(FirstLast, lt.getElement(lista, i))
    for i in range(size-(N-1),size+1):
        lt.addLast(FirstLast, lt.getElement(lista, i))
    return FirstLast

#================[Impresion de datos de tiempo y memoria]=====================

def printTiempo_Memoria(tiempo, memoria): 
    mensaje = "****  Tiempo [ms]: {0} | Memoria [kb]: {1}  ****".format(round(tiempo,2), round(memoria,2))
    print(mensaje)

#================[Impresion de la altura del arbol y su numero de elementos (lab #9)]=====================

def printHeightN(height, n_elements):
    print("====="*20)
    print('La altura del árbol de los record y juegos es: {0} y tiene {1} elementos'.format(height, n_elements))

#================[Menu principal]=====================

def printMenu():
    print("====="*20)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información en el catálogo.")
    print("  [R1]   1- Reportar las cinco videojuegos lanzados recientemente.")
    print("  [R2]   2- Reportar los games de cierta posición dentro de un rango de desempeño, potencial y salario.")
    print("  [R3]   3- Reportar los games dentro de un rango salarial y con cierta etiqueta.")
    print("  [R4]   4- Reportar los games con cierto rasgo característico y nacidos en un periodo de tiempo. ")
    print("  [R5]   5- Graficar el histograma de una propiedad para los games FIFA.")
    print("  [R6]   6- Encontrar posibles sustituciones para los games FIFA")
    print("         0- Salir")
    print("====="*20)

#================[Impresion de la carga de datos]=====================

def printGamesAndRecords(catalog):
    num_games = lt.size(catalog["games_data"])
    num_records = lt.size(catalog["category_data"])
    pos_for_prints_games = [1,2,3,num_games-2,num_games-1, num_games]
    pos_for_prints_records = [1,2,3,num_records-2,num_records-1, num_records]
    
    print("====="*20)
    print("      Número Total de games: {0} y el Numero Total de records: {1}".format(num_games, num_records))


    print(">>>   Primeros 3 games cargados...   >>>")
    for pos_games in pos_for_prints_games:
        games = lt.getElement(catalog["games_data"], pos_games)
        print(
            "\033[1m" +
            "Nombre: " + 
            str(games["Name"]) + 
            "\033[0m" +
            
            "-"*(35 - len(games['Name'])) +

            "\n      Generos: " + 
            str(games["Genres"]) + 
            " "*(40 - len(str(games['Genres'])) -4)+ "Plataforma: " + 
            str(games["Platforms"]) + 

            "\n      Total Speedruns: " +
            str(games["Total_Runs"]) + 
            " "*(40 - len(str(games['Total_Runs'])) -9)+ "Fecha publicacion del videojuego: " +  
            str(games["Release_Date"]) + 
            "\n"        
        )
        if pos_games == 3:
                print(">>>   Últimos 3 games cargados...   >>>")

    print(">>>   Primeros 3 records cargados...   >>>")
    for pos_record in pos_for_prints_records:
        records = lt.getElement(catalog["category_data"], pos_record)
        if int(records['Num_Runs']) != 0:
        
            print(
                "\033[1m" +
                "Nombre: " + 
                str(records["Game_Id"]) + 
                "\033[0m" +
                
                "-"*(35 - len(records['Game_Id'])) +

                "\n      categoria: " + 
                str(records["Category"]) + 
                " "*(40 - len(str(records['Category'])) -4)+ "Subcategoria: " + 
                str(records["Subcategory"]) + 

                "\n      nombre jugador mejor tiempo: " +
                str(records["Players_0"]) + 
                " "*(40 - len(str(records['Players_0'])) -9)+ "tiempo del jugador: " +  
                str(records["Time_0"]) + 

                "\n   Fecha del record: " + 
                str(records["Record_Date_0"]) +

                "\n"

            )
            if pos_record == 3:
                        print(">>>   Últimos 3 records cargados...   >>>")

#================[Impresion del requerimiento #1]=====================

def printR1(sorted_list, sizelista, platform, min_date, max_date):
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(platform, sizelista))
    print("====="*20)
    if sizelista is None:
        print('Busque con una plataforma válida')
    else:
        if sizelista < 5:
            out_n = sizelista
        else:
            out_n = 5
        print('Los últimos {0} videojuegos son...'.format(out_n))
        for game in lt.iterator(sorted_list):

            print(
                "Nombre del videojuego: " + 
                str(game["Name"]) + 
                ",\n      Abreviacion del nombre: " + 
                str(game["Abbreviation"]) + 
                ",\n      Genero del videojuego: " + 
                str(game["Genres"]) + 
                ",\n      Plataformas: " +
                str(game["Platforms"]) + 
                ",\n      Intentos de speedruns: " + 
                str(game["Total_Runs"]) + 
                ",\n      Año de publicacion: " + 
                str(game["Release_Date"]) +  
                "\n"
            )

#================[Impresion del requerimiento #2]=====================

def printR2(n_records, records_list, player):
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(player, n_records))
    print("====="*20)
    if n_records is None:
        print('Busque con un nombre válido')
    else:
        if n_records < 5:
            out_n = n_records
        else:
            out_n = 5
        print('Los records {0} son...'.format(out_n))
        for record in lt.iterator(records_list):

            print(
                "Nombre del videojuego: " + 
                str(record["Game_Id"]) + 
                ",\n      Categoria: " + 
                str(record["Category"]) + 
                ",\n      Subcategoria: " + 
                str(record["Subcategory"]) + 
                ",\n      Intentos de speedruns: " +
                str(record["Num_Runs"]) + 
                ",\n      Nombre del jugador: " + 
                str(record["Players_0"]) + 
                ",\n      Nacionalidad del jugador: " + 
                str(record["Country_0"]) +  
                ",\n      Tiempo del jugador: " + 
                str(record["Time_0"]) +
                ",\n      Fecha del record: " + 
                str(record["Record_Date_0"]) +
                "\n"
            )

#================[Impresion del requerimiento #3]=====================

def printR3(sorted_list, sizelista, min_runs, max_runs):
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} intentos y {2} intentos'.format(sizelista, min_runs, max_runs))
    print("====="*20)
    if sizelista is None:
        print('Busque con una plataforma válida')
    else:
        if sizelista < 6:
            out_n = sizelista
        else:
            out_n = 6
        print('Los records {0} son...'.format(out_n))
        for record in lt.iterator(sorted_list):

            print(
                "Nombre del videojuego: " + 
                str(record["Game_Id"]) + 
                ",\n      Categoria: " + 
                str(record["Category"]) + 
                ",\n      Subcategoria: " + 
                str(record["Subcategory"]) + 
                ",\n      Intentos de speedruns: " +
                str(record["Num_Runs"]) + 
                ",\n      Nombre del jugador: " + 
                str(record["Players_0"]) + 
                ",\n      Nacionalidad del jugador: " + 
                str(record["Country_0"]) +  
                ",\n      Tiempo del jugador: " + 
                str(record["Time_0"]) +
                ",\n      Fecha del record: " + 
                str(record["Record_Date_0"]) +
                "\n"
            )

#================[Impresion del requerimiento #4]=====================

def printR4(sorted_list, sizelista, min_date, max_date):
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} y {2}'.format(sizelista, min_date, max_date))
    print("====="*20)
    if sizelista is None:
        print('Busque con una plataforma válida')
    else:
        if sizelista < 6:
            out_n = sizelista
        else:
            out_n = 6
        print('Los últimos {0} records son...'.format(out_n))
        for record in lt.iterator(sorted_list):

            print(
                "Nombre del videojuego: " + 
                str(record["Game_Id"]) + 
                ",\n      Categoria: " + 
                str(record["Category"]) + 
                ",\n      Subcategoria: " + 
                str(record["Subcategory"]) + 
                ",\n      Intentos de speedruns: " +
                str(record["Num_Runs"]) + 
                ",\n      Nombre del jugador: " + 
                str(record["Players_0"]) + 
                ",\n      Nacionalidad del jugador: " + 
                str(record["Country_0"]) +  
                ",\n      Tiempo del jugador: " + 
                str(record["Time_0"]) +
                ",\n      Fecha del record: " + 
                str(record["Record_Date_0"]) +
                "\n"
            )

#================[Impresion del requerimiento #5]=====================

def printR5(sorted_list, sizelista, min_time, max_time):
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} y {2}'.format(sizelista, min_time, max_time))
    print("====="*20)
    if sizelista is None:
        print('Busque con una plataforma válida')
    else:
        if sizelista < 6:
            out_n = sizelista
        else:
            out_n = 6
        print('Los últimos {0} records son...'.format(out_n))
        for record in lt.iterator(sorted_list):

            print(
                "Nombre del videojuego: " + 
                str(record["Game_Id"]) + 
                ",\n      Categoria: " + 
                str(record["Category"]) + 
                ",\n      Subcategoria: " + 
                str(record["Subcategory"]) + 
                ",\n      Intentos de speedruns: " +
                str(record["Num_Runs"]) + 
                ",\n      Nombre del jugador: " + 
                str(record["Players_0"]) + 
                ",\n      Nacionalidad del jugador: " + 
                str(record["Country_0"]) +  
                ",\n      Tiempo del jugador: " + 
                str(record["Time_0"]) +
                ",\n      Fecha del record: " + 
                str(record["Record_Date_0"]) +
                "\n"
            )

    

catalog = None

"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")

        catalog = controller.call_new_catalog()

        time, memory = controller.load_data(catalog)   

        printGamesAndRecords(catalog)
        printTiempo_Memoria(time, memory)    
    
    
    elif inputs == "1":
        platform = input('Nombre de la plataforma: ')
        min_date = str_to_date_2(input("Ingrese la fecha minima: "))
        max_date = str_to_date_2(input("Ingrese la fecha maxima: "))

        sorted_list, sizelista, time, memory = controller.callR1(catalog, platform, min_date, max_date)

        printR1(sorted_list, sizelista, platform, min_date, max_date)
        printTiempo_Memoria(time, memory)

    elif inputs == "2":
        player = input('Nombre del jugador: ')

        records_list, n_records, time, memory = controller.callR2(catalog, player)


        printR2(n_records, records_list, player)
        printTiempo_Memoria(time, memory)
    
    elif inputs == "3":
        min_runs = int(input('ingrese el numero minimo de intentos: '))
        max_runs = int(input('ingrese el numero maximo de intentos: '))

        sorted_list, sizelista, time, memory = controller.callR3(catalog, min_runs, max_runs)

        printR3(sorted_list, sizelista, min_runs, max_runs)
        printTiempo_Memoria(time, memory)

    elif inputs == "4":
        min_date = input('ingrese el numero minimo de intentos: ')
        max_date = input('ingrese el numero maximo de intentos: ')

        sorted_list, sizelista, time, memory = controller.callR4(catalog, min_date, max_date)

        printR4(sorted_list, sizelista, min_date, max_date)
        printTiempo_Memoria(time, memory)

    elif inputs == "5":
        min_time = float(input('ingrese el numero minimo de intentos: '))
        max_time = float(input('ingrese el numero maximo de intentos: '))

        sorted_list, sizelista, time, memory = controller.callR5(catalog, min_time, max_time)

        printR5(sorted_list, sizelista, min_time, max_time)
        printTiempo_Memoria(time, memory)

    else:
        sys.exit(0)
sys.exit(0)
