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
from math import log
from statistics import mean
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
                "cat_game_data":None,
                "Req1_VideogamesByRangeDate": None,
                'Req2_RegistersByShorterTime': None,
                "Req3_FastestRegistersByAttempts":None,
                "Req4_SlowRegistersbyDates" : None,
                "Req5_RecentRegistersRecord":None,
                "Req6_Histrogram":None,
                "Req7_TopNVideogames":None,
                "Ayuda_Req6":None

    }

    #================[Listas Generales]=====================
    analyzer["category_data"] = lt.newList("ARRAY_LIST")
    analyzer["games_data"] = lt.newList("ARRAY_LIST")

    analyzer['Req1_VideogamesByRangeDate'] =  om.newMap(omaptype="RBT")

    analyzer["Req2_RegistersByShorterTime"] = om.newMap(omaptype="RBT")

    analyzer['Req3_FastestRegistersByAttempts'] = om.newMap(omaptype="RBT")

    analyzer["Req4_SlowRegistersbyDates"] = om.newMap(omaptype="RBT")

    analyzer['Req5_RecentRegistersRecord']   = om.newMap(omaptype="RBT")

    analyzer['Req6_Histrogram'] = om.newMap(omaptype="RBT",comparefunction=cmptime)

    analyzer["Req7_TopNVideogames"] = mp.newMap(numelements=100000,
                                            maptype='PROBING', 
                                            loadfactor=0.5)       
    analyzer["Ayuda_Req6"] = om.newMap(omaptype="RBT")       
    return analyzer 


# ___________________________________________________
# Funciones para agregar informacion al analyzer
# __________________________________________________

    #================[Añadido de archivo game]=====================
def AddGameData(analyzer, game):
    #Carga a estructuras de datos para cada requerimiento

    R1_carga(analyzer, game)
    R6_carga(analyzer, game)
    R7_carga(analyzer,game)

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

        player_lst = record["Players_0"].split(",")
        for player in player_lst:
            player = player.strip(" ")
                
            xst_player = om.get(analyzer["Req2_RegistersByShorterTime"], player)

            if xst_player is None:
                new_list = lt.newList(datastructure = "ARRAY_LIST")
                om.put(analyzer["Req2_RegistersByShorterTime"], player, new_list)
            else: 
                new_list = me.getValue(xst_player)
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
        Release_Date = str_2_date(game['Release_Date'])
        exist= om.contains(analyzer["Req6_Histrogram"], int(Release_Date.year))

        if exist:
            entry= om.get(analyzer["Req6_Histrogram"],int(Release_Date.year))
            year=me.getValue(entry)
            lt.addLast(year,game)
            
        else: 
            lsta=lt.newList(datastructure='ARRAY_LIST')
            om.put(analyzer['Req6_Histrogram'],int(Release_Date.year),lsta)
            entry= om.get(analyzer['Req6_Histrogram'],int(Release_Date.year))
            year=me.getValue(entry)
            lt.addLast(year,game)


        
#def Funcion_adicional(analyzer, record):
 #   if record["Game_Id"] != "":
  #      id = record["Game_Id"]
   #     exist_id = om.get(analyzer["Ayuda_Req6"], id)
#
  #      if exist_id is None:
 #           new_list = lt.newList(datastructure = "ARRAY_LIST")
   #         om.put(analyzer["Ayuda_Req6"], exist_id, new_list)
     #   else: 
    #        new_list = me.getValue(exist_id)
      #  lt.addLast(new_list, record)

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
    lst = om.values(map1, min_date, max_date)
    games_by_platform = lt.newList(datastructure = "ARRAY_LIST")
    for lst_games in lt.iterator(lst):
        for game in lt.iterator(lst_games):
            if platform in game["Platforms"]:
                lt.addLast(games_by_platform, game)
    sorted_list = sortList(games_by_platform, cmp_Req1)
    final_list = FirstandLast(sorted_list)
    return final_list, listSize(sorted_list)



#=^..^=   [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
                    
