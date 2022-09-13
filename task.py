import requests
from bs4 import BeautifulSoup as BS
import psycopg2
import pandas as pd
from config import host, user, password, db_name
class BD:

    def __init__(self):
        pass
        

    
    
    def create_staging_table(self) -> None:
        connect = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name

            )
        connect.autocommit = True
        with connect.cursor() as cursor:
            cursor.execute(
            """CREATE TABLE list_of_flat(
                id serial PRIMARY KEY,
                price varchar(50) NOT NULL,
                date varchar(50) NOT NULL,
                town varchar(50) NOT NULL,
                name varchar(50) NOT NULL)"""
                rint("success table")            
        



   
        
    def close_db(self):
        pass

#######################
class Flat:
   
    
    def parse(self) -> dict:
        website = ("https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273")
        r = requests.get(website)
        soup = BS(r.text, 'lxml')
        #1
        url_of_image__advertisement = soup.find('div', class_='image').find('picture', class_='').find('source', class_='').get('data-srcset').strip()
        #2
        name_of_advertisement = soup.find('div', class_='title').find('a', class_='title').text.strip()
        #3
        data_of_advertisement  = soup.find('span', class_='date-posted').text
        #4
        city_of_advertisement  = soup.find('div', class_='location').find('span', class_='').text.strip()
        #5
        place_of_advertisement =  soup.find('span', class_ = 'bedrooms').text.replace(" ","").replace('\n','')
        #6
        discribe_of_advertisement =  soup.find('div', class_ = 'description').text.strip()
        #7
        price_of_advertisement =  soup.find('div', class_ = 'price').text.strip()
        
        info_about_flat = {'url image':url_of_image__advertisement,
                            'name':name_of_advertisement,
                            'data':data_of_advertisement,
                            'city':city_of_advertisement,
                            'place':place_of_advertisement,
                            'discribe':discribe_of_advertisement,
                            'price':price_of_advertisement}

        
        data_1 = []
        for p in range(2,5):
            url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{p}/c37l1700273'
            r = requests.get(url)
            soup = BS(r.text, 'lxml')
            all_info = soup.findAll('div',class_='info' )
            for ads in all_info:
                 #url_of_image__advertisement = ads.find('div', class_='image').find('picture', class_='').find('source', class_='').get('data-srcset').strip()
                 name_of_advertisement = ads.find('div', class_='title').find('a', class_='title').text.strip()
                 #data_of_advertisement = ads.find('div', class_='date-posted').text
                 city_of_advertisement = ads.find('div', class_='location').find('span').text.strip()
                 #place_of_advertisement = ads.find('div', class_ = 'rental-info').find('span', class_ = 'bedrooms').text.replace(" ","").replace('\n','')
                 discribe_of_advertisement = ads.find('div', class_ = 'description').text.strip()
                 price_of_advertisement = ads.find('div', class_ = 'price').text.strip()
                 data_1.append([name_of_advertisement, city_of_advertisement, discribe_of_advertisement, price_of_advertisement, ])
            

            
            
        header = ['name_of_advertisement', 'city_of_advertisement', 'discribe_of_advertisement', 'price_of_advertisement']
        df = pd.DataFrame(data_1,columns=header)
        df.to_sql('list_of_folat')
        
        return df
unit = Flat()
print(unit.parse())
text = BD()
