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
size = "small" 

#================[llamado del catalogo]=====================

def call_new_catalog():
    catalog = model.new_catalog()
    return catalog

# ===================================================
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ===================================================

def load_data(catalog):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    gamesfile = cf.data_dir + '/Speedruns/game_data_utf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(gamesfile, encoding='utf-8'), delimiter=",")
    for game in input_file:
        model.add_game(catalog, game)
        
    Recordsfile = cf.data_dir +  '/Speedruns/category_data_urf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(Recordsfile, encoding='utf-8'), delimiter=",")
    for record in input_file:
        model.add_record(catalog, record)
    
    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    return time, memory

#====================================================
#  Funciones de cada requerimiento
#====================================================

def callR1(catalog, platform, min_date, max_date):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, sizelista = model.R1_answer(catalog, platform, min_date, max_date)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (sorted_list, sizelista, time, memory)

def callR2(catalog, player):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    records_list, n_records = model.R2_answer(catalog, player)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (records_list, n_records, time, memory)

def callR3(catalog, min_runs, max_runs):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, sizelista = model.R3_answer(catalog, min_runs, max_runs)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (sorted_list, sizelista, time, memory)

def callR4(catalog, min_date, max_date):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, sizelista = model.R4_answer(catalog, min_date, max_date)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (sorted_list, sizelista, time, memory)

def callR5(catalog, min_time, max_time):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()


    sorted_list, sizelista = model.R5_answer(catalog, min_time, max_time)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (sorted_list, sizelista, time, memory)

#====================================================
#  Funciones para la toma de tiempos
#====================================================

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

#====================================================
#  Funciones para la toma de memoria utilizada
#====================================================

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