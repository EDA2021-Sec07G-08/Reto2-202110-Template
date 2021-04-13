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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
                'videos_by_id': None,
                'videos_by_category_ids': None,
                'videos_by_country' : None}

    """
    Esta lista contiene todo los libros encontrados
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('ARRAY_LIST', compareVideosIds)

    catalog['videos_by_id'] = mp.newMap(375943, maptype='CHAINING', loadfactor=6.0, comparefunction=compareMapVideosIds)

    catalog['videos_by_category_ids'] = mp.newMap(numelements = 37, maptype='CHAINING', loadfactor = 6.0, comparefunction = compareVideosIds)

    catalog['videos_by_country'] = mp.newMap(numelements = 37, maptype = 'CHAINING', loadfactor = 2.0, comparefunction = compareMapVideosIds)

    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):

    lt.addLast(catalog['videos'], video)
    mp.put(catalog['videos_by_id'], video['video_id'], video)
    addCategoryVideo(catalog, video)
    addVideo_by_Country(catalog,video)

def addCategoryVideo(catalog, video):

    categories = catalog['videos_by_category_ids']
    category_id = video['category_id']
    entrada = mp.get(categories, category_id)
    videos_cat = me.getValue(entrada)
    lt.addLast(videos_cat['videos'], video)

def addCategory(catalog, category):

    categories = catalog['videos_by_category_ids']
    category_id = category['id']
    existCate = mp.contains(categories, category_id)
    if not existCate:
        videos_cat = newCategory(category)
        mp.put(categories, category_id, videos_cat)

def newCategory(category):
    entrada = {'category_id': '', 'category_name': '', 'videos': None}
    entrada['category_id'] = category['id']
    entrada['category_name'] = category['name']
    entrada['videos'] = lt.newList('LINKED_LIST', compareVideosByCategory)

    return entrada

def addVideo_by_Country(catalog,video):
    country = video['country']
    exists = mp.contains(catalog['videos_by_country'],country)
    if not exists:
        videos_country = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(videos_country,video)
        mp.put(catalog['videos_by_country'],country,videos_country)
    else:
        key_value= mp.get(catalog['videos_by_country'],country)
        value = me.getValue(key_value)
        lt.addLast(value, video)
# Funciones para creacion de datos

# Funciones de consulta

def videosSize(catalog):

    return lt.size(catalog['videos'])

def categoriesSize(catalog):

    return mp.size(catalog['videos_by_category_ids'])

# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideosIds(video1, video2):
    if video1 == video2['key']:
        return 0
    elif video1 > video2['key']:
        return 1
    else: 
        return -1

def compareMapVideosIds(id, entrada):
    identidad = me.getKey(entrada)
    if(id == identidad):
        return 0
    elif(id > identidad):
        return 1
    else:
        return -1

def compareVideosByCategory(keyname, entry):
    catentry = me.getKey(entry)
    if keyname == catentry:
        return 0
    elif keyname > catentry:
        return 1
    else:
        return -1

def compareVideosByCountry(keyname, country):
    countentry = me.getKey(country)
    if keyname == countentry:
        return 0
    elif keyname > countentry:
        return 1
    else:
        return -1


# Funciones de ordenamiento

def buscarCate(catalog, category_name):

    keys = mp.keySet(catalog['videos_by_category_ids'])

    for key in range(lt.size(keys)):

        pos = lt.getElement(keys, key)
        key_value = mp.get(catalog['videos_by_category_ids'], pos)
        value = me.getValue(key_value)
        cat_name = value['category_name']
        if cat_name == category_name:
            return value['category_id']

def Requerimiento2(catalog,country) :
    videos = mp.get(catalog['videos_by_country'],country)
    videos = me.getValue(videos)
    retorno = mp.newMap(comparefunction = compareMapVideosIds)
    print(lt.size(videos))
    for i in range(1,lt.size(videos)):
        video = lt.getElement(videos,i)
        exists = mp.contains(retorno,video['video_id'])
        if not exists:
            dic = {}
            dic['title'] = video['title']
            dic['channel_title'] = video['channel_title']
            dic['country'] = video['country'].lower()
            dic['trending_days'] = 1
            mp.put(retorno,video['video_id'],dic)
        else:
            key_value = mp.get(retorno,video['video_id'])
            value = me.getValue(key_value)
            value['trending_days'] += 1
    mayor = 0 
    mayor1 = {}
    result = mp.valueSet(retorno)
    for i in range(0,lt.size(result)):
        video=lt.getElement(result,i)
        if video['trending_days']  > mayor:
            mayor = video['trending_days']
            mayor1 = video 
    return mayor1 

def requerimiento3(catalog, category_name):

    category_id = buscarCate(catalog, category_name)

    key_value = mp.get(catalog['videos_by_category_ids'], category_id)
    videos = me.getValue(key_value)['videos']

    retorno = mp.newMap()

    for i in range(lt.size(videos)):

        video = lt.getElement(videos, i)
        exists = mp.contains(retorno, video['title'])
        if exists:
            valores = mp.get(retorno, video['title'])
            valor = me.getValue(valores)
            valor['trending_dates'] += 1
        else:
            dicc = {}
            dicc['channel_title'] = video['channel_title']
            dicc['category_id'] = category_id
            dicc['trending_dates'] = 1
            mp.put(retorno, video['title'], dicc)

    temp = mp.keySet(retorno)

    mayor_num = 0
    mayor_dict = 0

    for i in range(lt.size(temp)):

        key = lt.getElement(temp, i)
        trendings = mp.get(retorno, key)
        values = me.getValue(trendings)
        num = values['trending_dates']
        if mayor_num < num:
            mayor_dict = values

    return values
        

