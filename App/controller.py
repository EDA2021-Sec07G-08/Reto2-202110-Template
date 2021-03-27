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
from datetime import datetime as dt
import DISClib.ADT.list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():

    catalog = model.newCatalog()

    return catalog

def loadData(catalog, size):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadVideos(catalog, size)
    loadCategories(catalog)

def loadVideos(catalog, size):
    videosfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    cont = 0
    for video in input_file:
        new_video = {}
        info = ['title', 'video_id', 'category_id', 'channel_title', 'country', 'publish_time']
        info_2 = ['views', 'likes', 'dislikes']
        for i in info:
            new_video[i] = video[i]
        for j in info_2:
            new_video[j] = video[j]

        new_video['trending_date'] = dt.strptime(video['trending_date'], '%y.%d.%m').date()

        new_video['tags'] = lt.newList('ARRAY_LIST')

        for tag in video['tags'].split('"|"'):
            tag.replace('"', '')
            lt.addLast(new_video['tags'], tag)

        model.addVideo(catalog, new_video)
        cont += 1
        if cont >= size:
            break

def loadCategories(catalog):
    categoryfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'))
    for cat in input_file:
        new_cat = {}
        info = ['id', 'name']
        for i in info:
            new_cat[i] = (str(new_cat[i]).lower()).replace(' ', '')
            model.addCategory(catalog, new_cat)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def videosSize(catalog):
    return model.videosSize(catalog)

def categoriesSize(catalog):
    return model.categoriesSize(catalog)
