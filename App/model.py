"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from doctest import OutputChecker
from filecmp import cmp
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from datetime import datetime as dt
import math as ma


# Construccion de modelos

loadfactor = 0.5

# ___________________________________________________
#  Creacion del analyzer
# ___________________________________________________
def newAnalyzer():
    #Indices iniciales lab 9
    analyzer = { 
               "category_data": None,
               'game_data': None,
               "Req1_FivePlatformGames": None,

    }

    #================[Listas Generales]=====================
    analyzer["category_data"]    = lt.newList("ARRAY_LIST")
    analyzer["games_data"]    = lt.newList("ARRAY_LIST")

     #=================[R1]=================
    analyzer['Req1_FivePlatformGames'] = mp.newMap(numelements=100000,
                                      maptype='PROBING', 
                                      loadfactor=loadfactor)

    
                                    
    return analyzer 


"""Funciones para agregar informacion al analyzer"""

    #[Añadido de archivo game_data]



def add_game(analyzer, game):
    #Carga a estructuras de datos para cada requerimiento
    R1_platforms(analyzer, game)
    #Agregar a la lista general de games
    lt.addLast(analyzer["games_data"], game)

    #[Añadido de archivo category_data]

def add_record(analyzer, record):
    #Agregar a la lista general de records
    lt.addLast(analyzer["category_data"], record)

# ___________________________________________________
# Funciones para creacion de datos
# ___________________________________________________

    #=================[R1]=================
def R1_platforms(analyzer, game):
    platforms_list = game["Platforms"].split(",")
    for platform in platforms_list:
        platform = platform.strip(" ")
        
        exist_platform = mp.get(analyzer["Req1_FivePlatformGames"], platform)

        if exist_platform is None:
            new_rbt =  om.newMap(omaptype="RBT", comparefunction= cmp_r1)
            mp.put(analyzer["Req1_FivePlatformGames"], platform, new_rbt)
        
    ordered_map = mp.get(analyzer["Req1_FivePlatformGames"], platform)['value']
    llave_compuesta = (game["Abbreviation"], game['Release_Date'])
    om.put(ordered_map, llave_compuesta, game)

def cmp_r1(game1, game2):

    Abbreviation_1, Release_Date_1 = game1
    Abbreviation_2, Release_Date_2 = game2
    
    Release_Date_1 = Dates(Release_Date_1)
    Release_Date_2 = Dates(Release_Date_2)
    if Release_Date_1 > Release_Date_2:
        return 1
    elif Release_Date_1 < Release_Date_2:
        return -1
    elif Release_Date_1 == Release_Date_2:
     
        if Abbreviation_1 > Abbreviation_2:
            return 1
        elif Abbreviation_1 > Abbreviation_2:
            return -1
        elif Abbreviation_1 == Abbreviation_2:
            return 0




# ___________________________________________________
# Funciones de consulta (Ejecución de cada req)
# ___________________________________________________
    

    #=================[R1]=================
def R1_FiveGamesbyPlatform(analyzer, platform, min_date, max_date):
    exist_map = mp.get(analyzer["Req1_FivePlatformGames"],platform)

    if exist_map == None:
        return None, None
    
    RBT = exist_map["value"]

    low_key = ('',0, min_date)
    high_key = ( "zzzzzzzzzzzzzzzz", max_date)
    
    keys_in_range = om.keys(RBT,low_key, high_key)
    keys_in_range = correct_range(keys_in_range, min_date, max_date)

    list_games_keys = lt.newList("ARRAY_LIST")

    num_games = lt.size(keys_in_range)

    for i in range(1,7):
        if i < 4:
            games = lt.getElement(keys_in_range, i)
            lt.addFirst(list_games_keys, games) 
        else:
            game = lt.getElement(keys_in_range, num_games - (6-i))
            lt.addFirst(list_games_keys, game)

    list_games = lt.newList("ARRAY_LIST")
    
    for key in lt.iterator(list_games_keys):
        game = om.get(RBT, key)["value"]
        lt.addLast(list_games, game)

    #Lab9
    height = indexHeight(RBT)                          
    n_elements = indexSize(RBT)                        


    return list_games, num_games, height, n_elements

def correct_range(keys, min_date, max_date):
    
    list_good_elems = lt.newList("ARRAY_LIST")
    for key in lt.iterator(keys):
        min_date, max_date = key

        if key in range(int(min_date), int(max_date+1)):
                lt.addLast(list_good_elems, key)

    return list_good_elems 
    

# ___________________________________________________
# Funciones utilizadas para comparar elementos dentro de una lista
# ___________________________________________________


    #=================[R1]=================

# ___________________________________________________
# Funciones lab 9
# ___________________________________________________


def gamesSize(analyzer):
    """
    Número de games
    """
    return lt.size(analyzer["games_data"])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['Req1_FivePlatformGames'])


def indexSize(analyzer):
    """o
    Numero de elementos en el indice
    """
    return om.size(analyzer['Req1_FivePlatformGames'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['Req1_FivePlatformGames'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['Req1_FivePlatformGames'])

# ___________________________________________________
# Funciones adicionales
# ___________________________________________________



def Dates(string): 
    "Transforma el formato en el que está la fecha en el CSV"
    if int(string[:2]) <= 22:
        año = "20" + string[:2]
        fecha = año + string[2:]
    elif int(string[:2]) > 22: 
        año = "19" + string[:2]
        fecha = año + string[2:]

    return dt.strptime(fecha, "%Y-%m-%d").date()





