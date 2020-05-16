#!usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from datetime import date
import os

dateToday=str(date.today().strftime('%d%m%Y'))
dataUrl='http://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD'
savePath='D:/MTA/Project_Guadalajara/Mapa_col/'
urllib.urlretrieve(dataUrl, savePath + 'casos_col_'+dateToday+'.csv')

os.remove(savePath+'yesterdaycol.js')
os.rename(savePath+'todaycol.js',savePath+'yesterdaycol.js')
modifiedName='yesterdaycol.js'
pro=open('yesterdaycol.js')
prof=pro.read()
with open(modifiedName,'w') as arch:
    arc=prof[9:]
    arch.write('var yesterday'+'{:}'.format(arc))

casos=pd.read_csv(savePath + 'casos_col_'+dateToday+'.csv')
casos.rename(columns={'Departamento o Distrito ':'Departamento','atención':'Condicion'}, inplace=True)
casos=pd.DataFrame(casos,columns=['Departamento','Condicion'])

dpto=list(casos.Departamento.unique())
dpt_col=pd.read_csv(savePath+'dptos_geojso_col.csv')
summaryCases=pd.DataFrame()
for i in range(len(dpto)):
    summaryCases.loc[i,'Departamento']=dpto[i]
    r=casos[casos.loc[:,'Departamento']==dpto[i]]
    summaryCases.loc[i,'confirmado']=len(r)
    summaryCases.loc[i,'recuperados']=len(r[r.loc[:,'Condicion']=='Recuperado'])
    summaryCases.loc[i,'defunciones']=len(r[r.loc[:,'Condicion']=='Fallecido'])

for i in range(len(dpto)):
    for j in range(len(summaryCases)):
        if str(dpt_col.dpto[j]) in dpto[i] and dpto[i]!='Valle del Cauca':
            summaryCases.replace(dpto[i],dpt_col.NOMBRE_DPT[j],inplace=True)

summaryCases.to_csv('resumen_casos_col_'+dateToday+'.csv', index=False)
today=[float(sum(summaryCases.confirmado)),float(sum(summaryCases.recuperados)),float(sum(summaryCases.defunciones))]
fileName='todaycol.js'
with open(fileName, 'w') as todayFile:
    todayFile.write('var today = '+'{:}'.format(today))
#
#dptos=list(dpt_col.loc[:,'NOMBRE_DPT'].unique())
#for i in range(len(dptos)):
#    cumsum=casos.loc[:,'Departamento']==dptos[i]
#    cumsum=casos.loc[cumsum]
#    cumcases=len(cumsum)
#    for j in range(l):
#        if str(casos.loc[j,'Departamento'])==dptos[i]:
#            casos.loc[j,'confirmado']=cumcases
#            casos.loc[j,'latitud']=dpt_col.loc[i,'latitud']
#            casos.loc[j,'longitud']=dpt_col.loc[i,'longitud']
##casos.sort_values('fecha_diagnostico')
#casos=casos.drop_duplicates('Departamento', keep='last')
#casos.reset_index(drop=True, inplace=True)
#conf=sum(casos.confirmado)
#casos.reset_index(drop=True, inplace=True)
#casos.to_csv('resumen_casos_col_26042020.csv', index=False)

