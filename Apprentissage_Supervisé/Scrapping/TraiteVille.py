# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:32:54 2020

@author: gasto
"""

import pandas as pd
import numpy as np 
import os 
import ast
import re
os.chdir('D:\SORBONNE\M1\S2\ProjetPy\AirbnbPropre')

data = pd.read_csv('VillePropre.csv', sep=';')

#Supprimer les doublons pur
data.drop_duplicates(keep='last', inplace=True)
data.reset_index(drop=True, inplace=True)

"""
LES FONCTIONS DU TRAITEMENT

"""
#Transformer en dictionnaire    

def dico(obj):
    a = obj.replace('[','').replace(']','').replace('}','').replace('{','')
    b= '{'+a+'}'
    dic = ast.literal_eval(b)
    return dic


"""
TRAITEMENT DE LA VARIABLE PRIX

"""

#Traitement des prix        
for i in range(len(data['prix'])):
    if type(data['prix'][i]) is str :
        if '€' in data['prix'][i] :
            data['prix'][i] = data['prix'][i].replace('€','')
    
data['prix']=data['prix'].astype(float)


# Supprimer les logement sans prix
df=data[~data['prix'].isna()]
df.reset_index(drop=True, inplace=True)



"""
TRAITEMENT DE LA VARIABLE NOTE

