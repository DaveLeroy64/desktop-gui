#https://www.onthemarket.com/for-sale/property/plymouth/

import requests 
from bs4 import BeautifulSoup 
import pandas 
import re 
import numbers
import numpy as np
from datetime import datetime

from . import storage

print("\nProperty data scraper. UK cities only.\n")
search_time = datetime.now().strftime("%Y-%m-%d_%H%M")


def scanner(city, radius):
    search_time = datetime.now().strftime("%Y-%m-%d_%H%M")
    city=city.lower()
    if " " in city:
        city = city.replace(" ", "-")


    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    r = requests.get(f"https://www.onthemarket.com/for-sale/property/{city}/?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("li", {"class":"result property-result panel new first"})


    for page in soup.find_all("ul", {"class":"pagination-tabs"}):
        for num in soup.find_all("li")[-2]:
            try:
                numpages = page.find_all("a",{"class":""})[-1].text
            except:
                numpages = 1



    if len(all) < 1:
        print("\nNothing found. Ensure city name entered correctly.")

    #https://www.onthemarket.com/for-sale/property/plymouth/?page=0&radius=5.0
    i = 0
    proplist = []
    #base_url=(f"https://www.onthemarket.com/for-sale/property/{city}/?page={page}&?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    chars="qwertyuiopasdfghjklzxcvbnm,"

    try:
        print(str(numpages) + " pages of results...\n")
    except:
        print("1 page of results")
        numpages = 1

    # if int(numpages) > 50:
    #     cont = input("Over 50 pages of results. Are you sure you wish to continue? y/n\n")
    #     if "y" in cont:
    #         pass
    #     else:
    #         print("Program terminated")
    #         exit()

    for page in range(0, int(numpages)+1, 1):
        r = requests.get(f"https://www.onthemarket.com/for-sale/property/{city}/?page=" + str(page) + "&?radius={radius}", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup=BeautifulSoup(c, "html.parser")
        all = soup.find_all("li", {"class":"result"})

        for item in all:
            property = {}
            i += 1
            print("property OTM")
            try:
                print(str(item.find("span", {"class":"title"}).text))
            except:
                print("Unknown number of bedrooms")

            try:
                property["Price"]=item.find("a", {"class":"price"}).text
                property["Price"] = ''.join(filter(str.isdigit, property["Price"]))
                if property["Price"] == "":
                    property["Price"] = "0"
            except:
                property["Price"] = "0"

            property["Address"]=item.find_all("span", {"class":"address"})[0].text
            try:
                property["Beds"]=item.find("span", {"class":"title"}).text
                property["Beds"]= ''.join(filter(str.isdigit, property["Beds"]))
            except:
                property["Beds"]="0"
            try:
                property["Agent_Name"]=item.find("a", {"class":"marketed-by-link"}).text
            except:
                property["Agent_Name"]="None"
            try:
                property["Agent_tel"]=item.find("span", {"class":"call"}).text #find("span").text
            except:
                property["Agent_tel"]="None"
            try:
                property['Link']=item.find("a", {"class":"price"})['href']
                property['Link']="www.onthemarket.com" + property['Link']
            except:
                property["Link"]="None"
                
            property["Website"] = "OTM"
            property["Acquire_time"] = str(search_time)
            proplist.append(property)

    if len(proplist) > 0:
        print (str(len(proplist)) + " properties found")
        print ("On " + str(numpages) + " pages\n")
        df = pandas.DataFrame(proplist)
        print(type(df['Beds']))
        for bed in df['Beds']:
            if not isinstance(bed, numbers.Integral):
                bed = 1
            print(bed)
            print(type(bed))

        try:
            otm_avprice = np.asarray(df["Price"], dtype=np.int).mean()
            print("Average Price: ")
            print(otm_avprice)
            print("Properties with price not explicitly specified excluded from average")

            # with open("average_prices.txt", 'a') as file:
            #     file.write(f"\n{search_time}_Average Price from OTM for properties within {radius} miles of {city}: " + "£" + str(int(avprice)))
        
        except:
            print("Cannot calculate average")
            otm_avprice = 0

        avbeds = 0
        for bed in df['Beds']:
            try:
                avbeds += int(bed)
                print("good bed")
            except:
                print("bad bed")

        # try:
        # otm_avbeds = np.asarray(int(df["Beds"]), dtype=np.int).mean()
        otm_avbeds = avbeds / len(df['Beds'])
        print("Average Beds: ")
        print(otm_avbeds)
        
        # except:
        #     print("Cannot calculate average BEDS")
        #     otm_avbeds = 0

        if "-" in city:
            city = city.replace("-", "_")
        print(f"Saving {len(proplist)} properties to {city.upper()} database...")
        storage.connect(city)

        otm_properties_saved = 0
        otm_properties_existing = 0

        for p in proplist: # consider adding tqdm - and removing print statements in storage
            if storage.insert_property(city, 'N/A', p['Price'], p['Address'], p['Beds'], 0, 0, p['Agent_Name'], p['Agent_tel'], p['Website'], p['Acquire_time'], p['Link']) == 'new':
                otm_properties_saved += 1
            else:
                otm_properties_existing += 1
            print(f"Saved {otm_properties_saved} to {city} - {otm_properties_existing} already in database")

        print("Saved to DB")

        return otm_properties_saved, otm_properties_existing, int(otm_avprice), otm_avbeds