def R2_player_records(analyzer, player):
    existRecords = om.get(analyzer['Req2_RegistersByShorterTime'], player)  
    #contención de error
    if (existRecords is None):
        return None
    list_values = existRecords['value']                       
    Num_records = listSize(list_values)                   
    final_list = sortList(list_values, cmp_Req2)
    if lt.size(final_list) >= 5:
        first_five_players = subList(final_list, 1, 5)
        return first_five_players, Num_records, listSize(final_list)
    else:
        return final_list, Num_records, listSize(final_list)
    
    

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
    return final_list, listSize(sorted_list)


#=^..^=   [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=

def Req4_SlowRegistersbyDates(analyzer, min_date, max_date):                   
    map_analyzer = analyzer["Req4_SlowRegistersbyDates"]
    lst = om.values(map_analyzer, min_date, max_date)
    date_records = lt.newList(datastructure = "ARRAY_LIST")
    for record_date in lt.iterator(lst):
        for final_record in lt.iterator(record_date):
            lt.addLast(date_records, final_record)
    sorted_list= sortList(date_records, cmp_Req3and4)
    final_list = FirstandLast(sorted_list)
    return final_list, listSize(sorted_list)

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
    return final_list, listSize(sorted_list)

#=^..^=   [Requerimiento 6]  =^..^=    =^..^=    =^..^=    =^..^=
#def Req6_histograma_por_rango(analyzer, min_date, max_date, propiedad, N, x):
    map = analyzer["Req6_Histrogram"]
    lst = om.values(map, min_date, max_date)
    print(lst,"Re loco")
    map_ayuda = analyzer["Ayuda_Req6"]
    print(map_ayuda,"re loco papi")
    for i in lt.iterator(lst):
        for key in lt.iterator(i):
            id = key["Name"]
            contains = om.contains(map_ayuda,id)
            if contains == True:
                f = om.get(map_ayuda,id)
                for r in lt.iterator(f):
                    if propiedad == "Time_Avg":
                        Dic = {"Time_Avg": None}
                        tim0 = r["Time_0"]
                        tim1 = r["Time_1"]
                        tim2 = r["Time_2"]
                        Time_Ag = (tim0+tim1+tim2)/3
                        Dic["Time_Avg"] = Time_Ag
                        print(Dic)
                        lt.addLast(lst,Dic)
    #print((lst), "Re loco papi")
    games_by_propoperty =  om.newMap(omaptype="RBT")
    for lst_games in lt.iterator(lst):
        for game in lt.iterator(lst_games):
            if propiedad == "Time_Avg":
                Time0 = game["Time_0"]
                time1 = game["Time_1"]
                time2 = game["Time_2"]
                time_prom =(Time0+time1+time2)/3
                om.put(games_by_propoperty,time_prom, game)   
            elif game[propiedad] != "":
                om.put(games_by_propoperty,game[propiedad], game)
    llave_max = om.maxKey(games_by_propoperty)
    llave_min = om.minKey(games_by_propoperty)
    size = om,size(games_by_propoperty)
    num_elem = llave_max - llave_min
    # Tamaño de cada rango
    tam = num_elem / N

    # Armar los intervalos y buscar sus valores.
    total = 0
    n = 0
    min = llave_min
    max = llave_min + tam
    dic = {}
    while n < N:
        lista = om.values(games_by_propoperty, min, max)
        count = 0
        for lst_games in lt.iterator(lista):
            games2 = lt.getElement(lst_games, 1)
            if min != games2[propiedad]:
                count += lt.size(lst_games)
                total += lt.size(lst_games)

        dic[(min,max)] = {"count": count, "lvl": count//x, "mark": "* "*(count//x)}
        min = max 
        max += tam
        n += 1
    return dic, total, llave_min, llave_max, size




#def Req6_histograma_por_rango(analyzer, min_date, max_date, propiedad, N, x):
    map = analyzer["Req6_Histrogram"]
    lst = om.values(map, min_date, max_date)
    print((lst), "Re loco papi")
    games_by_propoperty =  om.newMap(omaptype="RBT")
    for lst_games in lt.iterator(lst):
        for game in lt.iterator(lst_games):
            if propiedad == "Time_Avg":
                Time0 = game["Time_0"]
                time1 = game["Time_1"]
                time2 = game["Time_2"]
                time_prom =(Time0+time1+time2)/3
                om.put(games_by_propoperty,time_prom, game)   
            elif game[propiedad] != "":
                om.put(games_by_propoperty,game[propiedad], game)
    llave_max = om.maxKey(games_by_propoperty)
    llave_min = om.minKey(games_by_propoperty)
    size = om,size(games_by_propoperty)
    num_elem = llave_max - llave_min
    # Tamaño de cada rango
    tam = num_elem / N

    # Armar los intervalos y buscar sus valores.
    total = 0
    n = 0
    min = llave_min
    max = llave_min + tam
    dic = {}
    while n < N:
        lista = om.values(games_by_propoperty, min, max)
        count = 0
        for lst_games in lt.iterator(lista):
            games2 = lt.getElement(lst_games, 1)
            if min != games2[propiedad]:
                count += lt.size(lst_games)
                total += lt.size(lst_games)

        dic[(min,max)] = {"count": count, "lvl": count//x, "mark": "* "*(count//x)}
        min = max 
        max += tam
        n += 1
    return dic, total, llave_min, llave_max, size


def rgstrInYears(analyzer,max_date,min_date,propiedad):
    years= analyzer['Req6_Histrogram']
    interval= om.keys(years,min_date,max_date)

    if propiedad == 'time_0':
        times=om.newMap(omaptype='BST',comparefunction=cmptime)
        for i in lt.iterator(interval): 
            info=i['value']
            for j in info:
                game=findGame(analyzer,j)
                om.put(times,game['Time_0'],game)
        return times

    elif propiedad == 'time_1':
        times=om.newMap(omaptype='BST',comparefunction=cmptime)
        for i in lt.iterator(interval): 
            info= om.get(years,i)
            info=info['value']['elements']
            for j in info:
                game=findGame(analyzer,j)
                time= time= float(game['Time_1'].strip() or 0)
                if time != 0 or time != '':
                    om.put(times,time,game)
        return times

    elif propiedad == 'time_2':
        times=om.newMap(omaptype='BST',comparefunction=cmptime)
        for i in lt.iterator(interval): 
            info= om.get(years,i)
            info=info['value']['elements']
            for j in info:
                game=findGame(analyzer,j)
                time= time= float(game['Time_2'].strip() or 0)
                if time != 0 or time != '':
                    om.put(times,time,game)
        return times

    elif propiedad == 'time_avg':
        times=om.newMap(omaptype='BST',comparefunction=cmptime)
        for i in lt.iterator(interval): 
            info= om.get(years,i)
            info=info['value']['elements']
            for j in info:
                game=findGame(analyzer,j)
                add= promTime(game)
                om.put(times,add,game)
        return times

    elif propiedad == 'num_runs':
        tries= om.newMap(omaptype='BST',comparefunction=cmptime)
        for i in lt.iterator(interval): 
            info= om.get(years,i)
            info=info['value']['elements']
            for j in info:
                add=int(j['Num_Runs'])
                om.put(tries,add,j)
        return tries

    else:
        return None


def Req6_histograma_por_rango(analyzer, max_date, min_date, propiedad, N, x):
    map = rgstrInYears(analyzer,max_date,min_date,propiedad)
    if map != None:
        ran= (om.maxKey(map))-(om.minKey(map))
        interval= round(ran/N,2)
        
        hist={}

        i=1
        menor= round(om.minKey(map),2)
        mayor=0
        while i <= N:
            if i!=N:
                mayor=menor+interval
                mayor=round(mayor,2)
                bins= str(menor)+'-'+str(mayor)
                menor=mayor
                hist[bins]=0
            else:
                mayor=round(om.maxKey(map),2)
                bins= str(menor)+'-'+str(mayor)
                hist[bins]=0
            i+=1

        keys= om.keySet(map) 
        hist=count(hist,keys)  
        hist=countLvlmark(hist,x) 

        minim=round(om.minKey(map),2)
        maxim=round(om.maxKey(map),2)

        return hist,om.size(map),minim,maxim

    else:
        return None

def count(hist,keys):

    for k in lt.iterator(keys):
        k=round(k,2)
        i=0
        found=True
        intervals=sorted(hist)
        while (i <= len(intervals)) and found:
            comp= intervals[i].split('-')
            if k >= float(comp[0]) or k < float(comp[1]):
                hist[intervals[i]]+=1
                found=False
            i+=1
    return hist

def countLvlmark(hist,x):
    ans={}

    for i in sorted(hist):
        lvl= hist[i]//x
        ans[i]=(hist[i],lvl)
    return ans
    

#=^..^=   [Requerimiento 7]  =^..^=    =^..^=    =^..^=    =^..^=

def findGame(catalog,game):

    fnd=None
    
    for  Id in catalog['category_data']['elements']:
        name=Id['Game_Id']
        if game['Name']== name:
            fnd=Id
    return fnd

def Antiquity(game):
    releaseDate= str_2_date(game['Release_Date'])
    #year=str(releaseDate.year) 
    releaseDate=int(releaseDate.year)

    if releaseDate >=2018:
        return releaseDate - 2017
    elif 1998 < releaseDate < 2018:
        return ((-1/5)*releaseDate) + 404.6
    else:
        return 5

def howpopular(game):
    return log(int(game['Total_Runs']))

def promTime (game):

    times=lt.newList(datastructure='ARRAY_LIST')
    i=0
    while i<=2:
       iterator='Time_'+str(i)
       time= float(game[iterator].strip() or 0)
       lt.addLast(times,time)
       i+=1
    times= times['elements']

    return mean(times)

def R7_TOPN (analyzer,platform,N):
    exist=mp.contains(analyzer['Req7_TopNVideogames'],platform)

    if exist:
        entry= mp.get(analyzer['Req7_TopNVideogames'],platform)
        plat=me.getValue(entry)
        size= lt.size(plat)
        pt= totalTransmission(plat)

        rev,notMisc= revenue(analyzer,plat['elements'],pt)

        top= lt.newList(datastructure='ARRAY_LIST')

        i=1
        while i <= N:
            mayor= om.maxKey(rev)
            mayor= om.get(rev,mayor)
            lt.addLast(top,mayor)
            om.deleteMax(rev)

            i+=1
        
        return top,size,notMisc

    else:
        return None

def totalTransmission(games):
    pt=0
    for game in games['elements']:
        pt += int(game['Total_Runs'])
    return pt

def revenue(catalog,games,pt):

    rvTree= om.newMap(omaptype='BST',
                        comparefunction=cmpRevenue)
    notMc=0
    for game in games:
        x= findGame(catalog,game)
        
        if x['Misc']== 'False':

            notMc+=1

            Ant= Antiquity(game)
            popular= howpopular(game)
            avgTime= promTime(x)

            rev= (popular*avgTime)/Ant
            rev= round(rev,2)

            gt= int(game['Total_Runs'])

            marketShare= gt/pt  
            marketShare= round(marketShare,2)

            streamRevenue= marketShare*rev
            streamRevenue= round(streamRevenue,2)


            om.put(rvTree,streamRevenue,game)

    return rvTree,notMc
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

#def cmp_Req6(record1, record2):
#def cmp_Req7(record1, record2):

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
    first_3 = subList(lista,1, 3)
    last_3 = subList(lista,sizelista-2, 3)
    FinalList = lt.newList("ARRAY_LIST")
    for i in lt.iterator(first_3):
        lt.addLast(FinalList, i) 
    for a in lt.iterator(last_3):
        lt.addLast(FinalList, a)
    return FinalList
def findGame(catalog,game):

    found=None
    
    for  Id in catalog['category_data']['elements']:
        name=Id['Game_Id']
        if game['Name']== name:
            found=Id
    return found


def cmptime(time1,time2):
    if time1==time2:
        return 0
    elif time1 > time2:
        return 1
    else:
        return-1

def str_2_date(string): 
    if int(string[:2]) <= 22:
        año = "20" + string[:2]
        fecha = año + string[2:]
    elif int(string[:2]) > 22: 
        año = "19" + string[:2]
        fecha = año + string[2:]

    return dt.strptime(fecha, "%Y-%m-%d").date()

def cmpRevenue (revenue1,revenue2):
    if revenue1==revenue2:
        return 0
    elif revenue1 > revenue2:
        return 1
    else:
        return-1

def cmptime(time1,time2):
    if time1==time2:
        return 0
    elif time1 > time2:
        return 1
    else:
        return-1
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

