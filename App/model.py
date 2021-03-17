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

# Funciones para agregar informacion al catalogo

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
                'videos_id': None,
                'categoryIds': None,
                'tags': None,
                'tagIds' : None}

    """
    Esta lista contiene todo los libros encontrados
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideosIds)

    catalog['videos_id'] = mp.newMap(10000,
                                    maptype = 'CHAINING',
                                    loadfactor=4.0,
                                    comparefunction=compareMapVideosIds)

    catalog['categoryIds'] = mp.newMap(49,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareVideosByCategory)

    return catalog

# Funciones para creacion de datos

def newCategory(name):
    category = {'name' : "",
                'videos' : None}
    category['name'] = name
    category['videos'] = lt.newList('SINGLE_LINKED', compareVideosByCategory)

def addVideo(catalog, video):

    lt.addLast(catalog['videos'], video)
    mp.put(catalog['categoryIds'], video['title'], video)
    categories = video['category_id']
    for category in categories:
        addCategoryVideo(catalog, category, video)

def addCategoryVideo(catalog, category_name, video):
    categories = catalog['category_id']
    existcategory = mp.contains(categories, category_name)
    if existcategory:
        entry = mp.get(categories, category_name)
        category = me.getValue(entry)
    else:
        category = newCategory(category_name)
        mp.put(categories, category_name, category)

    lt.addLast(category['video'], video)


# Funciones de consulta

def videosSize(catalog):

    return lt.size(catalog['videos'])

def categoriesSize(catalog):

    return lt.size(catalog['categoryIds'])

# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideosIds(id1, id2):
    if(id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else: 
        return -1

def compareMapVideosIds(id, entrada):
    identidad = me.getKey(entrada)
    if(id1 == entrada):
        return 0
    elif(id1 > entrada):
        return 1
    else:
        return -1

def compareVideosByCategory(keyname, category):
    catentry = me.getKey(category)
    if (keyname == catentry):
        return 0
    elif (keyname > catentry):
        return 1
    else:
        return -1


# Funciones de ordenamiento
