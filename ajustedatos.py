#!usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import urllib
import zipfile
from datetime import date
import os

dateToday=str(date.today().strftime('%d%m%Y'))
dataUrl='http://187.191.75.115/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip'
savePath='D:/MTA/Project_Guadalajara/Mapas_Covid_CSL/Mapa_Covid_Polygon/'
saveNameZip='covid_mex_'+dateToday+'.zip'
saveNamecsv='covid_mex_'+dateToday+'.csv'
saveNameSummary='resumen_covid_mex_'+dateToday+'.csv'
urllib.urlretrieve(dataUrl, savePath+saveNameZip)

os.remove(savePath+'yesterdaymx.js')
os.rename(savePath+'todaymx.js',savePath+'yesterdaymx.js')
modifiedName='yesterdaymx.js'
pro=open('yesterdaymx.js')
prof=pro.read()
with open(modifiedName,'w') as arch:
    arc=prof[9:]
    arch.write('var yesterday'+'{:}'.format(arc))

with zipfile.ZipFile(savePath+saveNameZip, 'r') as zipData:
    rawData = zipData.namelist()
    zipData.extractall(savePath)
os.rename(savePath+rawData[0],savePath+saveNamecsv)

data = pd.read_csv(savePath+saveNamecsv, encoding = "ISO-8859-1")
data=data.drop(data[data.RESULTADO!=1].index)
data.ENTIDAD_RES=data.ENTIDAD_RES.astype(int)
data.reset_index(drop=True,inplace=True)
id_estado=data.ENTIDAD_RES.unique().tolist()
id_estado=[int(val) for val in id_estado]
casosconf=pd.DataFrame(id_estado,columns=['id_estado'])
estados=pd.read_csv('D:/MTA/Project_Guadalajara/Mapas_Covid_CSL/Mapa_Covid_Polygon/catalogo_estados.csv')
estados.CLAVE_ENTIDAD=estados.CLAVE_ENTIDAD.astype(int)
for i in range(len(casosconf)):
    var=data[data.loc[:,'ENTIDAD_RES']==casosconf.id_estado[i]]
    deftot=var[var.loc[:,'FECHA_DEF']!='9999-99-99']
    deftot=len(deftot)
    cum=len(var)
    casosconf.loc[i,'confirmado']=cum
    casosconf.loc[i,'defunciones']=deftot
    for j in range(len(estados)):
        if casosconf.id_estado[i]==estados.CLAVE_ENTIDAD[j]:
            casosconf.loc[i,'estado']=estados.ENTIDAD_FEDERATIVA[j]           

total_casos=sum(casosconf.confirmado)
casosconf.to_csv(saveNameSummary, index=False)

os.remove(savePath+saveNameZip)
today=[sum(casosconf.confirmado),sum(casosconf.defunciones)]
fileName='todaymx.js'
with open(fileName, 'w') as todayFile:
    todayFile.write('var today = '+'{:}'.format(today))
    
#casos_conf=[]
#for i in range(len(data)):
#    d=[val for val in data.iloc[i,4:]]
#    d=sum(d)
#    casos_conf.append(d)
#data['confirmado']=casos_conf
#data.rename(columns={'nombre':'estado'},inplace=True)
#data=data.drop(index=0,axis=0)
#data=pd.DataFrame(data,columns=['estado','confirmado','poblacion'])
#data.replace({'DISTRITO FEDERAL':'CIUDAD DE MEXICO'},inplace=True)
#data.reset_index(drop=True,inplace=True)
#
#for i in range(len(data)):
#    data.loc[i,'estado']=data.loc[i,'estado'].title()
#    if data.loc[i,'estado']=='Ciudad De Mexico':
#        data.loc[i,'estado']='Ciudad de Mexico'
#data=data.dropna()
#data.reset_index(drop=True, inplace=True)
#s=sum(data.confirmado)
#data.to_csv('resumen_covid_mex_20200424.csv', index=False)

#coor=pd.read_csv('covid_mx_23032020.csv')
#coor=coor.drop_duplicates('Estado')
#coor.reset_index(drop=True,inplace=True)
##origen=list(data.loc[:,'procedencia'].unique())
#n=len(data)
#
#estados=list(data.loc[:,'estado'].unique())
#for s in estados:
#    var=data.loc[:,'estado']==s
#    var=data.loc[var]
#    con=len(var)
#    for v in range(n):
#        if data.loc[v,'estado']==s:
#            data.loc[v,'confirmado']=con
#
#data['fecha_inicio']=pd.to_datetime(data['fecha_inicio'])
#data['fecha_inicio']=data['fecha_inicio'].dt.strftime('%Y%m%d').astype(int)
#data=data.sort_values('fecha_inicio')
#data=data.drop_duplicates('estado', keep='last')
#data.reset_index(drop=True,inplace=True)
#
#n=len(data)
#for i in range(n):
#    data.loc[i,'estado']=data.loc[i,'estado'].title()
#    if data.loc[i,'estado']=='Ciudad De Mexico':
#        data.loc[i,'estado']='Ciudad de Mexico'
#
#for j in range(len(data)):
#    for k in range(len(coor)):
#        if data.loc[j,'estado']==coor.loc[k,'Estado']:
#            data.loc[j,'latitud']=coor.loc[k,'latitud']
#            data.loc[j,'longitud']=coor.loc[k,'longitud']
#
#enc=list(data)
#ld=len(data)
#for i in enc:
#    for j in range(ld):
#        if str(data.loc[j,i])=='nan':
#            data.loc[j,i]='Undefined'
#cum=sum(data.confirmado)
#data=data.dropna()
#data.reset_index(drop=True, inplace=True)
#data.to_csv('resumen_covid_mex_20200418.csv', index=False)