    import pandas as pd
    import os 
    from selenium import webdriver 
    import time
    import numpy as np
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    
    os.chdir("D:\\SORBONNE\\M1\\S2\\ProjetPy")
    urls = pd.read_csv("urls_all_months.csv")
    urls = urls['urls'].tolist()
    
    chrome_path = r"C:/Users/gasto/Downloads/chromedriver.exe"
    def get_everything(url):
        url = url
        equips = []
        price_class=["_doc79r","_pgfqnw"] 
        rating_class=["_10za72m2","_192cr6q3"]
        equip_class = ["_czm8crp","_vzrbjl"]
    
    
        option = Options()
        #options.headless = True
        prefs = {'profile.default_content_setting_values': {'images':2}}
        option.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_path, options=option)
        driver.maximize_window()
        driver.get(url)
    
        time.sleep(3.5)
        #driver.find_element_by_css_selector(".optanon-allow-all.accept-cookies-button").click()
        #time.sleep(2)
        
        #Nom de l'appart:
        #_5gdh82 -> _5z4v7g -> _14i3z6h / _oc763uq -> _5twioja : no rating
        #                               / _13myk77s -> _5twioja : rating
        # weird : _1hpgssa1 -> _18hrqvin / _czm8crp
        try:
            c1 = driver.find_element_by_class_name("_5gdh82")
        
            c2 = c1.find_element_by_class_name("_5z4v7g")
            name = c2.find_element_by_class_name("_14i3z6h").text
            try:
                c2_bis=c1.find_element_by_class_name("_13myk77s")
                place = c2_bis.find_element_by_class_name("_5twioja").text
            except:
                c2_bis=c1.find_element_by_class_name("_oc763uq")
                place = c2_bis.find_element_by_class_name("_5twioja").text
        except:
            try:
                c1 = driver.find_element_by_class_name("_1hpgssa1")
                name = c1.find_element_by_class_name("_18hrqvin").text
                place = c1.find_element_by_class_name("_czm8crp").text
            except:
                name=np.nan
                place=np.nan
        
        # type_logement + nom de l'hôte
    
        try:    
            type_log_host_name_elm = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[1]')
            type_log_host_name = type_log_host_name_elm.text
            type_log_host_name = type_log_host_name.split('.')
        except:
            try:
                type_log_host_name=[]
                type_log_host_name.append(driver.find_element_by_xpath('//*[@id="room"]/div[2]/div/div[2]/div[1]/div/div[3]/div/div/div[3]/div/div/div[2]/div[1]/span').text)
                type_log_host_name.append(driver.find_element_by_xpath('//*[@id="summary"]/div/div/div[1]/div/div/div[2]/div/div/div[2]').text)
            except:
                try:
                    type_log_host_name=[]
                    type_log_host_name.append(driver.find_element_by_xpath('//*[@id="summary"]/div/div/div[1]/div/div/div[1]/div[1]/div/span/h1/span').text)
                    type_log_host_name.append(driver.find_element_by_xpath('//*[@id="summary"]/div/div/div[1]/div/div/div[2]/div/div/div[2]').text)
                except:
                    type_log_host_name=np.nan
        #Chambres /:
        chambres=[]
        j=[0,1,3,5,7]
        for i in range(1,5):    
                try:                  
                    chambres_elm=driver.find_element_by_xpath('//*[@id="site-content"]/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[2]/span['+str(j[i])+']').text
                    chambres.append(chambres_elm)
                except:
                    try:
                        chambres_elm= driver.find_element_by_xpath("//*[@id='room']/div[2]/div/div[2]/div[1]/div/div[3]/div/div/div[1]/div/div/div["+str(i)+"]/div").text
                        chambres.append(chambres_elm)
                    except:
                        chambres.append(np.nan)
        #host_carac:
        host_carac=[]           
        for x in range(1,4):
            try:
                host_=driver.find_element_by_xpath('//*[@id="site-content"]/div/div[7]/div/div/div/section/div/div[2]/div[2]/ul/li['+ str(x) +']').text
                host_carac.append(host_)
            except:
                try:
                    host_=driver.find_element_by_xpath('//*[@id="host-profile"]/div/div/section/div[5]/div/div['+str(x)+']/span/span').text
                    host_carac.append(host_)
                except:
                    try:
                        host_=driver.find_element_by_xpath('//*[@id="host-profile"]/div/div/section/div[4]/div/div['+str(x)+']/span/span').text
                        host_carac.append(host_)    
                    except:
                        host_carac.append(np.nan)
        
        #Details des notes :
        #  _en5l15m x->_iq8x9is  x ->_czm8crp / _1p3joamp
        #  _1s11ltsf x-> _y1ba89 / _4oybiu     
        time.sleep(0.7)
        # detailed prices: 
        #_1hvzytt -> _ryvszj x -> _bmsen5 -> _8zqgja / _ryvszj x -> _ra05uc  : clickable
        #_hgs47m x -> _10ejfg4u -> _1jlnvra2 // _ni9axhe -> _1jlnvra2 -> _j1kt73 : non-clickable
        # Taxes : _adhikmk -> _8zqgja / _ra05uc
        # Total : _j44qhm -> _adhikmk -> _plc5prx / _1d3ext9m
        details=[]
        # Clickable :
        try:
            s1=driver.find_element_by_class_name("_1hvzytt")
            
            tax_1=s1.find_element_by_class_name("_adhikmk")
            tax_type = tax_1.find_element_by_class_name("_8zqgja").text
            tax_value = tax_1.find_element_by_class_name("_ra05uc").text
            
            total_1=driver.find_element_by_class_name("_j44qhm")
            total_2=total_1.find_element_by_class_name("_adhikmk")
            total_type=total_2.find_element_by_class_name("_plc5prx").text
            total_value=total_2.find_element_by_class_name("_1d3ext9m").text
            
            s2=s1.find_elements_by_class_name("_ryvszj")
            for elm in s2:
                try:
                    details_below={}
            
                    price_value_elm=elm.find_element_by_class_name('_ra05uc')
            
                    s3=elm.find_element_by_class_name("_bmsen5")
                    price_type_elm=s3.find_element_by_class_name("_8zqgja")
            
                    price_type = price_type_elm.text
                    price_value=price_value_elm.text
            
                    details_below[price_type]=price_value
                    details.append(details_below)
                    time.sleep(4)
                except:
                    pass
            details.append({tax_type:tax_value})
            details.append({total_type:total_value})
        # Non-clickable :  
        except:
            try:
                for i in range(1,5):
                    details_below={}
                    type_try=driver.find_element_by_xpath('//*[@id="book_it_form"]/div[2]/div['+str(i)+']/div[1]/div[1]/span/span').text
                    value_try=driver.find_element_by_xpath('//*[@id="book_it_form"]/div[2]/div['+str(i)+']/div[1]/div[2]/span/span').text
                    details_below[type_try]=value_try
                    details.append(details_below)
                    time.sleep(4)
            except:
                try:        
                    s1=driver.find_elements_by_class_name("_hgs47m")
                    for elm in s1:
                
                        details_below={}
                
                        s2=elm.find_element_by_class_name("_10ejfg4u")
                        price_type_elm=s2.find_element_by_class_name("_1jlnvra2")
                
                        s2_bis=elm.find_element_by_class_name("_ni9axhe")
                        s3=s2_bis.find_element_by_class_name("_1jlnvra2")
                        price_value_elm=s3.find_element_by_class_name("_j1kt73")
                
                        price_value=price_value_elm.text
                        price_type = price_type_elm.text
                
                        details_below[price_type]=price_value
                        details.append(details_below)
                        time.sleep(4)
                except:
                    details.append(np.nan)
                               
        #Price  : 
        
        try:
            step_price = driver.find_element_by_class_name("_ryvszj")
            price_elm = step_price.find_element_by_class_name("_ra05uc")
            price = price_elm.text
            if '€' not in price:
                price_elm = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[4]/div/div/div[3]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/span/span[2]/span[1]')
                price = price_elm.text
        except:
            try:
                price_elm = driver.find_element_by_class_name(price_class[0])
                price = price_elm.text
                if '€' not in price:
                    price_elm = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[4]/div/div/div[3]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/span/span[2]/span[1]')
                    price = price_elm.text
            except:
                try:
                    price_elm = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[4]/div/div/div[3]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/span/span[2]/span[1]')
                    price = price_elm.text
                    if '€' not in price:
                        price=np.nan
                except:
                    price=np.nan
        # rating
        try:
            rating_elm = driver.find_element_by_class_name(rating_class[0])
            rating = rating_elm.text
        except:
            try:
                rating_elm = driver.find_element_by_class_name(rating_class[1])
                rating = rating_elm.text
            except:
                rating = np.nan
        
        #equipements 
                
        amenity_url = url.replace("?","/amenities?",1)
        driver.get(amenity_url)
        time.sleep(5)
         
        equip_elm=[]
        try:            
            try:
                equip_above = driver.find_elements_by_class_name("_1lhxpmp")
            except:
                try:
                    equip_above = driver.find_elements_by_class_name("_1dotkqq")
                except:
                    equip_above = driver.find_elements_by_class_name("_4xosax")    
            try:
                for elm in equip_above:
                    equip_elm.append(elm.find_element_by_class_name(equip_class[0]))
                for i in range(len(equip_elm)):
                    equips.append(equip_elm[i].text)
            except:
                for elm in equip_above:
                    equip_elm.append(elm.find_element_by_class_name(equip_class[1]))
                for i in range(len(equip_elm)):
                    equips.append(equip_elm[i].text)
                  
            if len(equips)==0:
                try:
                    equip_above = driver.find_elements_by_class_name("_1dotkqq")
                except:
                    equip_above = driver.find_elements_by_class_name("_4xosax")    
                try:
                    for elm in equip_above:
                        equip_elm.append(elm.find_element_by_class_name(equip_class[0]))
                    for i in range(len(equip_elm)):
                        equips.append(equip_elm[i].text)
                except:
                    for elm in equip_above:
                        equip_elm.append(elm.find_element_by_class_name(equip_class[1]))
                    for i in range(len(equip_elm)):
                        equips.append(equip_elm[i].text)
        except:
            equips=np.nan
    
        return name, place , price, rating, equips,host_carac,chambres, details ,url , type_log_host_name
    
    
    
    var = int((len(urls)/10)+1)
    counter = (np.arange(0,var)*10).tolist()
    
    for i in range(len(counter)-1):
        urls_test = urls[counter[i]:counter[i+1]]
        names,places,prices,ratings,equipss,host_caracs,chambress,detailss,liens,type_log_host_names = [],[],[],[],[],[],[],[],[],[]  
        for url in urls_test:
            name,place,price, rating, equips,host_carac,chambres,details,lien , type_log_host_name = get_everything(url)
    
            names.append(name)
            places.append(place)
            prices.append(price)
            ratings.append(rating)
            equipss.append(equips)
            host_caracs.append(host_carac)
            chambress.append(chambres)
            detailss.append(details)
            liens.append(lien)
            type_log_host_names.append(type_log_host_name)
    
    
        apparts=pd.DataFrame({'name':names,'place':places,'price':prices,'rating':ratings,'amenities':equipss,'host_caracs':host_caracs,'details_chambre':chambress,'details_prix':detailss,'url':liens,'type_log_host_name':type_log_host_names})
        apparts.to_csv(r'D:\SORBONNE\M1\S2\ProjetPy\donnee\lescsv\apparts1_'+str(i)+'.csv',index = None, header=True,sep=";", na_rep='NA')
    
    
    
    
    
a = "fdfbdf"
b=range(5)
for i, j in a, b:
    print(i)
    print(j)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
