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
Se define la estructura de un catálogo de videojuegos.
"""

# ___________________________________________________
# Construccion de modelos
# ___________________________________________________


def new_analyzer():
    analyzer = { 
                "category_data": None,
                'game_data': None,
                "Req1_VideogamesByRangeDate": None,
                'Req2_RegistersByShorterTime': None,
                "Req3_FastestRegistersByAttempts":None,
                "Req4_SlowRegistersbyDates" : None,
                "Req5_RecentRegistersRecord":None,
                "Req6_HistogramRegistersbyYears":None,
                "Req7_TopNVideogames":None

    }

    #================[Listas Generales]=====================
    analyzer["category_data"] = lt.newList("ARRAY_LIST")
    analyzer["games_data"] = lt.newList("ARRAY_LIST")

    analyzer['Req1_VideogamesByRangeDate'] =  om.newMap(omaptype="RBT")

    analyzer["Req2_RegistersByShorterTime"] = om.newMap(omaptype="RBT")

    analyzer['Req3_FastestRegistersByAttempts'] = om.newMap(omaptype="RBT")

    analyzer["Req4_SlowRegistersbyDates"] = om.newMap(omaptype="RBT")

    analyzer['Req5_RecentRegistersRecord']   = om.newMap(omaptype="RBT")
     
    analyzer["Req6_HistogramRegistersbyYears"] = mp.newMap(numelements=100000,
                                            maptype='PROBING', 
                                            loadfactor=0.5)

    analyzer["Req7_TopNVideogames"] = mp.newMap(numelements=100000,
                                            maptype='PROBING', 
                                            loadfactor=0.5)                    
    return analyzer 


# ___________________________________________________
# Funciones para agregar informacion al analyzer
# __________________________________________________

    #================[Añadido de archivo game]=====================
def AddGameData(analyzer, game):
    #Carga a estructuras de datos para cada requerimiento

    R1_carga(analyzer, game)

    #Agregar a la lista general de games, en este caso para el R1.

    lt.addLast(analyzer["games_data"], game)

    #================[Añadido de archivo category]=====================
"""
def NameById(analyzer, record):
    data = analyzer["games_data"]
    name_by_Id = mp.newMap(numelements=100000,
                        prime=109345121,
                        maptype='PROBING', 
                        loadfactor=0.5,
                        comparefunction=None)
    for game in lt.iterator(data):
        if game["Game_Id"] == record["Game_Id"]:
            name_by_Id.put(data, record["Game_Id"],game["Name"])
    return name_by_Id

