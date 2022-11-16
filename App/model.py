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
from statistics import mean
from math import log
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

    #Agregar a la lista general de juegos

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

def R6_carga(analyzer, game):
    if game['Release_Date'] != '':
        Release_Date = CompleteDate(game['Release_Date'])
        exist_date = om.contains(analyzer["Req6_HistogramRegistersbyYears"], int(Release_Date.year))

        if exist_date:
            get = om.get(analyzer["Req6_HistogramRegistersbyYears"],int(Release_Date.year))
            value_get =me.getValue(get)
            lt.addLast(value_get,game)
            
        else: 
            lista = lt.newList(datastructure='ARRAY_LIST')
            om.put(analyzer['Req6_HistogramRegistersbyYears'],int(Release_Date.year),lista)
            get = om.get(analyzer['Req6_HistogramRegistersbyYears'],int(Release_Date.year))
            value_get = me.getValue(get)
            lt.addLast(value_get,game)
#=^..^=   [Requerimiento 7]  =^..^=    =^..^=    =^..^=    =^..^=
def R7_carga(analyzer,game):

    platforms= game['Platforms']
    platforms= platforms.split(', ')
    for platform in platforms:
        exist= om.contains(analyzer['Req7_TopNVideogames'],platform)  

        if exist: 
            entry= om.get(analyzer['Req7_TopNVideogames'],platform)
            rev=me.getValue(entry)
            lt.addLast(rev,game)

        else:
            lista=lt.newList(datastructure='ARRAY_LIST')
            om.put(analyzer['Req7_TopNVideogames'],platform,lista)
            entry= om.get(analyzer['Req7_TopNVideogames'],platform)
            rev=me.getValue(entry)
            lt.addLast(rev,game)
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
    lst = om.values(map1, min_date, max_date)                     #O(logn)
    games_by_platform = lt.newList(datastructure = "ARRAY_LIST")  #O(1)

    for lst_games in lt.iterator(lst):                            #O(n^2)
        for game in lt.iterator(lst_games):
            if platform in game["Platforms"]:
                lt.addLast(games_by_platform, game)               #O(n^2)

    sorted_list = sortList(games_by_platform, cmp_Req1)           #O(n^2)
    final_list = FirstandLast(sorted_list)                        #O(n^2)
    return final_list, listSize(sorted_list)                      #La complejidad se resume en el ordenamiento con insertion O(n^2)



#=^..^=   [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
                    
def R2_player_records(analyzer, player):
    existRecords = om.get(analyzer['Req2_RegistersByShorterTime'], player)   #O(logn)
    #contención de error
    if (existRecords is None):
        return None
    list_values = existRecords['value']                                       #O(1)            
    Num_records = listSize(list_values)                                       #O(1)
    final_list = sortList(list_values, cmp_Req2)                              #O(n^2)
    if lt.size(final_list) >= 5:
        first_five_players = subList(final_list, 1, 5)                        #O(1)
        return first_five_players, Num_records, listSize(final_list)
    else:
        return final_list, Num_records, listSize(final_list)                  #La complejidad se resume en el ordenamiento con insertion 
                                                                              #O(n^2)            
    
    

#=^..^=   [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
                      
def Req3_FastestRegistersByAttempts(analyzer, min_time, max_time):
    map_analyzer = analyzer["Req3_FastestRegistersByAttempts"]
    list_ = om.values(map_analyzer, min_time, max_time)                     #O(logn)
    fastest_records = lt.newList(datastructure = "ARRAY_LIST")              #O(1)

    for record in lt.iterator(list_):                                       #O(n^2)
        for finalRecord in lt.iterator(record):
            lt.addLast(fastest_records, finalRecord)                        #O(1)

    sorted_list = sortList(fastest_records, cmp_Req3and4)                   #O(n^2)
    final_list = FirstandLast(sorted_list)                                  #O(n^2)
    return final_list, listSize(sorted_list)                                #La complejidad se resume en el ordenamiento con insertion O(n^2)            
    


#=^..^=   [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=

