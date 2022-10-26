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

# ___________________________________________________
# Inicialización del Catálogo de videojuegos
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def load_data(analyzer):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    gamesfile = cf.data_dir + '/Speedruns/game_data_utf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(gamesfile, encoding='utf-8'), delimiter=",")
    for game in input_file:
        model.add_game(analyzer, game)
        
    Recordsfile = cf.data_dir +  '/Speedruns/category_data_urf-8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(Recordsfile, encoding='utf-8'), delimiter=",")
    for record in input_file:
        model.add_record(analyzer, record)
    
    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    return time, memory

def loadGames(analyzer):

    gamesfile = cf.data_dir + 'game_data_utf8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(gamesfile, encoding='utf-8'))
    for game in input_file:
        model.add_game(analyzer, game)
    return lt.size(analyzer["games_data"])

def loadRecords(analyzer):
    
    Recordsfile = cf.data_dir + 'category_data_utf8-{0}.csv'.format(size)
    input_file = csv.DictReader(open(Recordsfile, encoding='utf-8'))
    for record in input_file:
        model.add_record(analyzer, record)
    return lt.size(analyzer["category_data"])


# ___________________________________________________
# Requerimientos
# ___________________________________________________


def CallReq1(analyzer, platform, min_date, max_date): 
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    list_games, num_games, height, n_elements= model.R1_FiveGamesbyPlatform(analyzer, platform, min_date, max_date)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if list_games == None:
        return None, None, None, None

    return time, memory, list_games, num_games, height, n_elements


# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

# ___________________________________________________
# Funciones para medir el tiempo utilizado
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



# ___________________________________________________
# Funciones para medir la memoria utilizada
# ___________________________________________________


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