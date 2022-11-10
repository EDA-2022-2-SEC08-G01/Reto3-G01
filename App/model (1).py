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
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from datetime import datetime as dt

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

"""Construccion de modelos"""

def new_catalog():
    catalog = { 
                "category_data": None,
                'game_data': None,
                "R1_platforms_games": None,
                'R2_recent_reports': None,
                "R3_duration_attempts":None,
                "R4_duration_date" : None,
                "R5_recent_record_times":None,
                "R6_times_year":None,
                "R7_rentable_games":None

    }

    #================[Listas Generales]=====================
    catalog["category_data"] = lt.newList("ARRAY_LIST")
    catalog["games_data"] = lt.newList("ARRAY_LIST")

     #=================[R1]=================
    catalog['R1_platforms_games'] =  om.newMap(omaptype="RBT")

     #=================[R2]=================
    catalog["R2_recent_reports"] = om.newMap(omaptype="RBT")

     #=================[R3]=================
    catalog['R3_duration_attempts'] = om.newMap(omaptype="RBT")

     #=================[R4]=================
    catalog["R4_duration_date"] = om.newMap(omaptype="RBT")

     #=================[R5]=================
    catalog['R5_recent_record_times']   = om.newMap(omaptype="RBT")
     #=================[R6]=================
    catalog["R6_times_year"] = mp.newMap(numelements=100000,
                                            maptype='PROBING', 
                                            loadfactor=0.5)

     #=================[R7]=================
    catalog["R7_rentable_games"] = mp.newMap(numelements=100000,
                                            maptype='PROBING', 
                                            loadfactor=0.5)
                           
    return catalog 


"""Funciones para agregar informacion al catalogo"""

    #================[Añadido de archivo game]=====================
def add_game(catalog, game):
    #Carga a estructuras de datos para cada requerimiento
    R1_platforms(catalog, game)
    #Agregar a la lista general de games
    lt.addLast(catalog["games_data"], game)

    #================[Añadido de archivo category]=====================
def add_record(catalog, record):
    for game in lt.iterator(catalog["games_data"]):
        if game["Game_Id"] == record["Game_Id"]:
            record["Game_Id"] = game["Name"]
    #Carga a estructuras de datos para cada requerimiento
    R2_player_records(catalog, record)
    R3_duration_attempts(catalog, record)
    R4_duration_date(catalog, record)
    R5_recent_record_times(catalog, record)
    #Agregar a la lista general de records
    lt.addLast(catalog["category_data"], record)



"""Funciones para creacion de datos"""

    #=================[R1]=================
def R1_platforms(catalog, game):
    if game['Release_Date'] != '':
        Release_Date = str_to_date(game['Release_Date'])
        exist_platform = om.get(catalog["R1_platforms_games"], Release_Date)

        if exist_platform is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(catalog["R1_platforms_games"], Release_Date, new_list)
            
        else: 
            new_list = me.getValue(exist_platform)
        lt.addLast(new_list, game)

        

    #=================[R2]=================
def R2_player_records(catalog, record):
    if record['Players_0'] != '':

        player_list = record["Players_0"].split(",")
        for player in player_list:
            player = player.strip(" ")
                
            exist_player = om.get(catalog["R2_recent_reports"], player)

            if exist_player is None:
                new_list = lt.newList(datastructure = "ARRAY_LIST")
                om.put(catalog["R2_recent_reports"], player, new_list)
            else: 
                new_list = me.getValue(exist_player)
            lt.addLast(new_list, record)


def R3_duration_attempts(catalog, record):
    if record['Num_Runs'] != '':

        num_runs = int(record["Num_Runs"])
        exist_runs = om.get(catalog["R3_duration_attempts"], num_runs)

        if exist_runs is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(catalog["R3_duration_attempts"], num_runs, new_list)
        else: 
            new_list = me.getValue(exist_runs)
        lt.addLast(new_list, record)


    #=================[R4]=================