def Req4_SlowRegistersbyDates(analyzer, min_date, max_date):                   
    map_analyzer = analyzer["Req4_SlowRegistersbyDates"]                   
    lst = om.values(map_analyzer, min_date, max_date)                       #O(logn)
    
    date_records = lt.newList(datastructure = "ARRAY_LIST")                 #O(1)
    for record_date in lt.iterator(lst):                                    #O(n^2)
        for final_record in lt.iterator(record_date):
            lt.addLast(date_records, final_record)                          #O(1)
    
    sorted_list= sortList(date_records, cmp_Req3and4)                       #O(n^2)
    final_list = FirstandLast(sorted_list)                                  #O(n^2)
    return final_list, listSize(sorted_list)                                #La complejidad se resume en el ordenamiento con insertion O(n^2)            

#=^..^=   [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=

def Req5_RecentRegistersRecord(analyzer, min_time, max_time):                   
    map_analyzer = analyzer["Req5_RecentRegistersRecord"]
    lst = om.values(map_analyzer, min_time, max_time)                      #O(logn)
    
    time_records = lt.newList(datastructure = "ARRAY_LIST")                #O(1)
    for record_time in lt.iterator(lst):                                   #O(n^2)
        for final_record in lt.iterator(record_time):
            lt.addLast(time_records, final_record)                         #O(1)
    
    sorted_list = sortList(time_records, cmp_Req5)                         #O(n^2)
    final_list = FirstandLast(sorted_list)                                 #O(n^2)
    return final_list, listSize(sorted_list)                               #La complejidad se resume en el ordenamiento con insertion O(n^2)            

#=^..^=   [Requerimiento 6]  =^..^=    =^..^=    =^..^=    =^..^=
def YearsHistogram(analyzer,max_date,min_date,propiedad):
    dates = analyzer['Req6_HistogramRegistersbyYears']
    ranges = om.keys(dates,min_date,max_date)

    if propiedad == 'time_0':
        tiempos = om.newMap(omaptype='BST',comparefunction=cmp_Req6)
        for i in lt.iterator(ranges): 
            information = i['value']
            for j in information:
                game = SearchGame(analyzer,j)
                om.put(tiempos,game['Time_0'],game)
        return tiempos

    elif propiedad == 'time_1':
        tiempos = om.newMap(omaptype='BST',comparefunction=cmp_Req6)
        for i in lt.iterator(ranges): 
            information = om.get(dates,i)
            information = information['value']['elements']
            for j in information:
                game = SearchGame(analyzer,j)
                tiempo = tiempo = float(game['Time_1'].strip() or 0)
                if tiempo != 0 or tiempo != '':
                    om.put(tiempos,tiempo,game)
        return tiempos

    elif propiedad == 'time_2':
        tiempos = om.newMap(omaptype='BST',comparefunction=cmp_Req6)
        for i in lt.iterator(ranges): 
            information = om.get(dates,i)
            information = information['value']['elements']
            for j in information:
                game = SearchGame(analyzer,j)
                tiempo = tiempo = float(game['Time_2'].strip() or 0)
                if tiempo != 0 or tiempo != '':
                    om.put(tiempos,tiempo,game)
        return tiempos

    elif propiedad == 'time_avg':
        tiempos = om.newMap(omaptype='BST',comparefunction=cmp_Req6)
        for i in lt.iterator(ranges): 
            information = om.get(dates,i)
            information = information['value']['elements']
            for j in information:
                game = SearchGame(analyzer,j)
                avg = PromediosTime(game)
                om.put(tiempos,avg,game)
        return tiempos

    elif propiedad == 'num_runs':
        runs = om.newMap(omaptype='BST',comparefunction=cmp_Req6)
        for i in lt.iterator(ranges): 
            information = om.get(dates,i)
            information = information['value']['elements']
            for j in information:
                runs_avg = int(j['Num_Runs'])
                om.put(runs,runs_avg,j)
        return runs

    else:
        return None

