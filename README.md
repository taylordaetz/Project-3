# Project-3 Web-Scraping from eBay

Project completed for CS40 Computing for the Web at Claremont McKenna College. Here is the [course project](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03)
## `eBay-dl.py`
Overall, this python project extracts html data from eBay and converts it into JSON. In doing this, I can better analyze the data within eBay in a dictionary of items; such as the item name, price, status, shipping, returns and number of items sold. 

I started this file by using argparse to be able to search for items from the command line. Then, I looped over the eBay webpages utilizing the search term item that was inputted from the command line. 

## How to run `ebay-dl.py`
In order to run the eBay program properly, one must write the json to a separate file. The json file is created with the name of the specific search term: 

```
filename = args.search_term+'.json'
with open(filename, 'w', encoding = 'ascii') as f:
    f.write(json.dumps(items))
```

The search term must be input into the command line in the python terminal for the program to run and output a json or csv file. One must ensure that the search term is in quotation marks if there is a space, ie 'water bottle'. 
(NOTE: taylordaetz@Taylors-MacBook-Air-3 project_3 % corresponds to MY current directory): 

```
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'headphones'
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'water bottle'
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'backpack'
```

To export the data as a csv file, one must add a --csv command to the command line. This looks as follows: 

```
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'headphones' --csv=True
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'water bottle' --csv=True
taylordaetz@Taylors-MacBook-Air-3 project_3 % python3 ebay-dl.py 'backpack' --csv=True 
```
