import requests
from bs4 import BeautifulSoup

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
            for x in elemento.stripped_strings:
                elementos.append(x)
        else:
            for z in elemento.stripped_strings: # Etiqueta
                if z == "Dimensión":
                    continue
                else:
                    elementos.append(z)
                print(z)
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
datos.append(getDatos(getPage(enlacesObras[0])))

print(datos)
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


