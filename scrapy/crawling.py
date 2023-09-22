from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy.settings")
import django
django.setup()
from collector.models import Collector

# < -- global variable -- > # 
USER_ID = '####'
USER_PW = '####'
PlatformCode = '####'
url = '####'
shelfURL = '####'
datalst = []

def AutoLogin(driver, ID, Pw):
    driver.find_element(By.ID,'USER').click() 
    pyperclip.copy(ID)
    driver.find_element(By.ID,'USER').send_keys(Keys.CONTROL,'v')
    driver.find_element(By.ID,'LDAPPASSWORD').click()
    pyperclip.copy(Pw)
    driver.find_element(By.ID,'LDAPPASSWORD').send_keys(Keys.CONTROL,'v')
    driver.find_element(By.ID,'loginSsobtn').click()
    time.sleep(0.5)

def ProcessCrawling(url) :
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(3)
    driver.get(url)
    
    alert = Alert(driver)
    alert.accept()
    time.sleep(3)
    
    AutoLogin(driver, USER_ID, USER_PW)
    
    driver.get(shelfURL)
    
    driver.find_element(By.XPATH,'//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[1]/td[2]/div').click()

    pyperclip.copy(PlatformCode) # flexible
    
    driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[1]/td[2]/div/div/div/input').send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[1]/td[2]/div/div/div/input').send_keys(Keys.ENTER)

    time.sleep(0.5)
    
    driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/div/button').click()
    
    time.sleep(0.5)
    
    driver.find_element(By.XPATH, '//*[@id="sdpForm"]/div[2]/div[1]/select').click()
    driver.find_element(By.XPATH, '//*[@id="sdpForm"]/div[2]/div[1]/select/option[7]').click()
    
    # <! -- pagination-group -- !> #
    Pagnation = list(driver.find_element(By.XPATH, '//*[@id="sdpForm"]/nav/ul').text)
    PageList = ''.join(Pagnation).split('\n')
    
    if 'Next' in PageList :
        startpageidx = PageList.index('1')
        endpageidx = PageList.index('Next')-1

    else :
        startpageidx = int(PageList[PageList.index('1')])
        endpageidx = int(PageList[-1])

    print(f' > -- complete setting from {startpageidx} to {endpageidx} -- <')

    for page in range(startpageidx, endpageidx + 1) :
        pageSelector =  f'//*[@id="sdpForm"]/nav/ul/li[{page}]/a'
        driver.find_element(By.XPATH, pageSelector).click()
        time.sleep(0.2)
        
        # < -- check the row of count -- > #
        table = driver.find_element(By.XPATH, '//*[@id="sdpForm"]/div[3]/table/tbody')
        tr = len(table.find_elements(By.TAG_NAME, 'tr'))
        
        print(f' > -- start crawling {tr} of {page} data -- < ')
        
        # < -- click the shelf display ID -- > # 
        for num in range(1, tr+1) :
            time.sleep(0.5)
            shelfDispId = f'//*[@id="sdpForm"]/div[3]/table/tbody/tr[{num}]/td[2]/a'
            driver.find_element(By.XPATH, shelfDispId).send_keys(Keys.ENTER)
            time.sleep(0.5)
            
            ProdPlfCode = driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[2]/td[1]').text
            version = driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[3]/td[1]').text
            country = driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[3]/td[2]').text
            Status = driver.find_element(By.XPATH, '//*[@id="sdpForm"]/fieldset/div/table/tbody/tr[4]/td[1]/span').text
            
            # DF['PlatformCode'].append(ProdPlfCode)
            # DF['NPV'].append(version)
            # DF['Country'].append(country)
            # DF['Status'].append(Status)

            table = driver.find_element(By.XPATH, '//*[@id="shlefListTable"]/tbody')
            tr = len(table.find_elements(By.TAG_NAME, 'tr'))
            tmp = []
            
            for row in range(1, tr+1) :
                trpath = f'//*[@id="shlefListTable"]/tbody/tr[{row}]/td[2]'
                shelf = driver.find_element(By.XPATH, trpath).text
                tmp.append(shelf)
            
            # DF['Shelf'].append(', '.join(tmp))
            datalst.append([ProdPlfCode, version, country, Status, ', '.join(tmp)])
            driver.back()
            
        
    
    print('> -- crawling has been finsihed -- < ')
    print('> ------- show the result  -------- <')
    # print(datalst)
    
    return datalst
    
if __name__ == '__main__' :
    res = ProcessCrawling(url)
    for data in datalst :
        collector = Collector(
            platformcode = data[0],
            country = data[2],
            npv = data[1],
            status = data[3],
            shelf = data[4]
        )
        collector.save()
        
    print(' > -- complete data migrate -- <')
