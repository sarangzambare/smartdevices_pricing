import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# creating dataframe for the storage of all products
features = ['name','LTE','year','weight','display_type','screen_size','ppi','cpu_ghz','ram','internal','camera','front_cam','blth_v','battery','price']
products_df = pd.DataFrame(columns=features)
#test = [{'name':'blah'},{'LTE':'blah'},{'year':'blah'},{'weight':'blah'},{'display_type':'blah'},{'screen_size':'blah'},{'ppi':'blah'},{'cpu_ghz':'blah'},{'ram':'blah'},{'internal':'blah'},{'camera':'blah'},{'front_cam':'blah'},{'blth_v':'blah'},{'battery':'blah'}]


# scrapping gsmarena
base_url = 'https://www.gsmarena.com/'
# getting page
page = requests.get("https://www.gsmarena.com/makers.php3")




# making soup object
soup = BeautifulSoup(page.content, 'html.parser')

brands_container = soup.find("div",{'class':'st-text'})
# list of links of all mobile phone brands

brand_links = []
for a in brands_container.find_all("a"):
    brand_links.append(base_url+str(a.get('href')))


for brand_link in brand_links:
    product_links = []
    page = requests.get(brand_link)
    soup = BeautifulSoup(page.content,'html.parser')
    product_containers = soup.find("div",{"class":'makers'}).find_all('a')
        # creating list of all product links for a given brand
    for a in product_containers:
        product_links.append(base_url+str(a.get('href')))
        # scraping required features for each product_link for the given brand_link
    for product_link in product_links:
        page = requests.get(product_link)
        soup = BeautifulSoup(page.content,'html.parser')
        product_name = str(soup.find('h1',{'class':'specs-phone-name-title'}).text)

        # scraping all product specifications
        specs_list_container = soup.find('div',{'id':'specs-list'})
        product_lte = 1 if 'LTE' in str(specs_list_container.find('a',{'class':'link-network-detail collapse'}).text) else 0

        product_year = str(specs_list_container.find('td',{'data-spec':'year'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'year'}) else None

        product_weight = str(specs_list_container.find('td',{'data-spec':'weight'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'weight'}) else None

        product_disp_type = str(specs_list_container.find('td',{'data-spec':'displaytype'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'displaytype'}) else None

        product_disp_size = str(specs_list_container.find('td',{'data-spec':'displaysize'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'displaysize'}) else None

        product_ppi = str(specs_list_container.find('td',{'data-spec':'displayresolution'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'displayresolution'}) else None

        product_ghz = str(specs_list_container.find('td',{'data-spec':'cpu'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'cpu'}) else None

        product_ram = str(specs_list_container.find('td',{'data-spec':'internalmemory'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'internalmemory'}) else None

        product_internal = str(specs_list_container.find('td',{'data-spec':'internalmemory'}).text.encode('ascii','ignore')) if specs_list_container.find('td',{'data-spec':'internalmemory'}) else None

        product_cam = str(soup.find('td',{'data-spec':'cam1modules'}).text.encode('ascii','ignore')) if soup.find('td',{'data-spec':'cam1modules'}) else None

        product_frontcam = str(soup.find('td',{'data-spec':'cam2modules'}).text.encode('ascii','ignore')) if soup.find('td',{'data-spec':'cam2modules'}) else None

        product_bluetooth = str(soup.find('td',{'data-spec':'bluetooth'}).text.encode('ascii','ignore')) if soup.find('td',{'data-spec':'bluetooth'}) else None

        product_battery = str(soup.find('td',{'data-spec':'batdescription1'}).text.encode('ascii','ignore')) if soup.find('td',{'data-spec':'batdescription1'}) else None

        product_price = str(soup.find('td',{'data-spec':'price'}).text.encode('ascii','ignore')) if soup.find('td',{'data-spec':'price'}) else None

        # appending product to products_df dataframe
        products_df.loc[products_df.shape[0],:] = [product_name,product_lte,product_year,product_weight,product_disp_type,product_disp_size,product_ppi,product_ghz,product_ram,product_internal,product_cam,product_frontcam,product_bluetooth,product_battery,product_price]



products_df.to_csv('csv/smartdevices_data_full.csv')


# re for ppi = re.findall(r'\d{1,3} ppi',str(specs_list_container.find('td',{'data-spec':'displayresolution'}).text))[0][:4]
# re for ghz = re.findall(r'\d{1,2}\.\d{1,2} GHz',str(specs_list_container.find('td',{'data-spec':'cpu'}).text))[0][:3]
