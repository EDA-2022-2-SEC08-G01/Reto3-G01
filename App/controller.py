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
 """


import config as cf
import model
import csv
import time
import tracemalloc
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
size = "10pct" 

# ___________________________________________________
# Inicialización del Catálogo de jugadores
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.new_analyzer()
    return analyzer


# ___________________________________________________
# Funciones carga de datos
# ___________________________________________________

def load_data(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    gamesfile = cf.data_dir + '/Speedruns/game_data_utf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(gamesfile, encoding='utf-8'), delimiter=",")

    for game in input_file:
        model.AddGameData(analyzer, game)
        
    Recordsfile = cf.data_dir +  '/Speedruns/category_data_urf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(Recordsfile, encoding='utf-8'), delimiter=",")
    
    for record in input_file:
        model.AddRecordData(analyzer, record)
    
    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    return time, memory

# ___________________________________________________
# Funciones de cada requerimiento
# ___________________________________________________

def Call_Req1(analyzer, platform, min_date, max_date):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, size = model.Req1_VideogamesByRangeDate(analyzer, platform, min_date, max_date)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return sorted_list, size, time, memory

def Call_Req2(analyzer, player):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    recordlist, Numrecords, size = model.R2_player_records(analyzer, player)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return recordlist, Numrecords, size, time, memory

def Call_Req3(analyzer, min_runs, max_runs):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    final_list, size = model.Req3_FastestRegistersByAttempts(analyzer, min_runs, max_runs)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (final_list, size, time, memory)

def Call_Req4(analyzer, min_date, max_date):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    final_list, size = model.Req4_SlowRegistersbyDates(analyzer, min_date, max_date)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (final_list, size, time, memory)

def Call_Req5(analyzer, min_time, max_time):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, size = model.Req5_RecentRegistersRecord(analyzer, min_time, max_time)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (sorted_list, size, time, memory)

def Call_req6(analyzer, min_date, max_date, propiedad, N, X):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    resultado = model.Req6_histograma_por_rango(analyzer, min_date, max_date, propiedad, N, X)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    return(resultado,time,memory)



# ___________________________________________________
# Funciones para la toma de tiempos
# ___________________________________________________

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# _____________________________________________
# Funciones para la toma de memoria
# ___________________________________________________

#Tomadas de HALLOFFRAME

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory