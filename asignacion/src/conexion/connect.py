import pyodbc
import pandas as pd
import os

ruta = os.getcwd() #Obtiene el directorio actual
sep = os.sep #Obtiene el separador de directorios predefinido del sistema
filetype = '*.xlsx' #Tipo de archivo a buscar

# Nombre del controlador.
DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"
# Ruta completa del archivo.
# DB_PATH = r'C:\Users\daetobo\DAETOBO\Desarrollos\asignacion embargos py\asignacion\src\BD.accdb'
DB_PATH = r'\\10.8.45.166\DirServLogyAdmin\GciaReqLegales\Sección Embargos y Soluciones Legales\3.Inteligencia_Documental\1.Gestion_Informacion\1.Informacion_Central\BD.accdb'

def consulta(query):
    try:
        cnxn  = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
        if cnxn :
            cursor = cnxn.cursor()
            cursor.execute(query)
            rs = cursor.fetchall()
            datos = pd.read_sql(query,cnxn)
    except pyodbc.Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        cnxn.close()
        print("Conexión cerrada")
    return datos 

def insert(df):
    try:
        cnxn  = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
        if cnxn :
            cursor = cnxn.cursor()
            df1 = df[['# RUB','Identificacion del Demandado','Nombre Demandado','Fecha De emision del requerimiento','Valor De Embargo','Número De Oficio','Número De Radicado','Nombre Ente Legal','Nombre Funcionario','Identificacion del Demandante','Nombre Demandante','Nombre del Banco a Pagar','Número Cuenta Pago','Filial','Fecha y Hora de recepción al Banco (Sello o Correo electronico)','Tipo de Requerimiento','Ciudad del oficio','Departamento del Ente Legal','Dirección Ente Legal','Canal de Entrada','Fecha y Hora de Asignacion','Fecha y Hora de Aplicación','Tipo de Ley','Oficina Contable','Codigo de Banco a Pagar','Estado del Requerimiento','Dias de Solucion','Observacion y Gestion','Tipo de Carta','Porcentaje','Futuro','Abierto/Cerrado','Segmento del Cliente','Check Masivo','Anotacion Especial para la Aplicación','Ente Solicitante','Nombre del Demandado Sistema Banco','Generó devolución','¿Esperar Guia de Correspondencia?','countGroup']]
            
            df1 = df1.fillna('')
            df1 = df1.astype('str')
            
            df1.to_excel(ruta + sep + 'res' + sep + 'df1.xlsx',index=False)
            insert_sql = ("""INSERT INTO transmision_prueba (RUB,ID_Demandado,Nombre_Demandado,Fecha_Embargo,Valor_Embargo,Numero_Oficio,Num_Radicado,Nombre_Entidad,Nombre_Funcionario,Id_Dte,Nombre_Demandante,Nom_BancoAPagar,Num_Cuenta,Filial,Fecha_Hora_Recepcion,Tipo_Requerimiento,Ciudad,Departamento,Direccion,Canal_Entrada,Fecha_Asignacion,Fecha_Aplicacion,Tipo_Ley,Oficina_Pago,Codigo_BancoPagar,Estado_Requerimiento,Dias,Observacion,Tipo_Carta,Porcentaje,Futuro,Abierto_Cerrado,Segmento_Cliente,Check_Masivo,Anotacion_Especial,Ente_Solicitante,Nombre_ddo_Banco,Genero_Devolucion,Guia_Correspondencia,Usuario)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )""")
            
            values = [tuple(x) for x in df1.to_records(index=False)]

            cursor.executemany(insert_sql,values)
            cnxn.commit()
           
    except pyodbc.Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        cnxn.close()
        print("Conexión cerrada")
    return values