def R4_duration_date(catalog, record):
    if record['Record_Date_0'] != '':

        record_date = record["Record_Date_0"]
        exist_date = om.get(catalog["R4_duration_date"], record_date)

        if exist_date is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(catalog["R4_duration_date"], record_date, new_list)
                
        else: 
            new_list = me.getValue(exist_date)
        lt.addLast(new_list, record)


   #=================[R5]=================

def R5_recent_record_times(catalog, record):
    if record['Time_0'] != '':

        record_time = float(record["Time_0"])
        exist_time = om.get(catalog["R5_recent_record_times"], record_time)

        if exist_time is None:
            new_list =  lt.newList(datastructure = "ARRAY_LIST")
            om.put(catalog["R5_recent_record_times"], record_time, new_list)
        else: 
            new_list = me.getValue(exist_time)
        lt.addLast(new_list, record)

        

""""Funciones de consulta"""

    #=================[R1]=================
                      
def R1_answer(catalog, platform, min_date, max_date):
    map1 = catalog["R1_platforms_games"]
    lst = om.values(map1, min_date, max_date)
    games_by_platform = lt.newList(datastructure = "ARRAY_LIST")
    for lst_games in lt.iterator(lst):
        for game in lt.iterator(lst_games):
            if platform in game["Platforms"]:
                lt.addLast(games_by_platform, game)
    sorted_list_1 = insertion.sort(games_by_platform, cmp_r1)
    sorted_list = primerosYultimos(sorted_list_1)
    sizelista = lt.size(sorted_list_1)
    return sorted_list, sizelista

    #=================[R2]=================
                      
def R2_answer(catalog, player):

    exist_records = om.get(catalog['R2_recent_reports'], player)  

    
    #Contención de error
    if (exist_records is None):
        return None
    
    list_values = exist_records['value']                       
    n_records = lt.size(list_values)                   
    
    records_list_1 = insertion.sort(list_values, cmp_r2)
    records_list =  primerosYultimos(records_list_1)              
    
    return records_list, n_records

    #=================[R3]=================
                      
def R3_answer(catalog, min_runs, max_runs):
    map = catalog["R3_duration_attempts"]
    lst = om.values(map, min_runs, max_runs)
    fastest_records = lt.newList(datastructure = "ARRAY_LIST")
    for record in lt.iterator(lst):
        for final_record in lt.iterator(record):
            lt.addLast(fastest_records, final_record)
    sorted_list = insertion.sort(fastest_records, cmpfunction=cmp_r3and4)
    sizelista = lt.size(sorted_list)
    return sorted_list, sizelista



   #=================[R4]=================
def R4_answer(catalog, min_date, max_date):                   
    map = catalog["R4_duration_date"]
    lst = om.values(map, min_date, max_date)
    date_records = lt.newList(datastructure = "ARRAY_LIST")
    for record_date in lt.iterator(lst):
        for final_record in lt.iterator(record_date):
            lt.addLast(date_records, final_record)
    sorted_list_1 = insertion.sort(date_records, cmpfunction=cmp_r3and4)
    sorted_list = primerosYultimos(sorted_list_1)
    sizelista = lt.size(sorted_list_1)
    return sorted_list, sizelista

    #=================[R5]=================
def R5_answer(catalog, min_time, max_time):                   
    map = catalog["R5_recent_record_times"]
    lst = om.values(map, min_time, max_time)
    time_records = lt.newList(datastructure = "ARRAY_LIST")
    for record_time in lt.iterator(lst):
        for final_record in lt.iterator(record_time):
            lt.addLast(time_records, final_record)
    sorted_list_1 = insertion.sort(time_records, cmp_r5)
    sorted_list = primerosYultimos(sorted_list_1)
    sizelista = lt.size(sorted_list_1)
    return sorted_list, sizelista



"""Funciones utilizadas para comparar elementos dentro de una lista"""

    #=================[R1]=================
