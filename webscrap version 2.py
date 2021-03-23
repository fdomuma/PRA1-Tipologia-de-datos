import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

webBase = "https://www.museodelprado.es/coleccion/obras-de-arte"

def getPage(srcUrl):
    """
    Extrae la estructura HTML de una página web.

    :param srcUrl: Página web de la que extraer el contenido, debe ser un enlace web en formato string.
    :return: Estructura HTML de la web
    """

    pageStr = requests.get(srcUrl)
    pageCont = BeautifulSoup(pageStr.content, features="html.parser")

    return pageCont

def getLinks(pageCont):
    """
    Extrae los enlaces url dentro de la clase "presentacion-mosaico" de una web a partir de su estructura HTML.

    :param pageCont: Estructura HTML de una web.
    :return: lista con los enlaces url mencionados
    """

    mosaico = pageCont.find_all(class_="presentacion-mosaico")
    links = []

    for obra in mosaico:
        prueba = obra.find('a')
        links.append(prueba.get("href"))

    return links


def getDatos(pageCont):
    """
    Extrae los datos incluidos en la ficha técnica

    :param pageCont: Estructura HTML de una web
    :return: Lista con el contenido de la ficha técnica
    """
    #TODO Arreglar la estructura en la que extrae la información
    ficha =  pageCont.find(class_="ficha-tecnica")
    tags = ficha.find_all(['dt', 'dd'])
    elementos = []

    #en dd se encuentran los datos de cada pieza y en dt el nombre de la variable
    for elemento in tags:
        if elemento.name == "dd": # Contenido
            cadena = []
            for x in elemento.stripped_strings:
                cadena.append(x)
            elementos.append("".join(cadena))
        else:
            for z in elemento.stripped_strings: # Etiqueta
                elementos.append(z)
    return elementos


#función para descargar imagen
def load_requests(source_url):
    """
    #TODO
    :param source_url:
    :return:
    """

    r = requests.get(source_url, stream = True)
    if r.status_code == 200:
        aSplit = source_url.split('/')
        ruta = "./img/"+aSplit[len(aSplit)-1]
        print(ruta)
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()


def getImage(pageCont):
    """

    :param pageCont:
    :return:
    """
    images = []
    imagen = pageCont.find(class_="section-viewer")
    #obtenemos todos los img-src
    for img in imagen.findAll('img'):
        images.append(img.get('src'))

    #descargamos images[1] porque images[0] es None
    load_requests(images[1])



# Extraemos la estructura de la página base
pagBaseStr = getPage(webBase)

# Extraemos los links
enlacesObras = getLinks(pagBaseStr)

# Extraemos los datos
datos = []
for link in enlacesObras:
    tempPage = getPage(link)
    tempData = getDatos(tempPage)
    datos.append(tempData)

datosNP = np.array(datos)

for i, _array in enumerate(datosNP):
    if i == 0: # Sólo se va a ejecutar en la primera iteración luego iniciamos el df
        tempData = np.reshape(datosNP[i], (9, 2)) # Lista de listas
        fichaTec = tempData[:, 1] # Extrae la info
        datosDF = pd.DataFrame(data=[fichaTec], columns=tempData[:, 0])
    else:
        tempData = np.reshape(datosNP[i], (9, 2))
        fichaTec = []
        for element in tempData:
            fichaTec.append(element[1])
        datosDF.loc[len(datosDF.index)] = fichaTec
print(datosDF)
datosDF.to_csv('mydataframe.csv', index=False, encoding="iso-8859-1") #TODO al exportar el ; corta la línea


#TODO hacer una lista con todos los links de descarga e incluirlos en una nueva columna "url" en el df
"""
#obtenemos todos los links a buscar
linksBuscar = getLinks(webBase)


#obtenemos los datos de cada link
datos = []
for v in linksBuscar:
   datos.append(getDatos(v))

   #obtenemos la imagen
   getImage(v)

#imprimimos el codigo de cada pieza
for d in datos:
    print(d[1])
"""


