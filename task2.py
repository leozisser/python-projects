from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

'''THIS SCRIPT IS RELAUNCHABLE. THAT IS, IF YOU WERE BANNED, 
THE RESULTS ARE SAVED AND IF YOU AUNCH THE SCRIPT AGAIN YOUL PICK UP WHERE YOU FINISHED LAST TIME'''


url = 'https://elibrary.ru/titles.asp'
pub_url = 'https://elibrary.ru/title_profile.asp?id={}'
js = 'goto_page({})' #javascript we need to execute to go to next page of search results
pub_xpath = '/html/body/div[2]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[1]/table[3]/tbody/tr[4]' #xpath of publications

#next pages - we just set up our chrome prowser for selenium
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--disable-infobars')
driver = webdriver.Chrome('/Users/leo_z/Documents/GitHub/emboodo/chromedriver') #path for YOUR Chrome webdriver here


def get_id(elts): #cleaning up the elements list
    els = []
    for el in elts:
        id = el.get_attribute('id')[1:] #getting rid of 'a' in the beginning
        print('ID', id)
        if id:
            els.append(id)
    return els


def years(id, vals): #take list of values and assign them all the keys they need
    yrs = ['n_papers_risc_'+str(i) for i in range(2011,2021)]
    d = dict(zip(yrs,vals))
    d['name'] = str(id)
    return d


def get_list_of_ids():
    driver.get(url) #go to url
    driver.find_element_by_id('rubriccode').click() #find rubric code list
    driver.find_element_by_xpath("//option[@value='200000']").click() #select INFORMATIKA and click
    driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[2]/table[9]/tbody/tr[2]/td[6]/div").click() #click 'FIND' button
    i=1
    ids = []
    found = True
    while found == True: #if elements were found on the previous step, do:
        table = driver.find_element_by_xpath("//table[@id='restab']") #get the table from the page source
        elts = table.find_elements_by_tag_name("tr") #get the entries from the table
        els = get_id(elts)
        found = bool(els) #see if elements are found 
        ids.extend(els)
        i+=1
        driver.execute_script(js.format(str(i)))#go to next page

    ids = list(filter(None, ids))#filter out empty values  - the scraping is robust, so it grabs elements we do not need
    print(len(ids))
    with open('ids.txt','w')as idlist:
        idlist.write(','.join(ids))


def get_table(curnum:int):
    table = [] #list to which the columns will be added as dicts
    ids = open('ids.txt','r').read().split(',') #we open the id file and transform it into a list of values
    for nu, id in enumerate(ids[curnum:]): #we read every id 
        driver.get(pub_url.format(id)) #form a url and open it
        element_present = EC.presence_of_element_located((By.XPATH, pub_xpath)) #we need to be sure the element we re looking for can be found
        try:
            WebDriverWait(driver, 5).until(element_present) #we check for 5 seconds if the element is loaded
        except: #we write what we ve got to the resulting table
            dff = pd.DataFrame(table)
            dff.to_csv('out.csv',mode = 'a', header = (curnum==0),index = False)
            with open('current.txt','w') as out:
                out.write(str(curnum + nu)) #we update the last scraped number of id in the 'current' file
            print('BANNED, try again later')
            driver.exit()#exit the program
        row = driver.find_element(By.XPATH, pub_xpath) #find the desired element on the web page
        elts  = [i.text for i in row.find_elements_by_tag_name("td")[-10:]] #find table entries, grab the last 10 - thats how things work, they are the yearly publication figures
        row = years(id,elts) #create a dictionary with column names out of the figures
        print(row)
        table.append(row) #append them to the list of such rows
    dff = pd.DataFrame(table) #create a table from the list of dictionaries
    dff.to_csv('out.csv',mode = 'a', header = (curnum==0),index = False)#add the result to the file, headers only if the file was empty


#если файла со всеми id еще нет, запускается скрипт, который пролистывает страницы и берет оттуда все id
if not os.path.exists('ids.txt'):
    get_list_of_ids()

#в файле current сожержится порядковый номер id, на котором закончился скрейпингб если нас забанили за частые запросы
if os.path.exists('current.txt'):
    try:
        curnum = int(open('current.txt').read())
    except: #если файл пустой, начинаем с нуля - т е с первой пйдишки
        curnum = 0
else:#если файл не нацйден, начинаем с нуля тоже
    curnum = 0
get_table(curnum) #execute the table filling script. 
