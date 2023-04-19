import numpy as np
import re
import math 
import conexion.connect as cn

def convertData(df, column, regex, value):
    df.loc[df[column].str.contains(regex, flags=re.IGNORECASE, regex=True), 'group' ] = value
    return df
        
def asignacion (df,value,dfI):
    
    '''
        Operación asignación
    '''
    for grupo in value:
        print('estoy en el for y el grupo es: ',grupo)
        filter = df.loc[df['group'] == grupo]
        # if not filter.empty :
        dfTotal = filter.count()['group']

        dfIFilter = dfI.loc[dfI['Grupo'] == grupo]
        dfITotal = dfIFilter.count()['Grupo']
        
        operation = math.floor(dfTotal / dfITotal)
        
        extra = dfTotal % dfITotal
        array = ([operation+1] * extra) + ([operation] * (dfITotal - extra))
        start = 0
        
        users = dfIFilter['Usuario_Red'].values
        for idx, pos in enumerate(array):
            filter.loc[start:pos + start,['countGroup']] = [str(users[idx])]
            start = pos + start
            
        print('df es:', df)
    return df 
    


        
    
    

    

