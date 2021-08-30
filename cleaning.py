#######   LIMPIEZA Y ORGANIZACION DEL DATA SET Y LOS DATOS DE LA API ########

#Importamos las librerias que utilizaremos

import json
import numpy as np
import pandas as pd
import requests
import scr.functions as cf

#Importamos el data set de temperaturas y comenzaremos con el cleaning

te = pd.read_csv('/home/julian/Cursos/Ironhack/Proyectos/Proyecto2/temperature.csv')
h = pd.read_csv('/home/julian/Cursos/Ironhack/Proyectos/Proyecto2/humidity.csv')

tee = te.rename(columns={'datetime': 'fechas'}) 
he = h.rename(columns={'datetime': 'fechas'}) 

#TEMPERATURAS MEDIANAS MENSUALES EN CELSIUS
"""
Construimos un nuevo data frame con una columna de datos temporales, mostrando solo el año y el mes. Y agruparemos los
datos seleccionando la mediana del valor mensual. Primero, por cuestiones metodologicas, renombramos la columna
'datetime' por 'fechas'
"""

tem = cf.agrup_mensual(tee)

cf.keep_columns(['Vancouver', 'Los Angeles', 'Denver', 'Houston', 'Chicago', 'Atlanta', 'Miami',
              'Toronto', 'New York', 'Montreal'], tem)
"""
Convertimos los valores en grados kelvin a celsius y reposicionamos las fechas como una columna. Y los exportamos
a un csv
"""

temc = tem.apply(lambda row : cf.celsius_conv(row, tem))

temc = temc.reset_index()

temc.to_csv('temc',index=False)

#VARIABILIDAD MENSUAL DE TEMPERATURAS (EN K)
"""
Construimos un nuevo data frame con una columna de datos temporales, mostrando solo el año y el mes. Y agruparemos los
datos seleccionando el desvío estandar mensual.
"""

volat = cf.agrup_mensual_std(tee)

cf.keep_columns(['Vancouver', 'Los Angeles', 'Denver', 'Houston', 'Chicago', 'Atlanta', 'Miami',
              'Toronto', 'New York', 'Montreal'], volat)

volat = volat.reset_index()

volat.to_csv('volat',index=False)

#VALORES DE HUMEDAD MENSUAL 
"""
Repetimos proceso anterior con los datos de humedad
"""

hm = cf.agrup_mensual(he)

cf.keep_columns(['Vancouver', 'Los Angeles', 'Denver', 'Houston', 'Chicago', 'Atlanta', 'Miami',
              'Toronto', 'New York', 'Montreal'], h)

hm = hm.reset_index()

hm.to_csv('hm',index=False)

#VARIABILIDAD MENSUAL DE LA HUMEDAD


volath = cf.agrup_mensual_std(he)

cf.keep_columns(['Vancouver', 'Los Angeles', 'Denver', 'Houston', 'Chicago', 'Atlanta', 'Miami',
              'Toronto', 'New York', 'Montreal'], volath)

volath = volath.reset_index()

#DATOS DE LA API DE DIOXIDO DE CARBONO
"""
Obtenemos los datos de la API, y los volcamos a un data frame.
"""

c = cf.get_carbon_data('https://daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com/api/co2-api')

"""
Renombramos la columna cycle
"""
c = c.rename(columns={'cycle': 'Co2 Level'})

"""
Acoplamos las columnas de año, mes y dia en una sola, y agrupamos los valores por la mediana mensual
"""

dates = pd.period_range(start='2011-01-01', end='2021-08-28', freq='D')

c['fechas'] = [str(d) for d in dates]

cf.keep_columns(['fechas', 'Co2 Level'], c)

co2 = cf.agrup_mensual_co2(c)

co2 = co2.reset_index()

co2.to_csv('co2',index=False)

"""
Duplicamos el data frame de dioxido de carbono, pero escalado a las fechas del data set de 
temperaturas y humedad
"""
cco2 = cf.agrup_mensual_co2(c)

cco2 = cco2.reset_index()

cco2 = cf.chop_co2(cco2)

cco2.to_csv('cco2',index=False)

#TEMPERATURAS Y CARBONO
"""
Unimos los datos de temperatura y carbono en un solo data frame
"""

tyc = temc.set_index('Date').join(co2.set_index('Date'))

tyc = tyc.reset_index()

tyc.to_csv('tyc',index=False)

##HUMEDAD Y CARBONO

hyc = hm.set_index('Date').join(co2.set_index('Date'))

hyc = hyc.reset_index()

