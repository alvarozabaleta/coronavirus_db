#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Usuario
"""

import json
import pandas as pd
from datetime import date

dateToday=str(date.today().strftime('%d%m%Y'))
with open('departamentos.geojson') as f:
    data = f.read()
raw_data=json.loads(data.decode("utf-8-sig"))

datos=pd.read_csv('resumen_casos_col_'+dateToday+'.csv', encoding='utf-8')
for i in range(len(raw_data['features'])):
    raw_data['features'][i]['properties']['confirmado']=0
    raw_data['features'][i]['properties']['recuperados']=0
    raw_data['features'][i]['properties']['defunciones']=0
    for j in range(len(datos)):
        if raw_data['features'][i]['properties']['departamento']==datos.loc[j,'Departamento']:
            raw_data['features'][i]['properties']['confirmado']=datos.loc[j,'confirmado'].astype(float)
            raw_data['features'][i]['properties']['recuperados']=datos.loc[j,'recuperados'].astype(float)
            raw_data['features'][i]['properties']['defunciones']=datos.loc[j,'defunciones'].astype(float)

geojson_file=json.dumps(raw_data, encoding='utf-8')
output_filename = 'covidgeojsoncol.js'
with open(output_filename, 'w') as output_file:
    output_file.write('departamentos = '+'{:}'.format(geojson_file))