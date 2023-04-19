import pandas as pd 
import numpy as np
import components.utils as utils
import conexion.connect as cn
import data.datos as dt
import re
import json
import os
import datetime

ruta = os.getcwd() #Obtiene el directorio actual
sep = os.sep #Obtiene el separador de directorios predefinido del sistema
filetype = '*.xlsx' #Tipo de archivo a buscar
fileName = dt.findFile()

def asignarGrupo(columns,grupos):

    for file in fileName:
        df = pd.read_excel(file,index_col=False)
        # se agrupa por RUB con transform aplica count a todas las filas
        df['count'] = df.groupby('# RUB')['# RUB'].transform('count')
                
        map_salida = json.load(open('map' + '.json'))
        
        '''
            Ciclo que valida los parametros de columna, filtra el archivo para
            asignar el grupo al que pertenece cada caso según las reglas de negocio.
        '''
        for i in columns:
            for k, v in map_salida[i].items():
                df = utils.convertData(
                    df=df,
                    column=i,
                    regex=k,
                    value=v
                )
        
        df.loc[( df['group'].isnull() == True ) & ( df['count'] > 5 ),'group'] = 'Masivo'
        df.loc[( df['group'].isnull() == True ),'group'] = 'Genérico'

        '''
            Asignación de Grupos
        '''
        df['countGroup'] = df.groupby('group')['group'].transform('count')
        query = """SELECT Usuario_Red, Grupo
                    FROM Investigadores"""
        datos = cn.consulta(query)

        df = utils.asignacion(df= df,value= grupos,dfI= datos)
        
        insert = cn.insert(df)
        
        df.to_excel(ruta + sep + 'res' + sep + 'resultado.xlsx',index=False)
         
asignarGrupo(columns=['Nombre Ente Legal','Nombre Demandado','Filial'], grupos=['Genérico','Especiales','Mixtos','Colpensiones','Filiales'])