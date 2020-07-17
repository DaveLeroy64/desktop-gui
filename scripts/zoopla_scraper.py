#https://www.zoopla.co.uk/for-sale/houses/edinburgh/?q=Edinburgh&radius=40&results_sort=newest_listings&search_source=refine
#https://www.zoopla.co.uk/for-sale/houses/edinburgh/?identifier=edinburgh&property_type=houses&q=Edinburgh&search_source=refine&radius=40&pn=2

import requests 
from bs4 import BeautifulSoup, SoupStrainer
import pandas
import re 
import numpy as np
import os
import datetime
from copy import deepcopy
from tqdm import tqdm
from datetime import datetime

from . import storage

numpages = 1
# idea for connecting to progress bar

# one function here that calculates the number of pages
# this data is passed to properties.py which then does a loop
# over every page, that calls the PAGE SCAN function contained in HERE,
# that scrapes the properties off THAT page

# since the over 50 pages prompt crashes Qt, we can then pass that prompt to a
# popupbox that is prompted if the return from the pages calc function is over 50
# the OK button can then continue the scan, or cancel can abort it

def scanner(city, radius):
    global numpages
    accepted_radii = [1, 3, 5, 10, 15, 20, 30, 40]

    if int(radius) not in accepted_radii:
        return "Please enter a search radius of\n1, 3, 5, 10, 15, 20, 30 or 40 miles"


    search_time = datetime.now().strftime("%Y-%m-%d_%H%M")



    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    r = requests.get(f"https://www.zoopla.co.uk/for-sale/houses/{city}/?identifier={city}&property_type=houses&q={city}&search_source=refine&radius={radius}&pn=1", headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class":"listing-results-wrapper"})


    for page in soup.find_all("div", {"class":"paginate bg-muted"}):
        print("trying to find pages")
        numpages = page.find_all("a")[-2].text
        print(numpages)
        print("++++++++++++++")

    try:
        print(str(numpages) + " pages of results...\n")
    except:
        print("1 page of results")
        numpages = 1


    if len(all) < 1:
        print("\nNothing found. Ensure city name entered correctly.")

    i = 0
    proplist = []
    base_url=f"https://www.zoopla.co.uk/for-sale/houses/{city}/?identifier={city}&page_size=100&property_type=houses&q={city}&search_source=refine&radius={radius}&pn="
    chars="qwertyuiopasdfghjklzxcvbnm,"

    # if int(numpages) > 50:
    #     cont = input("Over 50 pages of results. Are you sure you wish to continue? y/n: ")
    #     if "y" in cont:
    #         pass
    #     else:
    #         print("Program terminated")
    #         exit()

    print("\nScanning " + str(numpages) + " pages...\n")

    for page in tqdm(range(1, int(numpages)+1, 1)):
        r = requests.get(base_url + str(page))
        c = r.content
        soup=BeautifulSoup(c, "lxml")
        all = soup.find_all("div", {"class":"listing-results-wrapper"})

        for item in all:

            property = {}
            i += 1

            property["Date_Listed"]=item.find("p", {"class":"top-half listing-results-marketed"}).find("small").text.replace(" ", "").replace("\n", "").replace("Listedon", "").replace("by", "")
            try:
                property["Price"] = item.find("a", {"class":"listing-results-price text-price"}).text.replace("\n", "").replace("Offersinregionof", "").replace(" ", "").replace("Offersover", "")
                property["Price"] = ''.join(filter(str.isdigit, property["Price"]))
                if property["Price"] == "":
                    property["Price"] = "0"
            except:
                property["Price"] = "0"

            property["Address"]=item.find_all("a", {"class":"listing-results-address"})[0].text

            try:
                property["Beds"]=item.find("span", {"class":"num-icon num-beds"}).text
            except:
                property["Beds"]="0"
            try:
                property["Bathrooms"]=item.find("span", {"class":"num-icon num-baths"}).text
            except:
                property["Bathrooms"]="0"
            try:
                property["Reception_rooms"]=item.find("span", {"class":"num-icon num-reception"}).text
            except:
                property["Reception_rooms"]="0"
            try:
                property["Agent_Name"]=item.find("p", {"class":"top-half listing-results-marketed"}).find("span").text
            except:
                property["Agent_Name"]="None"
            try:
                property["Agent_tel"]=item.find("span", {"class":"agent_phone"}).find("span").text
            except:
                property["Agent_tel"]="None"
            property["Website"] = "Zoopla"
            property["Acquire_time"] = str(search_time)

            proplist.append(property)

    if len(proplist) > 0:
        print (str(len(proplist)) + " properties found")
        print ("On " + str(numpages) + " pages\n")
        df = pandas.DataFrame(proplist)

        try:
            zoo_avprice = np.asarray(df["Price"], dtype=np.int).mean()
            print("Average Price: ")
            print(zoo_avprice)
            print("Properties with price not explicitly specified excluded from average")

            # with open("average_prices.txt", 'a') as file:
            #     file.write(f"\n{search_time}_Average Price from Zoopla for properties within {radius} miles of {city}: " + "£" + str(int(avprice)))
        
        except:
            print("Cannot calculate average")
            zoo_avprice = 0

        
        print(f"Saving {len(proplist)} properties to {city.upper()} database...")
        storage.connect_property(city)

        zoo_properties_saved = 0
        zoo_properties_existing = 0

        for p in proplist: # consider adding tqdm - and removing print statements in storage
            if storage.insert_property(city, p['Date_Listed'], p['Price'], p['Address'], p['Beds'], p['Bathrooms'], p['Reception_rooms'], p['Agent_Name'], p['Agent_tel'], p['Website'], p['Acquire_time']) == 'new':
                zoo_properties_saved += 1
            else:
                zoo_properties_existing += 1
            print(f"Saved {zoo_properties_saved} to {city} - {zoo_properties_existing} already in database")

        print("Saved to DB")
        sendback = f"{zoo_properties_saved} properties within {radius}m\nAverage Price: £{round(zoo_avprice, 2)}"
        if zoo_properties_existing > 0:
            sendback += f"\n{zoo_properties_existing} already stored"
        return zoo_properties_saved, zoo_properties_existing, int(zoo_avprice)