import pandas as pd
import random
from selenium import webdriver 
import time
import numpy as np
from selenium.webdriver.chrome.options import Options

# 1h et qlq :
chrome_path = r"C:/Users/gasto/Downloads/chromedriver.exe"

url_prime = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=search_query&query=Paris%2C%20France&checkin=2020-08-01&checkout=2020-08-15&adults=1"
next_page = '//*[@id="ExploreLayoutController"]/div[2]/div[2]/div/div/div[1]/nav/ul/li[6]/a/span/svg'

#page_ch = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=97bc65cd-f5ec-4f6e-9a9f-b7d375feef2a&query=Paris%2C%20France&checkin=2020-08-01&checkout=2020-08-15&adults=1&section_offset=4&items_offset="
nb_pages = 15
pages = (np.arange(nb_pages)*20).tolist()
def get_apparts_url(month):
    """
    Cette fonction permet d'extraire les liens de tous les appartements présent dans la page,
    elle permets aussi de parcourire plusieurs pages (le nombre est à définir dans la variable nb_pages) 
    """
    month=month
    zero = '0'
    day_in = 1
    day_out = 2
    apparts = []
    while day_in < 11 :
        if len(str(day_in)) ==1 and len(str(day_out)) ==1:
            page_ch = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=b7db1b2a-e291-440f-949b-f182ee6fdb8f&query=Paris%2C%20France&checkin=2020-"+month+"-"+zero+str(day_in)+"&checkout=2020-"+month+"-"+zero+str(day_out)+"&adults=1&section_offset=4&items_offset="
        elif len(str(day_in)) >1 and len(str(day_out)) ==1:
            page_ch = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=b7db1b2a-e291-440f-949b-f182ee6fdb8f&query=Paris%2C%20France&checkin=2020-"+month+"-"+str(day_in)+"&checkout=2020-"+month+"-"+zero+str(day_out)+"&adults=1&section_offset=4&items_offset="
        elif len(str(day_in)) ==1 and len(str(day_out)) >1:
            page_ch = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=b7db1b2a-e291-440f-949b-f182ee6fdb8f&query=Paris%2C%20France&checkin=2020-"+month+"-"+zero+str(day_in)+"&checkout=2020-"+month+"-"+str(day_out)+"&adults=1&section_offset=4&items_offset="            
        elif len(str(day_in)) >1 and len(str(day_out)) >1:
            page_ch = "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=b7db1b2a-e291-440f-949b-f182ee6fdb8f&query=Paris%2C%20France&checkin=2020-"+month+"-"+str(day_in)+"&checkout=2020-"+month+"-"+str(day_out)+"&adults=1&section_offset=4&items_offset="
        option = Options()
        #options.headless = True
        prefs = {'profile.default_content_setting_values': {'images':2}}
        option.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_path, options=option)
        for page in pages:
            driver.get(page_ch+str(page))
            try:
                apparts_elm = driver.find_elements_by_class_name("_i24ijs")
                for i in range(len(apparts_elm)):
                    apparts.append(apparts_elm[i].get_attribute('href'))
            except:
                pass
        driver.close()
        day_in +=1
        day_out +=1
    return apparts


ee=0
months=['06','07','08']  #,'09','10','11','12'
for month in months:
    apparts_urls = get_apparts_url(month)
    ids=[]
    for i in range(len(apparts_urls)):
        ids.append(apparts_urls[i][28:36])
    
    test2 = pd.DataFrame({'ids':ids})
    #print(test2['ids'].nunique())

    unique_urls = test2['ids'].unique().tolist()

    to_export =[]

    for id in unique_urls:
        for url in apparts_urls:
            if id in url:
                to_export.append(url)
                break

    last_urls= pd.DataFrame({'urls':to_export})

    last_urls.to_csv(r'D:\SORBONNE\M1\S2\ProjetPy\urls_'+month+'.csv',index = None, header=True,sep=";")
    ee=ee+1
    print(ee)






#https://www.airbnb.fr/s/Toulouse/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJ_1J17G-7rhIRMBBBL5z2BgQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=8ba02b09-b0ff-4e44-a4fc-70719b5512bc&query=Toulouse%2C%20France&checkin=2020-

#https://www.airbnb.fr/s/Lyon/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJl4foalHq9EcR8CG75CqrCAQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=63bd3e60-1fa7-4b16-a384-0afa847fe45a&query=Lyon%2C%20France&checkin=2020-


#https://www.airbnb.fr/s/Nice/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJMS2FahDQzRIRcJqX_aUZCAQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=1722ab6d-1693-4f7f-bf2d-fdb09136f0cc&query=Nice%2C%20France&checkin=2020-06-01&checkout=2020-08-31&section_offset=6&items_offset=20

#https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&source=structured_search_input_header&search_type=pagination&federated_search_session_id=b7db1b2a-e291-440f-949b-f182ee6fdb8f&query=Paris%2C%20France&checkin=2020-06-01&checkout=2020-