"""
def AddRecordData(analyzer, record):
 
    for game in lt.iterator(analyzer["games_data"]):
        if game["Game_Id"] == record["Game_Id"]:
            record["Game_Id"] = game["Name"]
    #Carga a estructuras de datos para cada requerimiento
    R2_carga(analyzer, record)
    R3_carga(analyzer, record)
    R4_carga(analyzer, record)
    R5_carga(analyzer, record)
    #Agregar a la lista general de records
    lt.addLast(analyzer["category_data"], record)


# ___________________________________________________
# Funciones para creacion de datos
# ___________________________________________________

#=^..^=   [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=

def R1_carga(analyzer, game):
    if game['Release_Date'] != '':
        Release_Date = CompleteDate(game['Release_Date'])
        exist_platform = om.get(analyzer["Req1_VideogamesByRangeDate"], Release_Date)

        if exist_platform is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(analyzer["Req1_VideogamesByRangeDate"], Release_Date, new_list)
            
        else: 
            new_list = me.getValue(exist_platform)
        lt.addLast(new_list, game)

        
#=^..^=   [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=

def R2_carga(analyzer, record):
    if record['Players_0'] != '':

        player_list = record["Players_0"].split(",")
        for player in player_list:
            player = player.strip(" ")
                
            exist_player = om.get(analyzer["Req2_RegistersByShorterTime"], player)

            if exist_player is None:
                new_list = lt.newList(datastructure = "ARRAY_LIST")
                om.put(analyzer["Req2_RegistersByShorterTime"], player, new_list)
            else: 
                new_list = me.getValue(exist_player)
            lt.addLast(new_list, record)

#=^..^=   [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=

def R3_carga(analyzer, record):
    if record['Num_Runs'] != '':

        num_runs = int(record["Num_Runs"])
        exist_runs = om.get(analyzer["Req3_FastestRegistersByAttempts"], num_runs)

        if exist_runs is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(analyzer["Req3_FastestRegistersByAttempts"], num_runs, new_list)
        else: 
            new_list = me.getValue(exist_runs)
        lt.addLast(new_list, record)


#=^..^=   [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=

def R4_carga(analyzer, record):
    if record['Record_Date_0'] != '':

        record_date = record["Record_Date_0"]
        exist_date = om.get(analyzer["Req4_SlowRegistersbyDates"], record_date)

        if exist_date is None:
            new_list = lt.newList(datastructure = "ARRAY_LIST")
            om.put(analyzer["Req4_SlowRegistersbyDates"], record_date, new_list)
                
        else: 
            new_list = me.getValue(exist_date)
        lt.addLast(new_list, record)


#=^..^=   [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=

def R5_carga(analyzer, record):
    if record['Time_0'] != '':

        record_time = float(record["Time_0"])
        exist_time = om.get(analyzer["Req5_RecentRegistersRecord"], record_time)

        if exist_time is None:
            new_list =  lt.newList(datastructure = "ARRAY_LIST")
            om.put(analyzer["Req5_RecentRegistersRecord"], record_time, new_list)
        else: 
            new_list = me.getValue(exist_time)
        lt.addLast(new_list, record)

#=^..^=   [Requerimiento 6]  =^..^=    =^..^=    =^..^=    =^..^=
#=^..^=   [Requerimiento 7]  =^..^=    =^..^=    =^..^=    =^..^=

# ___________________________________________________
# Funciones genericas
# ___________________________________________________

def sortList(list, cmp_function):
    return insertion.sort(list, cmp_function)

def subList(list, pos, len):
    return lt.subList(list, pos, len)

def listSize(list):
    return lt.size(list)

def mapSize(map):
    return mp.size(map)

def treeSize(tree):
    return om.size(tree)

# ___________________________________________________
# Funciones de consulta
# ___________________________________________________


#=^..^=   [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
                      
def Req1_VideogamesByRangeDate(analyzer, platform, min_date, max_date):
    map1 = analyzer["Req1_VideogamesByRangeDate"]
    lst = om.values(map1, min_date, max_date)
    games_by_platform = lt.newList(datastructure = "ARRAY_LIST")
    for lst_games in lt.iterator(lst):
        for game in lt.iterator(lst_games):
            if platform in game["Platforms"]:
                lt.addLast(games_by_platform, game)
    sorted_list_1 = sortList(games_by_platform, cmp_Req1)
    sorted_list = FirstandLast(sorted_list_1)
    return sorted_list



#=^..^=   [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
                    
def R2_player_records(analyzer, player):
    existRecords = om.get(analyzer['Req2_RegistersByShorterTime'], player)  
    #contención de error
    if (existRecords is None):
        return None
    list_values = existRecords['value']                       
    n_records = listSize(list_values)                   
    records_list_1 = sortList(list_values, cmp_Req2)
    if lt.size(records_list_1) >= 5:
        first_five_players = subList(records_list_1, 1, 5)
        return first_five_players, n_records
    else:
        return records_list_1, n_records
    
    

#=^..^=   [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
                      
def Req3_FastestRegistersByAttempts(analyzer, min_time, max_time):
    map_analyzer = analyzer["Req3_FastestRegistersByAttempts"]
    list_ = om.values(map_analyzer, min_time, max_time)
    fastest_records = lt.newList(datastructure = "ARRAY_LIST")
    for record in lt.iterator(list_):
        for finalRecord in lt.iterator(record):
            lt.addLast(fastest_records, finalRecord)
    sorted_list = sortList(fastest_records, cmp_Req3and4)
    final_list = FirstandLast(sorted_list)
    return final_list


#=^..^=   [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=

def Req4_SlowRegistersbyDates(analyzer, min_date, max_date):                   
    map_analyzer = analyzer["Req4_SlowRegistersbyDates"]
    lst = om.values(map_analyzer, min_date, max_date)
    date_records = lt.newList(datastructure = "ARRAY_LIST")
    for record_date in lt.iterator(lst):
        for final_record in lt.iterator(record_date):
            lt.addLast(date_records, final_record)
    sorted_list_1 = sortList(date_records, cmp_Req3and4)
    sorted_list = FirstandLast(sorted_list_1)
    return sorted_list

#=^..^=   [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=

def Req5_RecentRegistersRecord(analyzer, min_time, max_time):                   
    map_analyzer = analyzer["Req5_RecentRegistersRecord"]
    lst = om.values(map_analyzer, min_time, max_time)
    time_records = lt.newList(datastructure = "ARRAY_LIST")
    for record_time in lt.iterator(lst):
        for final_record in lt.iterator(record_time):
            lt.addLast(time_records, final_record)
    sorted_list = sortList(time_records, cmp_Req5)
    final_list = FirstandLast(sorted_list)
    return final_list



# ___________________________________________________
# Funciones utilizadas para comparar elementos dentro de una lista
# ___________________________________________________


    #=================[R1]=================
def cmp_Req1(game1, game2):
    Release_Date_1 = CompleteDate(game1['Release_Date'])
    Release_Date_2 = CompleteDate(game2['Release_Date'])

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
    
def cmp_Req2(record1, record2):

    Record_Date_1 = record1['Record_Date_0'][:10]
    Record_Date_2 = record2['Record_Date_0'][:10]

    Record_Date_1 = realDate(Record_Date_1)
    Record_Date_2 = realDate(Record_Date_2)
    
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

def cmp_Req3and4(record1, record2):

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
            
def cmp_Req5(record1, record2):

    Default = False 

    if (record1['Record_Date_0']) > (record2['Record_Date_0']) or (record1['Record_Date_0']) < (record2['Record_Date_0']):
        Default = True 
    elif  (record1['Record_Date_0']) == (record2['Record_Date_0']):
        if (record1['Num_Runs']) < (record2['Num_Runs']) or (record1['Num_Runs']) > (record2['Num_Runs']):
            Default = True 
        elif  (record1['Num_Runs']) == (record2['Num_Runs']):
            if (record1['Game_Id']) > (record2['Game_Id']) or (record1['Game_Id']) < (record2['Game_Id']):
                Default = True
            else: 
                Default = False
    return Default

#def cmp_Req5(record1, record2):
#def cmp_Req5(record1, record2):

# ___________________________________________________
# Funciones Adicionales
# ___________________________________________________

def CompleteDate(string): 
    if int(string[:2]) <= 22:
        año = "20" + string[:2]
        fecha = año + string[2:]
    elif int(string[:2]) > 22: 
        año = "19" + string[:2]
        fecha = año + string[2:]

    return dt.strptime(fecha, "%Y-%m-%d").date()


def realDate(string): 
    return dt.strptime(string, "%Y-%m-%d").date()
    
def FirstandLast(lista):
    sizelista = lt.size(lista)
    if sizelista <=6:
        df = (lista)
        return df
    first_3 = subList(lista,1, 3)
    last_3 = subList(lista,sizelista-3, 3)
    listafinal = lt.newList("ARRAY_LIST")
    for i in lt.iterator(first_3):
        lt.addLast(listafinal, i) 
    for a in lt.iterator(last_3):
        lt.addLast(listafinal, a)
    df=(listafinal)
    return df

# ___________________________________________________
# Funciones Lab 9
# ___________________________________________________

def indexHeight(analyzer):
    """
    Altura del árbol
    """
    return om.height(analyzer)


def indexSize(analyzer):
    """
    Número de elementos en el indice
    """
    return treeSize(analyzer)

