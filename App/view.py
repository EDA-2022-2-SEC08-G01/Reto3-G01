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


# ___________________________________________________
# Menu Principal
# ___________________________________________________

def printMenu():
    print("====="*20)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información en el catálogo.")
    print("  [R1]   1- Encontrar los videojuegos publicados para un rango de tiempo dada plataforma.")
    print("  [R2]   2- Encontrar los 5 registros con menor tiempo para un jugador en específico.")
    print("  [R3]   3- Conocer los registros más veloces en un rango de intentos.")
    print("  [R4]   4- Conocer los registros más lentos dentro de un rango de fechas. ")
    print("  [R5]   5- Conocer los registros más recientes para un rango de tiempos record.")
    print("  [R6]   6- Diagramar un histograma de propiedades para los registros de un rango de años.")
    print("  [R7]   6- Encontrar el TOP N de los videojuegos más rentables para retransmitir.")
    print("         0- Salir")
    print("====="*20)

# ___________________________________________________
# Impresion Carga de Datos
# ___________________________________________________

def printGamesAndRecords(analyzer):
    num_games = lt.size(analyzer["games_data"])
    num_records = lt.size(analyzer["category_data"])
    pos_for_prints_games = [1,2,3,num_games-2,num_games-1, num_games]
    pos_for_prints_records = [1,2,3,num_records-2,num_records-1, num_records]
    
    print("====="*20)
    print("      Número Total de games: {0} y el Numero Total de records: {1}".format(num_games, num_records))


    print(">>>   Primeros 3 games cargados...   >>>")
    for pos_games in pos_for_prints_games:
        games = lt.getElement(analyzer["games_data"], pos_games)
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
    
    print("_____"*20)
    print("\n")

    print(">>>   Primeros 3 records cargados...   >>>")
    for pos_record in pos_for_prints_records:
        records = lt.getElement(analyzer["category_data"], pos_record)
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

# ___________________________________________________
# Prints por requerimiento
# ___________________________________________________

def printR1(sorted_list, platform, min_date, max_date):
    size = lt.size(sorted_list)
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(platform, size))
    print('Released games between dates'.format(size))
    print("====="*20)
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
        else:
            out_n = 6
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


def printR2(n, records_list, player):
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(player, n))
    print("====="*20)
    if n is None:
        print('Busque con un nombre válido')
    else:
        if n_records < 5:
            out_n = n
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


def printR3(sorted_list, min_runs, max_runs):
    size = lt.size(sorted_list)
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} intentos y {2} intentos'.format(size, min_runs, max_runs))
    print("====="*20)
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
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


def printR4(sorted_list, min_date, max_date):
    size = lt.size(sorted_list)
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} y {2}'.format(size, min_date, max_date))
    print("====="*20)
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
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


def printR5(sorted_list, min_time, max_time):
    size = lt.size(sorted_list)
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} y {2}'.format(size, min_time, max_time))
    print("====="*20)
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
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

    
# ___________________________________________________
# Funciones adicionales y Lab 9
# ___________________________________________________

def printHeightN(height, n_elements):
    print("====="*20)
    print('La altura del árbol de los record y juegos es: {0} y tiene {1} elementos'.format(height, n_elements))

def printTimeMemory(Time, memoria): 
    mensaje = "****  Time [ms]: {0} | Memoria [kb]: {1}  ****".format(round(Time,2), round(memoria,2))
    print(mensaje)

def realDate(string): 
    return dt.strptime(string, "%Y-%m-%d").date()

analyzer = None

# ___________________________________________________
# Menu Principal
# ___________________________________________________

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")

        analyzer = controller.init()

        time, memory = controller.load_data(analyzer)   

        printGamesAndRecords(analyzer)

        printTimeMemory(time, memory)    
    
    
    elif inputs == "1":
        platform = input('Nombre de la plataforma: ')
        min_date = realDate(input("Ingrese el límite inferior de fecha de lanzamiento: "))
        max_date = realDate(input("Ingrese el Límite superior de fecha de lanzamiento: "))

        sorted_list, time, memory = controller.Call_Req1(analyzer, platform, min_date, max_date)

        printR1(sorted_list, platform, min_date, max_date)
        printTimeMemory(time, memory)

    elif inputs == "2":
        player = input('Ingrese el nombre del jugador: ')

        records_list, n_records, time, memory = controller.Call_Req2(analyzer, player)

        printR2(n_records, records_list, player)
        printTimeMemory(time, memory)
    
    elif inputs == "3":
        min_attempts = int(input('ingrese el límite inferior de intentos: '))
        max_attempts = int(input('ingrese el límite superior  de intentos: '))

        sorted_list, time, memory = controller.Call_Req3(analyzer, min_attempts, max_attempts)

        printR3(sorted_list, min_attempts, max_attempts)
        printTimeMemory(time, memory)

    elif inputs == "4":
        min_date_4 = input('ingrese el límite inferior de la fecha: ')
        max_date_4 = input('Ingrese el límite superior de la fecha: ')

        sorted_list, time, memory = controller.Call_Req4(analyzer, min_date_4, max_date_4)

        printR4(sorted_list, min_date_4, max_date_4)
        printTimeMemory(time, memory)

    elif inputs == "5":
        min_time = float(input('ingrese la duración mínima: '))
        max_time = float(input('ingrese la duración máxima: '))

        sorted_list, time, memory = controller.Call_Req5(analyzer, min_time, max_time)

        printR5(sorted_list, min_time, max_time)
        printTimeMemory(time, memory)

    else:
        sys.exit(0)
sys.exit(0)
