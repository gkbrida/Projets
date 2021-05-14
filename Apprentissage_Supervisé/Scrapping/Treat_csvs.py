
#merge apparts

import pandas as pd
import os 
from selenium import webdriver 
import time
import numpy as np


os.chdir(r'D:\SORBONNE\M1\S2\ProjetPy\AirbnbPropre')

apparts=[]

# Seperate months
for i in range(5):
    df = pd.read_csv("ville"+str(i)+".csv",sep=';')
    apparts.append(df)



nice = pd.concat(apparts)


nice.to_csv(r'D:\SORBONNE\M1\S2\ProjetPy\AirbnbPropre\VillePropre.',index = None, header=True,sep=";", na_rep='NA')







