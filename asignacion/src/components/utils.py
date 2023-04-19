import numpy as np
import pandas as pd
import re
import math
import conexion.connect as cn

ruta = r'C:\Users\daetobo\DAETOBO\Desarrollos\asignacion embargos py\asignacion\src'

def convertData(df, column, regex, value):
    df.loc[df[column].str.contains(
        regex, flags=re.IGNORECASE, regex=True), 'group'] = value
    return df


def asignacion(df, value, dfI):
    '''
        Operación asignación
    '''
    dfInicial = pd.DataFrame()
    for grupo in value:

        filter = df.loc[df['group'] == grupo]
        filter = filter.reset_index(drop=True)
        dfTotal = filter.count()['group']

        dfIFilter = dfI.loc[dfI['Grupo'] == grupo]
        dfITotal = dfIFilter.count()['Grupo']
        operation = math.floor(dfTotal / dfITotal)

        extra = dfTotal % dfITotal
        array = ([operation+1] * extra) + ([operation] * (dfITotal - extra))
        start = 0
        users = dfIFilter['Usuario_Red'].values

        for idx, pos in enumerate(array):
            filter.loc[start:pos + start, ['countGroup']] = [str(users[idx])]
            start = pos + start
        dfNuevo = pd.concat([filter, dfInicial], axis=0)
        dfInicial = dfNuevo

    return dfInicial
