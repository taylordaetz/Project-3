'''
1. convert HTML to JSON (compiling)
    - JSON better bc easier to extract and plot info
2. efficiently get info from webpages 
    - like markdown compiler, more things involved
3. search terms: yeti, headphones, backpack

argparse: easier to use from terminal
request library: communicate with ebay website
    *path of url -- "_nkw=stuffed+animals"
        page number "pgn=5"
bs4: parsing html, extraction of info

argsparse
    *no dash -> required argument
    *dash -> can have default
    *for search term with space, put in quotation\

ctrl c to interrupt the code
'''

import argparse
from traceback import print_exception
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text): 
    '''
    takes as input a string and returns the number of items sold, as specified in the string
    >>> parse_itemssold('286 sold')
    286
    >>> parse_itemssold('201 watchers')
    0
    >>> parse_itemssold('Last one')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text: 
        return int(numbers)
    else: 
        return 0

def parse_shipping(text):
    amount = ''
    for char in text: 
        if 'free' in text.lower():
            return 0 
        elif char in '1234567890':
            amount += char
    return int(amount) 

          
def parse_price(text):
    price = ''
    if text[0] =='$':
        for char in text:
            if char in '1234567890':
                price+=char
            elif char == ' ':
                break
        return int(price)
    else: 
        return None



# only run the code below when the python file is run 'normally'
# where normally means not in doctest 
if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default = 10)
    # EXTRA CREDIT add csv from command line
    parser.add_argument('--csv', default =False)
    args = parser.parse_args()
    print('args.search_terms=', args.search_term)

    #list of all items found in all ebay webpages
    items = []

    #loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url += args.search_term
        url += '&_sacat=0&LH_TitleDesc=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=', url)

        #download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status) 
        html = r.text
        #print('html=', html[:50])

        #process the html
        soup = BeautifulSoup(html, 'html.parser')
    
        '''
        for each item in ebay, will get a name and a free return status 
        now: add all things you need with little chunks of code 
        -- make sure you are picking out the good CSS selector when going to (inspect element)
        print('tag=', tag)
            after each item
        '''    
        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items: 

            # extract the name -- starts empty then fills the variable name with the text 
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name: 
                name = tag.text

            # extract the free returns -- starts false unless there is a free-return value (boolean - so needs to be true)
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns: 
                freereturns = True

            # extract the items_sold
            items_sold = None
            tags_items_sold = tag_item.select('.s-item__additionalItemHotness, .s-item__hotness')
            for tag in tags_items_sold:
                items_sold = parse_itemssold(tag.text)

            # extract the status (like name)
            status = None
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                status = tag.text
            # extract the shipping
            shipping = None
            tags_shipping = tag_item.select('.s-item__logisticsCost, .s-item__freeXDays') 
            for tag in tags_shipping: 
                shipping = parse_shipping(tag.text)

            # extract the price (more complicated, remove dollar sign and dot, price in cents)
                # create a function that parses out the price, and call after you have extracted

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)
            

            item = {
                'name': name, 
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)    

        print('len(tags_items)=', len(tags_items))
        print('len(items)=', len(items))

    # write the csv and json to a file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding = 'ascii') as f:
        f.write(json.dumps(items))
'''
if (args.csv) == True: 
    csv_data=list(items[0].keys())
    csv_filename = args.search_term+'.csv'
    with open(csv_filename, 'w', encoding ='utf-8') as f: 
        writer = csv.
else:
'''


