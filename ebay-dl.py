
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
        return None

def parse_shipping(text):
    amount = ''
    for char in text: 
        if 'free' in text.lower():
            return 0        
        elif char in '1234567890':
            amount += char
        elif char == '':
            break
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
        html = r.text

        #process the html
        soup = BeautifulSoup(html, 'html.parser')
    
        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items: 

            # extract the name 
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name: 
                name = tag.text

            # extract the free returns
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns: 
                freereturns = True

            # extract the items_sold
            items_sold = None
            tags_items_sold = tag_item.select('.s-item__additionalItemHotness, .s-item__hotness, .s-item__itemHotness')
            for tag in tags_items_sold:
                items_sold = parse_itemssold(tag.text)

            # extract the status 
            status = None
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                status = tag.text
            # extract the shipping

            shipping = None
            tags_shipping = tag_item.select('.s-item__logisticsCost, .s-item__freeXDays') 
            for tag in tags_shipping: 
                shipping = parse_shipping(tag.text)

            #extract the price
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
                'items_sold': items_sold
            }
            items.append(item)    


    # write the csv and json to a file

if (args.csv): 
    csv_header=list(items[0].keys())
    csv_filename = args.search_term+'.csv'
    with open(csv_filename, 'w', encoding ='utf-8') as f: 
        writer = csv.DictWriter(f, fieldnames = csv_header)
        writer.writeheader()
        writer.writerows(items)
else:
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding = 'ascii') as f:
        f.write(json.dumps(items))



