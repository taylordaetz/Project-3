# Project-3 Web-Scraping from eBay

Project completed for CS40 Computing for the Web at Claremont McKenna College. Here is the [course project](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03)
## `eBay-dl.py`
Overall, this python project extracts html data from eBay and converts it into JSON. In doing this, I can better analyze the data within eBay in a dictionary of items; such as the item name, price, status, shipping, returns and number of items sold. 

I started this file by using argparse to be able to search for items from the command line. Then, I looped over the eBay webpages utilizing the search term item that was inputted from the command line. 

## How to run `ebay-dl.py`
In order to run the eBay program properly, one must write the json to a separate file. 

The following commands must be input to the command line in the python terminal (NOTE: CD corresponds to current directory): 

```
CD % python3 ebay-dl.py 'headphones'
CD % python3 ebay-dl.py 'water bottle'
CD % python3 ebay-dl.py 'backpack'
```
