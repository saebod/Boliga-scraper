import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import regex
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def BoligRequirementsUrl(zipfrom,zipto='',property='',salestype='',yearfrom='',yearto=''):
	'''Bygger en URL udfra args som senere bruges til at scrape 
	
	Args:
	zipfrom (int): Postnummer den skal starte med at scrape fra
	zipto (int): slut interval for postnumeret den skal scrape, 
		hvis zipto er tom scraper den kun postnummeret der er angiver i zipfrom
	property (int): Angiver boligtype som kan være følgende:
		1: Villa
		2: Rækkehus
		3: Ejerlejlighed
		4: Fritidshus
		5: Landejendom
	salestype (int): Angiver handelstype som kan være følgende:
		1: Almindelig frihandel
		2: Familieoverdragvelse
		3: Auktion
		4: Øvrigt
	yearfrom (int): Angiver start intervallet for salgsåret
	yearto (int): Angiver slut intervallet for salgsåret, hvis dette felt er tomt vil salgsåret kun være yearfrom'''
	def Emptyinput(input,html):
		'''Empty input bruges til hvis input er tom skal den ikke tilføje noget input ellers skal den'''
		if input=='':
			linkpart=''
		else:
			linkpart=html+str(input)
		return linkpart
	if zipto=='':
		_zip='&zipcodeFrom='+zipfrom+'&zipcodeTo='+str(zipfrom)
	else:
		_zip='&zipcodeFrom='+str(zipfrom)+'&zipcodeTo='+str(zipto)
	_property=Emptyinput(property,'&propertyType=')
	_salestype=Emptyinput(salestype,'&saleType=')
	_yearfrom=Emptyinput(yearfrom,'&salesDateMin=')
	_yearto=Emptyinput(yearto,'&salesDateMax=')
	_end ='&sort=date-d&page=1'
	url='https://www.boliga.dk/salg/resultater?searchTab=1'+_zip+_property+_salestype+_yearfrom+_yearto+_end
	return str(url)

def LastPage(url):
	''' Henter den sidste side fra søgeresultaterne '''
	html = requests.get(str(url)).content
	soup = BeautifulSoup(html, 'html.parser')
	LastPage=soup.find_all('a',class_='page-button')[6].text
	return LastPage

def GetBoligInfo(i):
	'''Indsamler informationer fra hver bolig
	Args
	i angiver hver række i tabellen som kan findes ved soup.find_all('tr', class_='table-row')'''
	adresse=i.find('a',class_='text-primary font-weight-bolder text-left').text
	Boligpris = i.find_all('span',class_='text-nowrap')[0].text
	Salgsdato=i.find_all('span',class_='text-nowrap')[1].text
	kvm=(i.find_all('span',class_='text-nowrap')[3].text).split()[0]
	Rooms=(i.find_all('td',class_='table-col text-right')[4].text).replace('Værelser  ','')
	kvmpris=i.find_all('span',class_='text-nowrap')[2].text
	byggeaar=(i.find_all('td',class_='table-col text-right')[6].text).replace('Byggeår  ','')
	boligtype=(i.find('app-tooltip',class_='md-right flex-shrink-0').text).split()[0]
	bolig=[adresse,Boligpris,Salgsdato,kvm,Rooms,kvmpris,byggeaar,boligtype]
	return bolig

def Bolig_df(zipfrom,zipto='',property='',salestype='',yearfrom='',yearto=''):
	url=BoligRequirementsUrl(zipfrom=zipfrom,zipto=zipto,property=property,salestype=salestype,yearfrom=yearfrom,yearto=yearto)
	Boliginfo=[]
	_LastPage=LastPage(url)
	#Browser modul
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
	driver.get(url)
	#Acceptere cookies
	driver.find_element_by_css_selector('.coi-banner__accept').click()
	for i in tqdm(range(int(_LastPage)+1)):
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
	return final_db

