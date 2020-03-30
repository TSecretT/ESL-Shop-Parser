from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import requests
import time
import os
import json
import urllib.request
import telebot
from decimal import Decimal
import os


class ESL():
    folder_name = 'Items'
    PATH = f'{folder_name}/'

<<<<<<< HEAD
    if not os.path.exists(folder_name): os.path.mkdir(folder_name)
=======
def checkItem(link):
    try:
        j = json.loads(requests.get(link+'.js').text)
    except ConnectionError:
        print('Connection error')
        return
    except TimeoutError:
        print('Connection error')
        return
    item={
        'prase_time': time.strftime("%d:%m:%y-%H:%M:%S", time.gmtime(time.time())),
        'id': j['id'],
        'title': j['title'],
        'handle': j['handle'],
        'published': j['published_at'],
        'type': j['type'],
        'sale_price': float(j['price'] / 100),
        'price': float(j['compare_at_price'] / 100),
        'sizes': j['options'][0]['values'],
        'url': j['url'],
        'image_url': 'https://'+j['images'][0][2:],
        'available': j['available']
        }
    return item
>>>>>>> 3203788ffc12cbc68a5b779a6800b496f1c7e17b

    def __init__(self):
        self.pool = ThreadPool(8)

    def get_source(self, link):
        return BeautifulSoup(self.sendRequest(link).content, 'lxml')
    
    def sendRequest(self, url):
        while True:
            try:
                r = requests.get(url)
                return r
            except Exception as e:
                print(f'sendRequest () error {r.status_code} {e}')
                time.sleep(5)

<<<<<<< HEAD
    def checkItem(self, link):
        r = self.sendRequest(link+'.js')
        item = r.json()
        item['prase_time'] = time.strftime("%d:%m:%y-%H:%M:%S", time.gmtime(time.time())),
        return item

    def getItemsUrls(self, i):
        item_urls = []
        soup = self.get_source('https://shop.eslgaming.com/collections/all?page=' + str(i))
        for item in soup.findAll('div', class_='grid-product__content'):
            item_urls.append('https://shop.eslgaming.com'+item.a['href'])
        return item_urls

    def writeData(self, item):
        try:
            with open(self.PATH+item['handle']+'.json', 'r', encoding='utf-8') as file:
                data=json.load(file)
        except:
            data=[]
        finally:
            with open(self.PATH+item['handle']+'.json', 'w', encoding='utf-8') as file:
                data.append(item)
                json.dump(data, file, indent=4)

    def parse(self, anazyle=False):
        soup = self.get_source('https://shop.eslgaming.com/collections/all')
        total_pages = list(range(1,int(soup.find('span', class_='page').text.split('/')[1])+1))
        results = self.pool.map(self.getItemsUrls, total_pages)
        item_urls=[]
        for result in results:
            for item_url in result:
                item_urls.append(item_url)
        item_urls=item_urls[5:]
        results = self.pool.map(self.checkItem, item_urls)
        for result in results:
            if anazyle:
                self.anazyle_data(result)
            self.writeData(result)
=======
def analyzeItems(item):
    priceChange = False
    sizeChange = False
    stateChange = False
    newItem = False
    msg=''
    try:
        with open(PATH+item['handle']+'.json', 'r', encoding='utf-8') as file:
            data=json.load(file)[-1]
        if item['sale_price'] != data['sale_price']:    priceChange = True
        if item['sizes'] != data['sizes']:  sizeChange = True
        if item['available'] != data['available']:  stateChange = True
    except FileNotFoundError:
        newItem = True
        return
    finally:
        if stateChange: msg=msg+'Available:  '+str(item['available'])
        if priceChange: msg=msg+'Price changed from {}€ to {}€\n'.format(item['sale_price'], data['sale_price'])
        if sizeChange: msg=msg+'Sizes changed {}\n'.format(set(item['sizes']) - set(data['sizes']))
        if stateChange or priceChange or sizeChange:
            urllib.request.urlretrieve(item['image_url'], 'image.jpg')
            img = open('image.jpg', 'rb')
            bot.send_photo(admin_id, img, msg)



def check_items(analyze=False):
    print("Parsing ESL items...")
    starttime = time.time()
    soup = get_source('https://shop.eslgaming.com/collections/all')
    total_pages = list(range(1,int(soup.find('span', class_='page').text.split('/')[1])+1))
    pool = ThreadPool(8)
    results = pool.map(getItemUrls, total_pages)
    item_urls=[]
    for result in results:
        for item_url in result:
            item_urls.append(item_url)
    results = pool.map(checkItem, item_urls)
    print('Saving data...')
    if not os.path.exists('Items/'):    os.mkdir('Items')
    for result in results:
        if analyze: analyzeItems(result)
        writeData(result)
    try:
        os.remove("image.jpg")
    except:
        pass
    finishtime = time.time()
    print('Done in ' + str(round(finishtime-starttime, 0)))
>>>>>>> 3203788ffc12cbc68a5b779a6800b496f1c7e17b