def histogram(analyzer,max_date,min_date,propiedad,n,x):
    ADT = YearsHistogram(analyzer,max_date,min_date,propiedad)
    if ADT != None:
        ranges = (om.maxKey(ADT))-(om.minKey(ADT))
        interval= round(ranges/n,2)
        
        histograms = {}

        i=1
        low = round(om.minKey(ADT),2)
        maxim =0
        while i <= n:
            if i!=n:
                maxim=low+interval
                maxim = round(maxim,2)
                bins = str(low)+'-'+str(maxim)
                low = maxim
                histograms[bins] = 0
            else:
                maxim = round(om.maxKey(ADT),2)
                bins = str(low)+'-'+str(maxim)
                histograms[bins] = 0
            i+=1

        keys = om.keySet(ADT) 
        histograms =counters(histograms,keys)  
        histograms =counterslevelmarks(histograms,x) 

        minim =round(om.minKey(ADT),2)
        maximo =round(om.maxKey(ADT),2)

        return histograms,om.size(ADT),minim,maxim

    else:
        return None

def counters(histograms,keys):

    for x in lt.iterator(keys):
        x =round(x,2)
        i=0
        encontrado = True
        ranges = sorted(histograms)
        while (i <= len(ranges)) and encontrado:
            comparation = ranges[i].split('-')
            if x >= float(comparation[0]) or x < float(comparation[1]):
                histograms[ranges[i]]+=1
                encontrado=False
            i+=1
    return histograms

def counterslevelmarks(histograms,x):
    answer = {}

    for i in sorted(histograms):
        level = histograms[i]//x
        answer[i]=(histograms[i],level)
    return answer

#=^..^=   [Requerimiento 7]  =^..^=    =^..^=    =^..^=    =^..^=
def retransmi(analyzer,games,pt):

    retransTree= om.newMap(omaptype='BST',
                        comparefunction=cmp_Req7)
    notMisc=0
    for game in games:
        x= SearchGame(analyzer,game)
        
        if x['Misc'] == 'False':

            notMisc+=1

            Antiguedad = Antiq(game)
            popular = popularies(game)
            Promtime= PromediosTime(x)

            rest = (popular*Promtime)/Antiguedad
            rest = round(rest,2)

            runs = int(game['Total_Runs'])

            mercado = runs/pt  
            mercado = round(mercado,2)

            streamMercado = mercado*rest
            streamMercado = round(streamMercado,2)


            om.put(retransTree,streamMercado,game)

    return retransTree,notMisc

def SearchGame(analyzer,game):

    encontrado = None
    
    for  names in analyzer['category_data']['elements']:
        name = names['Game_Id']
        if game['Name']== name:
            encontado = names
    return encontado

def Antiq(game):
    release_Date = CompleteDate(game['Release_Date'])
    #year=str(releaseDate.year) 
    release_Date=int(release_Date.year)

    if release_Date >=2018:
        return release_Date - 2017
    elif 1998 < release_Date < 2018:
        return ((-1/5)*release_Date) + 404.6
    else:
        return 5

def popularies(game):
    return log(int(game['Total_Runs']))

def PromediosTime (game):

    tiempos = lt.newList(datastructure='ARRAY_LIST')
    i=0
    while i<=2:
       iterator='Time_'+str(i)
       tiempo = float(game[iterator].strip() or 0)
       lt.addLast(tiempos,tiempo)
       i+=1
    tiempos = tiempos['elements']

    return mean(tiempos)

def topN(analyzer,platform,N):
    exist_map = mp.contains(analyzer['Req7_TopNVideogames'],platform)

    if exist_map:
        entry= mp.get(analyzer['Req7_TopNVideogames'],platform)
        plat =me.getValue(entry)
        size = lt.size(plat)
        pt = total(plat)

        rest,notMisc= retransmi(analyzer,plat['elements'],pt)

        tops = lt.newList(datastructure='ARRAY_LIST')

        i=1
        while i <= N:
            maxim = om.maxKey(rest)
            maxim = om.get(rest,maxim)
            lt.addLast(tops,maxim)
            om.deleteMax(rest)

            i+=1
        
        return tops,size,notMisc

    else:
        return None

def total(games):
    pt=0
    for game in games['elements']:
        pt += int(game['Total_Runs'])
    return pt

# ___________________________________________________
# Funciones utilizadas para comparar elementos dentro de una lista
# ___________________________________________________


    #=================[R1]=================
