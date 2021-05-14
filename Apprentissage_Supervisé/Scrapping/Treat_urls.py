import pandas as pd
import os 
from selenium import webdriver 
import time
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Mets le chemin où t'as exporté les urls ici :

os.chdir("D:\\SORBONNE\\M1\\S2\\ProjetPy")
months=['06','07','08'] #,'09','10','11','12'
urls=[]

# Seperate months
for month in months:
    df = pd.read_csv("urls_"+month+".csv")
    urls.append(df['urls'].tolist())




# assemble months 
urls_all=[]
for i in range(len(urls)):
    urls_all = urls_all + urls[i]    
    
ids=[]
for i in range(len(urls_all)):
    ids.append(urls_all[i][28:36])
    
test2 = pd.DataFrame({'ids':ids})
print(test2['ids'].nunique())

all_months = test2['ids'].unique().tolist()

to_export=[]
for id in all_months:
    for url in urls_all:
        if id in url:
            to_export.append(url)
            break

last_urls= pd.DataFrame({'urls':to_export})

# CHanges le chemin ici aussi :

last_urls.to_csv(r'D:\SORBONNE\M1\S2\ProjetPy\urls_all_months.csv',index = None, header=True,sep=";")







