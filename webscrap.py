import requests
from bs4 import BeautifulSoup

princ = "https://www.museodelprado.es/coleccion/obras-de-arte"

def getLinks(srcUrl):
    page = requests.get(srcUrl)
    soup = BeautifulSoup(page.content)

    mosaico =  soup.find_all(class_="presentacion-mosaico")
    links = []

    for l in mosaico:
        prueba = l.find('a')
        links.append(prueba.get("href"))

    return links

def getDatos(srcUrl):
    #descargamos el html y lo parseamos con BS
    page = requests.get(srcUrl)
    soup = BeautifulSoup(page.content)

    #buscamos la clase ficha-tecnica que contiene todos los datos
    ficha =  soup.find(class_="ficha-tecnica")
    tags = ficha.find_all(['dt', 'dd'])
    elementos = []

    #en dd se encuentran los datos de cada pieza y en dt el nombre de la variable
    for i in tags:
        if i.name == "dd":
            cadena = []
            for x in i.stripped_strings:
                cadena.append(x)
            elementos.append(cadena)
        else:
            for z in i.stripped_strings:       
                elementos.append(z)

    return elementos


#función para descargar imagen
def load_requests(source_url):
    r = requests.get(source_url, stream = True)
    if r.status_code == 200:
        aSplit = source_url.split('/')
        ruta = "./img/"+aSplit[len(aSplit)-1]
        print(ruta)
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()


def getImage(srcUrl):
    page = requests.get(srcUrl)
    soup = BeautifulSoup(page.content)
    #buscamos la clase section-viewer que contiene el src de la imagen
    images = []
    imagen =  soup.find(class_="section-viewer")
    #obtenemos todos los img-src
    for img in imagen.findAll('img'):
        images.append(img.get('src'))

    #descargamos images[1] porque images[0] es None
    load_requests(images[1])


#obtenemos todos los links a buscar
linksBuscar = getLinks(princ)

#obtenemos los datos de cada link
datos = []
for v in linksBuscar:
   datos.append(getDatos(v))
   #obtenemos la imagen
   getImage(v)

#imprimimos el codigo de cada pieza
for d in datos:
    print(d[1])   



