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
import tabulate
import pandas as pd




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
    NumGames = lt.size(analyzer["games_data"])
    NumRec = lt.size(analyzer["category_data"])
    FirstAndLastGames = [1,2,3,NumGames-2,NumGames-1, NumGames]
    FirstAndLastRecords = [1,2,3,NumRec-2,NumRec-1, NumRec]
    
    print("====="*20)
    print("      Número Total de games: {0} y el Numero Total de records: {1}".format(NumGames, NumRec))


    print(">>>   Primeros 3 games cargados...   >>>")
    for position in FirstAndLastGames:
        games = lt.getElement(analyzer["games_data"], position)
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
        if position == 3:
                print(">>>   Últimos 3 games cargados...   >>>")
    
    print("_____"*20)
    print("\n")

    print(">>>   Primeros 3 records cargados...   >>>")
    for position in FirstAndLastRecords:
        records = lt.getElement(analyzer["category_data"], position)
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
            if position == 3:
                        print(">>>   Últimos 3 records cargados...   >>>")

# ___________________________________________________
# Prints por requerimiento
# ___________________________________________________
def listSize(list):
    return lt.size(list)

def printR1(final_list, size, platform, min_date, max_date):
    
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(platform, size))
    print('Released games between dates{0}'.format(listSize(final_list)))
    print("====="*20)
    if size is None:
        print('Busque una plataforma válida')
    else:
        if size < 6:
            out_n = size
        else:
            out_n = 6
        print('Los últimos {0} videojuegos son...'.format(out_n))
        for game in lt.iterator(final_list):

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


def printR2(num_records, size, final_list, player):
    print("====="*20)
    print('la plataforma {0} tiene un total de {1} videojuegos'.format(player, size))
    #print('Released games between dates{0}'.format(listSize(num_records)))
    print("====="*20)

    if num_records is None:
        print('Busque  un nombre válido')
    else:
        if num_records < 5:
            out_n = num_records
        else:
            out_n = 5
        print('Los records {0} son...'.format(out_n))
        for record in lt.iterator(final_list):

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


def printR3(final_list, size, min_runs, max_runs):

    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} intentos y {2} intentos'.format(size, min_runs, max_runs))
    print("====="*20)
    print('Attempts between range {0} '.format(listSize(final_list)))
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
        else:
            out_n = 6
        print('Los records {0} son...'.format(out_n))
        for record in lt.iterator(final_list):

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


def printR4(final_list, size, min_date, max_date):
    size = lt.size(final_list)
    print("====="*20)
    print('Hay un total de {0} intentos de speedruns entre {1} y {2}'.format(size, min_date, max_date))
    print("====="*20)
    print('Attempts between range {0} '.format(listSize(final_list)))
    if size is None:
        print('Busque con una plataforma válida')
    else:
        if size < 6:
            out_n = size
        else:
            out_n = 6
        print('Los últimos {0} records son...'.format(out_n))
        for record in lt.iterator(final_list):

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


def printR5(sorted_list, size, min_time, max_time):
    
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
        print('Los últimos {0} records de más lento a más rápido son...'.format(out_n))
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

def printR6(dic):
    tabla = [["bin", "count", "lvl", "mark"]]
    keys = list(dic.keys())
    for llave in keys:
        fila = ["("+str(round(llave[0], 3))+", "+str(round(llave[1],3))+"]", str(dic[llave]["count"]), str(dic[llave]["lvl"]), dic[llave]["mark"]]
        pds = pd.Series(fila).str.wrap(30)
        tabla.append(pds)
    print(tabulate.tabulate(tabla, tablefmt="grid"))

    
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

        sorted_list, size, time, memory = controller.Call_Req1(analyzer, platform, min_date, max_date)

        printR1(sorted_list, size, platform, min_date, max_date)
        printTimeMemory(time, memory)

    elif inputs == "2":
        player = input('Ingrese el nombre del jugador: ')

        records_list, n_records, size, time, memory= controller.Call_Req2(analyzer, player)

        printR2(n_records, size, records_list, player)
        printTimeMemory(time, memory)
    
    elif inputs == "3":
        min_attempts = int(input('ingrese el límite inferior de intentos: '))
        max_attempts = int(input('ingrese el límite superior  de intentos: '))

        sorted_list, size, time, memory = controller.Call_Req3(analyzer, min_attempts, max_attempts)

        printR3(sorted_list, size, min_attempts, max_attempts)
        printTimeMemory(time, memory)

    elif inputs == "4":
        min_date_4 = input('ingrese el límite inferior de la fecha: ')
        max_date_4 = input('Ingrese el límite superior de la fecha: ')

        sorted_list, size, time, memory = controller.Call_Req4(analyzer, min_date_4, max_date_4)

        printR4(sorted_list, size, min_date_4, max_date_4)
        printTimeMemory(time, memory)

    elif inputs == "5":
        min_time = float(input('ingrese la duración mínima: '))
        max_time = float(input('ingrese la duración máxima: '))

        sorted_list, size, time, memory = controller.Call_Req5(analyzer, min_time, max_time)

        printR5(sorted_list, size, min_time, max_time)
        printTimeMemory(time, memory)

    elif inputs == "6":
        min_date = realDate(input("Ingrese el límite inferior de fecha de lanzamiento: "))
        max_date = realDate(input("Ingrese el Límite superior de fecha de lanzamiento: "))
        N = int(input("Ingrese número de segmentos en que se divide el rango de propiedad en el histograma (N): "))
        x = int(input("Ingrese número de niveles en que se dividen las marcas de juegos en el histograma (x): "))
        propiedad = input("Ingrese propiedad de la cual se va a hacer el histograma (Time_0 , Time_1, Time_2, Time_Avg, Num_Runs :")
        req6, time, memory = controller.Call_req6(analyzer,min_date,max_date,propiedad,N,x,)
        diccionario = req6[0]
        total = req6[1]
        llave_min, llave_max = req6[2], req6[3]
        print("\n=============== Req No. 6 Inputs ===============")
        print("Count map (histogram) of:", propiedad)
        print("Number of bins:", N)
        print("scale:", x)
        print("\n=============== Req No. 6 Answer ===============")
        print("There are", req6[5], "(", total, ")" "players on record.")
        print("The histogram counts", total, "juegos.")
        print("The minimum and maximum value of property", propiedad, "is:", llave_min, "and", llave_max)
        print(propiedad, "Histogram with", N, "bins and", x, "players per lvl mark.")
        printR6(diccionario)
        print("NOTE: Each '*' represents",x,"attempts.")

    else:
        sys.exit(0)
sys.exit(0)
