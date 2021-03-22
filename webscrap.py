import requests
from bs4 import BeautifulSoup

link2 = "https://www.museodelprado.es/coleccion/obra-de-arte/parte-superior-del-pantocrator-sostenido-por/a331fb54-a6d4-4732-8509-daf462aa92bb?searchid=96eed19b-48f4-a288-f0b2-93f7f63d8f62" 
link = "https://www.museodelprado.es/coleccion/obra-de-arte/la-magdalena-pintura-mural-de-la-ermita-de-la/0ad8f53d-8249-40b0-9e75-73d59f0ec014?searchid=5b508f8f-b63a-cb19-3117-59130a5ee823"

#descargamos el html y lo parseamos con BS
page = requests.get(link)
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
print(elementos)

#función para descargar imagen
def load_requests(source_url):
    r = requests.get(source_url, stream = True)
    if r.status_code == 200:
        aSplit = source_url.split('/')
        ruta = "./"+aSplit[len(aSplit)-1]
        print(ruta)
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()

#buscamos la clase section-viewer que contiene el src de la imagen
images = []
imagen =  soup.find(class_="section-viewer")
#obtenemos todos los img-src
for img in imagen.findAll('img'):
    images.append(img.get('src'))

#descargamos images[1] porque images[0] es None
load_requests(images[1])

print(images)

