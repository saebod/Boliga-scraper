import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import regex
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from Scraper import LastPage
from Scraper import GetBoligInfo
from Scraper import BoligRequirementsUrl

url = BoligRequirementsUrl(zipfrom=1000,zipto=1100,property=3,salestype=1)
Boliginfo=[]
LastPage=LastPage(url)
#Browser modul
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--start-maximized")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.get(url)
#Acceptere cookies
driver.find_element_by_css_selector('.coi-banner__accept').click()
for i in tqdm(range(int(LastPage)+1)):
	#Sleep timer da den ellers bare bliver ved med at skifte side før data er loaded
	time.sleep(3)
	page_source = driver.page_source
	soup = BeautifulSoup(page_source, 'html.parser')
	for i in soup.find_all('tr', class_='table-row'):
		Boliginfo.append(GetBoligInfo(i))
	driver.find_element_by_css_selector('.page-button.next').click()
driver.close()
driver.quit()
timestr = time.strftime("%Y%m%d")
final_db=pd.DataFrame(Boliginfo,columns=['adresse','Boligpris','Salgsdato','kvm','Rooms','kvmpris','byggeaar','boligtype'])
final_db.to_csv('Boliga'+str(timestr)+'.csv',encoding='utf-8-sig')

