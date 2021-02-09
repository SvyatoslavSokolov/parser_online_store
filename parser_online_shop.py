from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.request
import urllib
import requests
import re
from datetime import datetime


def page():
    page = urllib.request.urlopen("NEED URL").read()
#    with open('test.html', 'r',encoding='utf-8') as f:
#        page = f.read()
    soup = BeautifulSoup(page, 'lxml')

    final_cost = soup.find('span', {'class': 'final-cost'}).text.replace(' ','').replace(' ','').replace('₽','').replace('\n','')
    brand = soup.find('span', {'class': 'brand'}).text
    name = soup.find('span', {'class': 'name'}).text.replace(' ','', 1)
    params = soup.find('div', {'class': 'params'}).find('div', {'class': 'params'})

    for i in params:
        
        try: i = params.find('div', {'class': 'pp'})
        except BaseException:
            break
        try: i0 = i.find('span').text
        except BaseException:
            break
        i.find('span').decompose()
        
        if 'количест' in i0 or 'Количеств' in i0 or 'кол-во' in i0 or 'Кол-во' in i0:
            kol = 'Кол-во'
            i1 = i.find('span').text
            n = re.findall(r'\d+',i1)
            n = n[0]
            tip = 'шт.'

        if 'Объем' in i0 or 'объем' in i0:
            name_V3 = 'Объем'
            i1 = i.find('span').text
            V3 = re.findall(r'\d+',i1)
            V3 = V3[0]
            if 'мл' in i1 or 'Мл' in i1:
                type_V3 = 'мл'
            else:
                type_V3 = 'л'
                
        params.find('div', {'class': 'pp'}).decompose()

    print(brand)
    print(name)
    print(final_cost)
    print(kol,n,tip)
    print(name_V3,V3,type_V3)
    
def lists():
    n=0
    text_file = open('data.txt','w')
    text_file.write(str('brand'))
    text_file.write('|')
    text_file.write(str('name'))
    text_file.write('|')
    text_file.write(str('quantity'))
    text_file.write('|')
    text_file.write(str('price_now'))
    text_file.write('|')
    text_file.write(str('price_old'))
    text_file.write('|')
    text_file.write(str('sale'))
    text_file.write('|')
    text_file.write(str('product_id'))
    text_file.write('|')
    text_file.write(str('href'))
    text_file.write('|')
    text_file.write(str('data'))
    text_file.write('|')
    text_file.write(str('time'))
    text_file.write('\n')
    
    for page in range(1, 2):
    
        site = urllib.request.urlopen('NEED URL {}'.format(page))
        site = site.read()
        soup = BeautifulSoup(site, 'lxml')
        #with open('test_page.html', 'r',encoding='utf-8') as f:
            #page = f.read()  
        soup = BeautifulSoup(page, 'lxml')

        product_card = soup.find_all('a', {'class': 'ref_goods_n_p j-open-full-product-card'})
        df_name = soup.find_all('div', {'class': 'dtlist-inner-brand-name'})
        df_price = soup.find_all('span', {'class': 'price'})
        k = 0
        
        for name in df_name:

            brand = name.find('strong', {'class': 'brand-name c-text-sm'}).text.replace(' /', '')
            name = name.find('span', {'class': 'goods-name c-text-sm'}).text       
            if 'шт' in name or 'Шт' in name:
                shtuk = re.findall(r'(\d+)',name)
                shtuk = shtuk[0]
                name = re.sub(r'\d+',r'',name)
                name = name.replace(' шт.', '')
            else:
                shtuk = 1
            
            
            price = df_price[k].text.replace('\n','').replace(' ₽','₽ ')
            price = re.sub(r'(\d)\s(\d)',r'\1\2',price)
            price = re.findall(r'(\d+)',price)
            
            price_now = price[0]
            try: price_old = price[1]
            except BaseException:
                price_old = price[0]
            try: sale = price[2]
            except BaseException:
                sale = 0
           
            href = product_card[k].get('href')
            href = 'https://www.wildberries.ru' + href
            product_id = re.search (r'[/]\d+[/]',href)
            product_id = product_id.group().replace('/','')      
            k = k+1


            
            text_file.write(str(brand))
            text_file.write('|')
            text_file.write(str(name))
            text_file.write('|')
            text_file.write(str(shtuk))
            text_file.write('|')
            text_file.write(str(price_now))
            text_file.write('|')
            text_file.write(str(price_old))
            text_file.write('|')
            text_file.write(str(sale))
            text_file.write('|')
            text_file.write(str(product_id))
            text_file.write('|')
            text_file.write(str(href))
            text_file.write('|')
            text_file.write(str(datetime.strftime(datetime.now(), "%Y.%m.%d|%H:%M")))
            text_file.write('\n')
            
            
        n = n +1    
        print('Страница: ',n,' завершена...')
        
    text_file.close()
lists()
