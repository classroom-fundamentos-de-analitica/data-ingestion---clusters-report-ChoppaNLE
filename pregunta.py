"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------
Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.
"""

import pandas as pd
import re

def ingest_data():

    dataframe = open('clusters_report.txt', 'r')
    regex = re.sub("\s{3,}", "  ", dataframe.readline().strip()).split("  ")
    line = dataframe.readline().replace("\n", "").strip().split("  ")

    for i in range(len(regex)):
      regex[i] = (regex[i].strip().lower()).replace(" ", "_")
      if (i == 1 or i == 2):
        regex[i] = (regex[i] + ' ' + line[i-1].lower()).replace(" ", "_")

    dataframe.readline(), dataframe.readline()
    document = dataframe.readlines()
    content = []
    text = ''

    for line in document:
      line = re.sub(r"\s{2,}", " ", line.strip()).replace('\n', '')
      line += ' '
      if '%' in line:
        if (text != ''): 
          aux = content.pop()
          text = text.replace('.', '').strip()
          aux[3] = aux[3] + text
          content.append(aux)
          text = ''
        j = line.index('%')
        sublista = line[:j].strip().replace(',', '.').split(" ")
        content.append(sublista + [line[j + 2:]])
      else:
        text += line

    aux = content.pop()
    text = text.replace('.', '').strip()
    aux[3] = aux[3] + text
    content.append(aux)
    dataframe = pd.DataFrame(content, columns = regex)
    dataframe['cluster'] = dataframe['cluster'].astype('int64')
    dataframe['cantidad_de_palabras_clave'] = dataframe['cantidad_de_palabras_clave'].astype('int64')
    dataframe['porcentaje_de_palabras_clave'] = dataframe['porcentaje_de_palabras_clave'].astype('float64')
    
    return dataframe