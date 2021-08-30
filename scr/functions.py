import requests
import json
import pandas as pd
import numpy as np

def keep_columns(x, y):
    """
    Toma como argumento la lista de las columnas que quiero conservar y el nombre del data frame.
    Recorre el indice de columnas del data frame correspondiente y elimina las
    columnas que no quiero conservar
    """
    relevant = x
    for i in y.columns:
        if i not in relevant:
            y.drop(columns=[i], inplace=True)

def celsius_conv(row, x):
    """
    Esta función toma como argumentos un data frame "x" y  la fila del data frame. Itera sobre los índices
    del data frame y convierte cada valor de la fila a grados celsius
    """

    for i in x.index:
           row[i] = row[i] - 273.15
    return row

def agrup_mensual_std(x):
    """
    Toma como argumento un data frame, le agrega la columna 'Date', itera sobre la columna 'fechas' seleccionando
    el año y el mes del dato, y agrupa los datos por mes utilizando el desvío estandar. El resultado son los
    desvíos estandar mensuales de las temperaturas para cada ciudad.
    """
    x['Date'] = x.fechas.apply(lambda y: y[:7])
    return x.groupby("Date").std()

def agrup_mensual(x):
    """
    Toma como argumento un data frame, le agrega la columna 'Date', itera sobre la columna 'fechas' seleccionando
    el año y el mes del dato, y agrupa los datos por mes utilizando la mediana. El resultado es la mediana
    mensual de las temperaturas para cada ciudad.
    """
    x['Date'] = x.fechas.apply(lambda y: y[:7])
    return x.groupby("Date").median()

def get_carbon_data(url):
    """
    Toma como argumento una url, agrega los headers específicos de la API en cuestión, genera una variable
    'response' haciendo un request a la url. Luego transforma la response en un json, para que esté en formato
    diccionario. Usando la response transformada, retorna un data frame.
    """
    url = f"{url}"
    headers = {
    'x-rapidapi-host': "daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com",
    'x-rapidapi-key': "6f91c81d8fmshc83b86b1b6c6c5cp108956jsnef221ca08c9a"
    }
    response = requests.request("GET", url, headers=headers)
    t = response.json()
    c = pd.DataFrame(t['co2'])
    return c

def agrup_mensual_co2(x):
    """
    Toma como argumento un data frame, le agrega la columna 'Date', itera sobre la columna 'fechas' seleccionando
    el año y el mes del dato, y agrupa los datos por mes utilizando la mediana. En este caso, el resultado es la mediana
    mensual de los valores de co2.
    """
    x['Date'] = x.fechas.apply(lambda y: y[:7])
    return x.groupby("Date").agg({"Co2 Level": "median"})

def chop_co2(x):
    """
    Toma como argumento un data frame, particularmente el de datos de Co2, y recorta las primeras 21 filas,
    y las últimas 45, de esta forma queda el data frame de la misma longitud que el de las temperaturas.
    """
    for i in range(83, 128):
        x.drop([i], axis=0, inplace=True)
    for i in range(21):
        x.drop([i], axis=0, inplace=True)
    return x