"""
# La note de l'appartement
j=0
for i in df["note"]:
    i=str(i)
    i=i.replace(",",".")
    if "c" in i:
        df["note"][j]=np.nan
    else:  
        df["note"][j]=float(i[0:3])
    j+=1
        
"""
TRAITEMENT DE LA VARIABLE EQUIPMT ( les équipement de l'appartement)

"""    
 
#Suppression des caracteres genant et rendre le contenu en une liste 
for i in range(len(df['equipmt'])):
    df['equipmt'][i] = df['equipmt'][i].replace('[','').replace(']','')
    df['equipmt'][i] = df['equipmt'][i].replace('\n',' ').replace("'","")
    df['equipmt'][i] = (df['equipmt'][i].replace('"','')).split(',')

#Definit la liste des équipements
equipmt = ['Wi-Fi','Télévision','Climatisation','Sèche-cheveux','Cintres','Équipements de base Serviettes' , 'Chauffage Chauffage central ou radiateur électrique' , 'Détecteur de fumée' , 'Détecteur de monoxyde de carbone','Kit de premiers secours', 'Shampooing', 'Extincteur'] 

# Créer des dummi pour les verbatime défini dans equipement
for x in equipmt:
    for y in range (len(df['equipmt'].tolist())):
        if any(x in s for s in df['equipmt'][y]):
            df.at[y, x] = 1
        else:
            df.at[y, x] = 0

#predefinir des colonnes qui correspondes aux equipement    
varequp =['wifi','tv','clim','sèche_cheveux','cintres','equip_base','chauffage','detect_fumee','detect_mono','kit_secours','shampooing','exctincteur']
vardict = {}
for i in range(len(equipmt)):
    vardict[equipmt[i]] = varequp[i]
    
#appliquer le changement de colonne 
df.rename(columns=vardict,inplace=True)
df.columns


"""
TRAITEMENT DE LA VARIABLE DETAILS DES PRIS

""" 


# Recuperer l'index du detail des prix ou il y à un "nan"
nanpri=[]
for i in range(len(df['detailprix'])):
    if type(df['detailprix'][i]) is str and 'nan' in df['detailprix'][i]:
        nanpri.append(i)


#Supprimer les nan dans les details des prix    
for i in nanpri :
    df['detailprix'][i] = df['detailprix'][i].replace(', nan','').replace('nan','')




# un dico qui prend les colonne que l'on peut sortir des details prix
frais = {'Frais de service': np.nan, 'Frais de ménage' : np.nan , 'Taxes de séjour et frais': np.nan }

#Transformer chaque ligne du detail des prix en dico
for i in range(len(df['detailprix'])):
    if type(df['detailprix'][i]) is str and '{' in df['detailprix'][i]:
        df['detailprix'][i] = dico(df['detailprix'][i])
    else:
        df['detailprix'][i] = frais
 
       
varfrais =['Frais de service', 'Frais de ménage', 'Taxes de séjour et frais']
for l in range(len(df['detailprix'])):
    for v in varfrais:           
        if any(v in s for s in list(df['detailprix'][l].keys())):
            if type(df['detailprix'][l][v]) is str:
                df.at[l,v] = float(df['detailprix'][l][v].replace('€',''))
            else:
                df.at[l,v] = df['detailprix'][l][v]
        else:
            df.at[l,v] = np.nan




"""
TRAITEMENT DE LA VARIABLE CARACTERISTIQUES DE L'APPARATEMENT

""" 

#Suppression de valeur manque dans les caracteristiques des appartements
nanhost = df['caract'][0]
for i in range(len(df['caract'])):
    if df['caract'][i] == nanhost:
        df['caract'][i] = np.nan


saved = df['detailchambre']
"""
TRAITEMENT DE LA VARIABLE DETAILS DES APPARTEMENT 

""" 

#Suppression de valeur manque dans details des appart
nanch =df['detailchambre'][677]
for i in range(len(df['detailchambre'])):
    if df['detailchambre'][i]== nanch:
        df['detailchambre'][i] = np.nan

#Sprression des caracteres genantpour obtenir le nombre de voyageur 
for i in range(len(df['detailchambre'])):
    if type(df['detailchambre'][i]) is str:
        df['detailchambre'][i] = (df['detailchambre'][i].replace("'",'').replace('[','').replace(']','')).split(',')
    if type(df['detailchambre'][i]) is list:
        df['detailchambre'][i][0] = re.sub("[^0-9]", "", df['detailchambre'][i][0])
        if df['detailchambre'][i][0] != '':
            df['detailchambre'][i][0] = float(df['detailchambre'][i][0])
        else:
            df['detailchambre'][i][0] = np.nan
    else:
        df['detailchambre'][i] = [np.nan , np.nan , np.nan ,np.nan]
            
df.reset_index(drop=True, inplace=True)
df['detailchambre'][545]
# variable qui prend 1 sur c'est un studio , 0 sinon
for i in range(len(df['detailchambre'])):
    try:
        if df['detailchambre'][i][1] == 'Studio':
            df.at[i,'studio'] = 1
            df['detailchambre'][i][1] = float(1)
        else :
            df.at[i,'Studio'] = 0
        if df['detailchambre'][i][1] == '':
            df['detailchambre'][i][1] = np.nan
        else:
            df['detailchambre'][i][1] = re.sub("[^0-9]", "", df['detailchambre'][i][1])
            try:
                df['detailchambre'][i][1] = float(df['detailchambre'][i][1])
            except:
                df['detailchambre'][i][1] = np.nan
    except:
        df['detailchambre'][i][1] = np.nan
        
for i in range(len(df['detailchambre'])):
    try:
        if df['detailchambre'][i][2] == ' nan' or df['detailchambre'][i][2] == 'nan':
            df['detailchambre'][i][2] = np.nan
        else:
            df['detailchambre'][i][2] = re.sub("[^0-9]", "", df['detailchambre'][i][2])
            df['detailchambre'][i][2] = float(df['detailchambre'][i][2])
        if df['detailchambre'][i][2] is not str:
            try:
                df['detailchambre'][i][2] = float(df['detailchambre'][i][2])
            except:
                df['detailchambre'][i][2] = np.nan
    except:
        df['detailchambre'][i][2] = np.nan
            
  
   
for i in range(len(df['detailchambre'])):
    if type(df['detailchambre'][i][3]) is str : 
        df['detailchambre'][i][3] = re.sub("[^0-9]", "", df['detailchambre'][i][3])
    
    if df['detailchambre'][i][3] == '':
        df['detailchambre'][i][3] = np.nan
        
    if type(df['detailchambre'][i][3]) is str and 'partagée' in  df['detailchambre'][i][3] :
        df.at[i,'salbprivée'] = 0
    else:
        df.at[i,'salbprivée'] = 1
    

dtch = ['nbvoyageur','nbchambre','nblit','nbsalb']
for i in range(len(df['detailchambre'])):
    for j,e in enumerate(dtch):
        df.at[i,j] = float(df['detailchambre'][i][j])
        
vardict={}
for i in range(len(dtch)):
    vardict[i] = dtch[i]
df.rename(columns=vardict,inplace=True)

df.info()


"""
TRAITEMENT DE LA VARIABLE DETAILS DES APPARTEMENT 

""" 
for j in range(50):
    print(df['typelogmt'][j])


for i in range(len(df['typelogmt'])):
    if type(df['typelogmt'][i]) is str:
        df['typelogmt'][i] = (df['typelogmt'][i].replace("'","").replace('[','').replace(']','')).split(',')

for i in range(len(df['typelogmt'])):
    if type(df['typelogmt'][i]) is list:
        if 'Hôte' in df['typelogmt'][i][1] :
            df['typelogmt'][i][1] = df['typelogmt'][i][1].replace('Hôte','').replace(':','').rstrip().lstrip()
        else:
            df['typelogmt'][i][1] = df['typelogmt'][i][1].rstrip().lstrip()


"""
#Type de logement
for i in range(len(df['typelogmt'])):
    try:
        df['typelogmt'][i] = (df['typelogmt'][i].replace("'","").replace('[','').replace(']','').replace(':','')).split(',')
        df['typelogmt'][i]= df['typelogmt'][i][0]
    except:
        if type(df['typelogmt']) is list:
            df['typelogmt'][i]= df['typelogmt'][i][0]
        else:
            df['typelogmt'][i]=np.nan 
"""



zer = ['0' for x in range(len(df['typelogmt']))]
test = pd.DataFrame({'tl':zer})
for i in range(len(df['typelogmt'])):
    if type(df['typelogmt'][i]) is list:
        test.at[i,'tl'] = df['typelogmt'][i][0]
        
test['tl'].value_counts()

index_logement_hotel = ['Chambre dans boutique-hôtel',"Chambre dans apparthôtel","Chambre dans hôtel"]
index_logement_prive = ['Logement entier']
index_logement_chprive = ['Chambre privée dans : appartement']
"""
typlog=["partagée","privée","entier"]
z=0
for j in typlog:
    for i in df['typelogmt']:
        z+=1
        if j in str("privée" in df['typelogmt'][1]):
            z+=1
print(z)
"""   
    
for i in range(len(test['tl'])):
    if 'artag' in test['tl'][i]:
        print( test['tl'][i])

for y in range (len(test['tl'])):
    if test['tl'][y] in index_logement_hotel:
        df.at[y, 'log_hotel'] = 1
        df.at[y, 'log_ent'] = 0
        df.at[y, 'log_chpv'] = 0
        df.at[y,'log_partagé'] = 0
    elif test['tl'][y] in index_logement_prive:
        df.at[y, 'log_ent'] = 1
        df.at[y, 'log_chpv'] = 0
        df.at[y,'log_partagé'] = 0
        df.at[y, 'log_hotel'] = 0
    elif test['tl'][y] in index_logement_chprive:
        df.at[y, 'log_chpv'] = 1
        df.at[y, 'log_hotel'] = 0
        df.at[y, 'log_ent'] = 0
        df.at[y,'log_partagé'] = 0
    elif 'artag' in test['tl'][y]:
        df.at[y,'log_partagé'] = 1
        df.at[y, 'log_hotel'] = 0
        df.at[y, 'log_ent'] = 0
        df.at[y, 'log_chpv'] = 0
    else:
        df.at[y, 'log_hotel'] = 0
        df.at[y, 'log_ent'] = 0
        df.at[y, 'log_chpv'] = 0
        df.at[y,'log_partagé'] = 0
        

df.to_csv(r'VilleFinale1.csv',sep=';')

a= 5
b=a
a+=1
a
b

