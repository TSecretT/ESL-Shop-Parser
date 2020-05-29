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
    pool = ThreadPool(8)
    base_url = 'https://shop.eslgaming.com'

    if not os.path.exists(folder_name): os.path.mkdir(folder_name)

    def sendRequest(self, url): #
        while True:
            try:
                r = requests.get(url)
                return r
            except Exception as e:
                print(f'sendRequest () error {r.status_code} {e}')
                time.sleep(5)

    def getSoup(self, link):
        return BeautifulSoup(self.sendRequest(link).content, 'lxml')

    def fetchUrls(self):
        soup = self.getSoup(self.base_url + '/collections/all')
        total_pages = list(range(1,int(soup.find('span', class_='page').text.split('/')[1])+1))
        results = self.combineResults(self.pool.map(self.fetchSinglePage, total_pages))
        return results

    def combineResults(self, results): #
        results_= []
        for result in results:
            results_.extend(result)
        return results_

    def fetchSinglePage(self, page_num):  
        urls = []
        soup = self.getSoup(self.base_url + '/collections/all?page=' + str(page_num))
        for item in soup.findAll('div', class_='grid-product__content'):
            urls.append(self.base_url + item.a['href'])
        return urls

    def fetchItems(self, bot=False): # main function to get data of all items in the shop
        msgs=[]
        itemUrls = self.fetchUrls()
        results =self.pool.map(self.fetchItem, itemUrls)
        for item in results:
            msg = self.compareItem(item)
            msgs.append(msg)
            self.saveData(item)
        if bot:
            return msgs

    def fetchItem(self, url): #fetch data of an items
        res = self.sendRequest(url+'.js').json()
        res['parse_time'] = time.strftime("%d:%m:%y-%H:%M:%S", time.gmtime(time.time()))
        res['parse_time_unix'] = time.time()
        return res

    def saveData(self, item): #save list of items into json
        if os.path.exists(self.PATH+str(item['id'])):
            with open(f"{self.PATH}{item['id']}.json") as file:
                data = json.load(file)
        else:
            data = []
        data.append(item)
        with open(f"{self.PATH}{item['id']}.json", 'w') as file:
            _ = json.dump(data, file, indent=4)

    def compareItem(self, item):
        priceChange = False
        sizeChange = False
        stateChange = False
        newItem = False
        msg = ''
        try:
            with open(f"{self.PATH}{item['id']}.json") as file:
                item_old = json.load(file)[-1]
            if item['price'] != item_old['price']:    priceChange = True
            #if item['sizes'] != item_old['sizes']:  sizeChange = True
            if item['available'] != item_old['available']:  stateChange = True
        except FileNotFoundError:
            newItem = True
        finally:
            if stateChange: msg=msg+'Available:  '+str(item['available'])
            if priceChange: msg=msg+'Price changed from {}€ to {}€\n'.format(item_old['price']/100, item['price']/100)
            #if sizeChange: msg=msg+'Sizes changed {}\n'.format(set(item['sizes']) - set(item_old['sizes']))
            if newItem: msg=msg+f"New item {item['price']/100}"
            item['msg'] = msg
            return item