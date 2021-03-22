import requests
from bs4 import BeautifulSoup

link = "https://www.museodelprado.es/coleccion/obra-de-arte/parte-superior-del-pantocrator-sostenido-por/a331fb54-a6d4-4732-8509-daf462aa92bb?searchid=96eed19b-48f4-a288-f0b2-93f7f63d8f62" 
page = requests.get(link)

soup = BeautifulSoup(page.content)

ficha =  soup.find(class_="ficha-tecnica")
tags = ficha.find_all(['dt', 'dd'])
elementos = []

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


