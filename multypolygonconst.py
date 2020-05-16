#!usr/bin/env/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
from datetime import date

dateToday=str(date.today().strftime('%d%m%Y'))
saveNameSummary='resumen_covid_mex_'+dateToday+'.csv'

with open('mexican_states.geojson') as f:
    data = f.read()
raw_data=json.loads(data.decode("utf-8-sig"))

casos_con=pd.read_csv(saveNameSummary, encoding='utf-8')
for i in range(len(raw_data['features'])):
    if raw_data['features'][i]['properties']['admin_name']=='Distrito Federal':
        raw_data['features'][i]['properties']['admin_name']='Ciudad de Mexico'
    for index, item in casos_con.iterrows():
        if raw_data['features'][i]['properties']['admin_name']==item.estado:
            raw_data['features'][i]['properties']['confirmado']=item.confirmado
            raw_data['features'][i]['properties']['defunciones']=item.defunciones
geojson_file = json.dumps(raw_data, encoding='utf-8')
output_filename = 'covidgeojsonpolygon.js'

with open(output_filename, 'w') as output_file:
    output_file.write('var states = '+'{:}'.format(geojson_file))