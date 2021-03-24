import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
import time
from selenium.webdriver.common.keys import Keys


def insertNone(datos):
    """
    Función para tratar los datos nulos de cada obra

    :param datos: lista con los datos actuales de la obra
    :return: lista con todas las variables 
    """
    columnas = ["Número de catálogo","Autor","Título","Fecha",
    "Técnica","Soporte","Dimensión","Serie","Procedencia"]
    for col in columnas:
        if col not in datos:
            indice = columnas.index(col)*2
            datos.insert(indice,col)
            datos.insert(indice + 1,"None")
    return datos        

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

def getLinksMax(pageCont,max):
    """
    Extrae los enlaces url dentro de la clase "presentacion-mosaico" de una web a partir de su estructura HTML.
    Contiene un numero mázimo de links

    :param pageCont: Estructura HTML de una web.
    :param max: número maximo de links
    :return: lista con los enlaces url mencionados
    """

    mosaico = pageCont.find_all(class_="presentacion-mosaico")
    links = []
    len(mosaico)
    for i in range(max):
        prueba = mosaico[i].find('a')
        links.append(prueba.get("href"))

    return links


def getDatos(pageCont):
    """
    Extrae los datos incluidos en la ficha técnica

    :param pageCont: Estructura HTML de una web   14/15
    :return: Lista con el contenido de la ficha técnica
    """
    #TODO Arreglar la estructura en la que extrae la información
    ficha =  pageCont.find(class_="ficha-tecnica")
    if ficha is not None:
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
        #añadimos las columnas pendientes, columna de Url y obteemos el link
        if len(elementos) < 18:
            elementos = insertNone(elementos)
        elementos.append("UrlImagen")        
        elementos.append(getLinkImage(pageCont))
    else:
        elementos = ["Número de catálogo","","Autor","","Título","","Fecha","",
                    "Técnica","","Soporte","","Dimensión","","Serie","","Procedencia","","UrlImagen",""]       
    return elementos


#función para descargar imagen
def load_requests(source_url):
    """
    Descarga imagen contenida en source_url
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


def getLinkImage(pageCont):
    """
    Extrae el link de imagende la obra contenida en pageCont
    :param pageCont:
    :return: Link de la imagen de la obra
    """
    linksImagen = []
    imagenInfo = pageCont.find(class_="section-viewer")
    #obtenemos todos los img-src
    for img in imagenInfo.findAll('img'):
        linksImagen.append(img.get('src'))

    return  list(filter(None, linksImagen))[0]

#-------------------------------------------------------------------------------

#iniciamos conexion al webdriver de selenium 


option = webdriver.ChromeOptions()
option.add_argument("--headless") #opcion para que no aparezca el navegador

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install(), options = option)

webBase = "https://www.museodelprado.es/coleccion/obras-de-arte"
driver.get(webBase)
try:
    driver.find_element_by_tag_name('body').send_keys(Keys.END) # Función que permite llegar al final de la pagina web
    print("Fin pagina")
    time.sleep(120) #necesitamos 2000 segundos hasta que la pagina llega al final
    print("Fin time")
except:
    print("error") 

#obtenemos el archivo html para beautifulsoup
body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')

# Extraemos la estructura de la página base
pagBaseStr = BeautifulSoup(source, "html.parser")

# Extraemos los links

enlacesObras = getLinks(pagBaseStr)
numMax = len(enlacesObras)
#enlacesObras = getLinksMax(pagBaseStr,numMax)
driver.close()

# Extraemos los datos
datos = []
inicio = 1

for link in enlacesObras:
    print(inicio,"/",numMax)
    tempPage = getPage(link)    
    tempData = getDatos(tempPage)
    if len(tempData)!= 20:
        print(tempData)
    datos.append(tempData)
    inicio += 1
    time.sleep(0.5)


datosNP = np.array(datos)

for i, _array in enumerate(datosNP):
    if i == 0: # Sólo se va a ejecutar en la primera iteración luego iniciamos el df
        tempData = np.reshape(datosNP[i], (10, 2)) # Lista de listas
        fichaTec = tempData[:, 1] # Extrae la info
        datosDF = pd.DataFrame(data=[fichaTec], columns=tempData[:, 0])
    else:
        tempData = np.reshape(datosNP[i], (10, 2))
        fichaTec = []
        for element in tempData:
            fichaTec.append(element[1])
        datosDF.loc[len(datosDF.index)] = fichaTec
#print(datosDF)
datosDF.to_csv('mydataframe.csv', index=False, encoding="utf-8") #TODO al exportar el ; corta la línea


#TODO hacer una lista con todos los links de descarga e incluirlos en una nueva columna "url" en el df

