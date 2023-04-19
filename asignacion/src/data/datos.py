import pandas as pd 
import os
import glob

def findFile():
    ruta = os.getcwd() #Obtiene el directorio actual
    sep = os.sep #Obtiene el separador de directorios predefinido del sistema
    filetype = '*.xlsx' #Tipo de archivo a buscar
    filename = glob.glob(ruta + sep + filetype)
    return filename