def cmp_r1(game1, game2):
    Release_Date_1 = str_to_date(game1['Release_Date'])
    Release_Date_2 = str_to_date(game2['Release_Date'])

    if (Release_Date_1 < Release_Date_2) or ((Release_Date_1) > Release_Date_2):
            Default = True
    elif  (Release_Date_1) == (Release_Date_2):
        if (game1['Abbreviation']) < (game2['Abbreviation']) or (game1['Abbreviation']) > (game2['Abbreviation']):
            Default = True 
        elif  (game1['Abbreviation']) == (game2['Abbreviation']):
            if (game1['Name']) < (game2['Name']) or (game1['Name']) > (game2['Name']):
                    Default = True
            else: 
                Default = False
    return Default
    
def cmp_r2(record1, record2):

    Record_Date_1 = record1['Record_Date_0'][:10]
    Record_Date_2 = record2['Record_Date_0'][:10]

    Record_Date_1 = str_to_date_2(Record_Date_1)
    Record_Date_2 = str_to_date_2(Record_Date_2)
    
    Default = False 

    if (float(record1['Time_0']) < float(record2['Time_0'])) or (float(record1['Time_0']) > float(record2['Time_0'])):
            Default = True
    elif  (float(record1['Time_0']) == float(record2['Time_0'])):
        if (Record_Date_1) < (Record_Date_2) or (Record_Date_1) > (Record_Date_2):
            Default = True 
        elif  (Record_Date_1) == (Record_Date_2):
            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                    Default = True
            else: 
                Default = False
    return Default

def cmp_r3and4(record1, record2):

    Default = False 

    if (float(record1['Time_0']) < float(record2['Time_0'])) or (float(record1['Time_0']) > float(record2['Time_0'])):
            Default = True
    elif  (float(record1['Time_0']) == float(record2['Time_0'])):
        if (record1['Record_Date_0']) < (record2['Record_Date_0']) or (record1['Record_Date_0']) > (record2['Record_Date_0']):
            Default = True 
        elif  (record1['Record_Date_0']) == (record2['Record_Date_0']):
            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                    Default = True
            else: 
                Default = False
    return Default
            
def cmp_r5(record1, record2):

    Default = False 

    if (record1['Record_Date_0']) < (record2['Record_Date_0']) or (record1['Record_Date_0']) > (record2['Record_Date_0']):
        Default = True 
    elif  (record1['Record_Date_0']) == (record2['Record_Date_0']):
        if (record1['Num_Runs']) < (record2['Num_Runs']) or (record1['Num_Runs']) > (record2['Num_Runs']):
            Default = True 
        elif  (record1['Num_Runs']) == (record2['Num_Runs']):
            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                Default = True
            else: 
                Default = False
    return Default
            

"""Funciones adicionales"""

def str_to_date(string): 
    if int(string[:2]) <= 22:
        año = "20" + string[:2]
        fecha = año + string[2:]
    elif int(string[:2]) > 22: 
        año = "19" + string[:2]
        fecha = año + string[2:]

    return dt.strptime(fecha, "%Y-%m-%d").date()


def str_to_date_2(string): 
    return dt.strptime(string, "%Y-%m-%d").date()
    
def primerosYultimos(lista):
    sizelista = lt.size(lista)
    if sizelista <=6:
        df = (lista)
        return df
    first_3 = lt.subList(lista,1, 3)
    last_3 = lt.subList(lista,sizelista-2, 3)
    listafinal = lt.newList("ARRAY_LIST")
    for i in lt.iterator(first_3):
        lt.addLast(listafinal, i) 
    for a in lt.iterator(last_3):
        lt.addLast(listafinal, a)
    df=(listafinal)
    return df

def indexHeight(analyzer):
    """
    Altura del árbol
    """
    return om.height(analyzer)


def indexSize(analyzer):
    """
    Número de elementos en el indice
    """
    return om.size(analyzer)

