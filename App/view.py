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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#category_file = 
def printTiempo_Memoria(tiempo, memoria): 
    mensaje = "****  Tiempo [ms]: {0} | Memoria [kb]: {1}  ****".format(round(tiempo,2), round(memoria,2))
    print(mensaje)


def printHeightN(height, n_elements):
    print("====="*20)
    print('La altura del árbol del club es: {0} y tiene {1} elementos'.format(height, n_elements))

def printMenu():
    print("====="*20)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información en el catálogo.")
    print("  [R1]   1- Reportar las cinco adquisiciones más recientes de un club.")
    print("  [R2]   2- Reportar los games de cierta posición dentro de un rango de desempeño, potencial y salario.")
    print("  [R3]   3- Reportar los games dentro de un rango salarial y con cierta etiqueta.")
    print("  [R4]   4- Reportar los games con cierto rasgo característico y nacidos en un periodo de tiempo. ")
    print("  [R5]   5- Graficar el histograma de una propiedad para los games FIFA.")
    print("  [R6]   6- Encontrar posibles sustituciones para los games FIFA")
    print("         0- Salir")
    print("====="*20)

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

    print(">>>   Primeros 3 records cargados...   >>>")
    for pos_record in pos_for_prints_records:
        records = lt.getElement(analyzer["category_data"], pos_record)
        if int(records['Num_Runs']) == 0:
            pass
        else:
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
                " "*(40 - len(str(records['Players_0'])) -9)+ "tiempo record: " +  
                str(records["Time_0"]) + 

                "\n   Fecha del record: " + 
                str(records["Record_Date_0"]) +

                "\n"

            )
            if pos_record == 3:
                        print(">>>   Últimos 3 records cargados...   >>>")


    

analyzer = None


"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")

        analyzer = controller.init()

        time, memory = controller.load_data(analyzer)   

        printGamesAndRecords(analyzer)
        printTiempo_Memoria(time, memory)    
    
    elif inputs == "1":
        platform = input("Ingrese una plataforma: ")
        min_date = input("Ingrese límite inferior de fecha de lanzamiento: ")
        max_date = input("Ingrese límite inferior de fecha de lanzamiento: ")

        time, memory, list_games, num_games, height, n_elements = controller.CallReq1(analyzer, platform, min_date, max_date)

        if time == None:
            print("No se pudo realizar la operacion")
        else: 
            printR1(list_games, num_games)
            printTiempo_Memoria(time, memory)
            printHeightN(height, n_elements)
            


    else:
        sys.exit(0)
sys.exit(0)
