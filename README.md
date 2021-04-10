# PRA1-Tipologia-de-datos

## Miembros del equipo

Este trabajo ha sido realizado por **Fernando Muñoz Martín** y **Ricardo Santos Patrício**, alumnos de la asignatura **Tipología y ciclo de vida de los datos** del **Máster en Ciencia de Datos**.

## Descripción Archivos

En este repositorio podemos encontrar las siguientes carpetas y archivos:

- **nombrePDF.pdf**: pdf en el que encontramos las respuestas a las preguntas propuestas en el enunciado de la práctica;
- **src**: en esta carpeta encontraremos todo el código desarrollado para realizar el scraping a la web del Museo del Prado
  - **Webscrapper Museo del Prado.py**: este archivo Python consiste en el archivo que realiza todo el web scraping de esta práctica
  - **versiones Anteriores**: en esta carpeta podemos encontrar versiones alternativas desarrolladas, entre las cuales tenemos una versión desarrollada con hilos que permite una ejecución concurrente del web scraping y una versión desarrollada para hacer web scrpaing con el navegador Chrome. La versión que implementa Hilos ha sido finalmente descartada debido a la gran carga que supone al servidor.
- **DOI**: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4678339.svg)](https://doi.org/10.5281/zenodo.4678339)
- **Datos**: en esta carpeta encontramos todos los datos obtenidos
  - **fichasTecnicas_MuseoPrado.csv**: CSV que contiene datos obtenidos de las obras con el desarrollo de esta práctica
  - **imgs**: carpeta que contiene las primeras 15 imagenes descargados de la página web del Museo del Prado