def cmp_Req1(game1, game2):
    #Se completan las fechas puesto que en el CSV estan en formato AA-MM-DD y se recibe una fecha AAAA-MM-DD

    Release_Date_1 = CompleteDate(game1['Release_Date'])
    Release_Date_2 = CompleteDate(game2['Release_Date'])

    if (Release_Date_1 < Release_Date_2) or ((Release_Date_1) > Release_Date_2):
            Value = True
    elif  (Release_Date_1) == (Release_Date_2):
        if (game1['Abbreviation']) < (game2['Abbreviation']) or (game1['Abbreviation']) > (game2['Abbreviation']):
            Value = True 
        elif  (game1['Abbreviation']) == (game2['Abbreviation']):
            if (game1['Name']) < (game2['Name']) or (game1['Name']) > (game2['Name']):
                    Value = True
            else: 
                Value = False
    return Value
    
def cmp_Req2(record1, record2):

    Record_Date_1 = realDate(record1['Record_Date_0'][:10])#Se extrae mediante un slice la fecha y posteriormente se pasa a formato datetime
    Record_Date_2 = realDate(record2['Record_Date_0'][:10])
    
    Value = False #Se inicializa en falso

    if (float(record1['Time_0']) < float(record2['Time_0'])) or (float(record1['Time_0']) > float(record2['Time_0'])):
            Value = True
    elif  (float(record1['Time_0']) == float(record2['Time_0'])):
        if (Record_Date_1) < (Record_Date_2) or (Record_Date_1) > (Record_Date_2):
            Value = True 
        elif  (Record_Date_1) == (Record_Date_2):
            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                    Value = True
            else: 
                Value = False
    return Value


def cmp_Req3and4(record1, record2):

    Value = False 

    if (float(record1['Time_0']) < float(record2['Time_0'])) or (float(record1['Time_0']) > float(record2['Time_0'])):
            Value = True
    elif  (float(record1['Time_0']) == float(record2['Time_0'])):
        if (record1['Record_Date_0']) < (record2['Record_Date_0']) or (record1['Record_Date_0']) > (record2['Record_Date_0']):
            Value = True 
        elif  (record1['Record_Date_0']) == (record2['Record_Date_0']):
            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                    Value = True
            else: 
                Value = False
    return Value
            
            
def cmp_Req5(record1, record2):

    Value = False 

    if (record1['Record_Date_0']) < (record2['Record_Date_0']) or (record1['Record_Date_0']) > (record2['Record_Date_0']):
        Value = True 

    elif  (record1['Record_Date_0']) == (record2['Record_Date_0']):

        if (record1['Num_Runs']) < (record2['Num_Runs']) or (record1['Num_Runs']) > (record2['Num_Runs']):
            Value = True 

        elif  (record1['Num_Runs']) == (record2['Num_Runs']):

            if (record1['Game_Id']) < (record2['Game_Id']) or (record1['Game_Id']) > (record2['Game_Id']):
                Value = True
            else: 
                Value = False
    return Value

def cmp_Req6(record1, record2):
    if record1==record2:
        return 0
    elif record1 > record2:
        return 1
    else:
        return-1
def cmp_Req7(record1, record2):
    if record1==record2:
        return 0
    elif record1 > record2:
        return 1
    else:
        return-1

# ___________________________________________________
# Funciones Adicionales
# ___________________________________________________

def CompleteDate(string): 
    "Mediante slices se extrae la fecha y se completa su año"
    if int(string[:2]) <= 22:
        año = "20" + string[:2]
        fecha = año + string[2:]
    elif int(string[:2]) > 22: 
        año = "19" + string[:2]
        fecha = año + string[2:]

    return dt.strptime(fecha, "%Y-%m-%d").date()


def realDate(string): 
    "Convierte un str de tipo AAAA-MM-DD en una fecha"
    return dt.strptime(string, "%Y-%m-%d").date()
    
def FirstandLast(lista):
    sizelista = lt.size(lista)
    if sizelista <=6:
        return lista
    else:
        first_3 = subList(lista,1, 3)
        last_3 = subList(lista,sizelista-2, 3)
        FinalList = lt.newList("ARRAY_LIST")
        for i in lt.iterator(first_3):
            lt.addLast(FinalList, i) 
        for a in lt.iterator(last_3):
            lt.addLast(FinalList, a)
        return FinalList

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