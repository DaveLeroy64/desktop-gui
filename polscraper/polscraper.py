import requests # pylint: disable=import-error
from bs4 import BeautifulSoup, SoupStrainer # pylint: disable=import-error
import pandas # pylint: disable=import-error
import re # pylint: disable=import-error
import numpy as np
import os
import datetime 
from datetime import timedelta
import time
from copy import deepcopy
from tqdm import tqdm # pylint: disable=import-error
from html.parser import HTMLParser
import json
import os
from .language_analyzer import analyzer

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

r = requests.get('https://boards.4chan.org/pol/', headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c, "html.parser")

#pages = [""]

def test(pages, interval):
    print(pages)
    print(interval)

def scanner(pages):
    
    filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M_pol_sentiment.json')
    
    all_post_data = []

    #print("Scanning threads...")
    for page in pages:
        r = requests.get(f'https://boards.4chan.org/pol/{page}', headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        threads = soup.select(".thread")
        #print(f"----------SCANNING PAGE {page}----------")

        #GET OP's
        print(f"Scanning page {page}")
        for thread in tqdm(threads):
            title = thread.select_one(".subject")
            op = thread.select_one(".opContainer blockquote")
            op_name = thread.select_one(".name").get_text()
            op_id = thread.select_one(".hand").get_text()
            try:
                op_flag = thread.select_one(".flag")['title']
            except:
                op_flag = "Unknown or no flag"
            time = thread.find("span", {"class":"dateTime"} )
            replyLink = thread.find("a", {"class":"replylink"})['href']

            #OPTIONAL PRINT TO CONSOLE
            # if title == "":
            #     print("No title")
            #     title = "No title"
            # else:
            #     print(title.get_text())
            # print(op_flag)
            # print(op_name)
            # print(op_id)
            # print(time.get_text())
            # print(op.get_text())

            thread_data = dict()

            thread_data['Title'] = title.get_text()
            thread_data['Flag'] = op_flag
            thread_data['OP Name'] = op_name
            thread_data['OP ID'] = op_id
            thread_data['Date'] = time.get_text()
            thread_data['OP'] = op.get_text()
            thread_data['Replies'] = []


            #GET REPLIES
            get_whole_thread = requests.get(f'https://boards.4chan.org/pol/{page}/{replyLink}', headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
            whole_thread = get_whole_thread.content
            replyscanner = BeautifulSoup(whole_thread, "html.parser")
            replies = replyscanner.select(".replyContainer")

            for reply in replies:
                reply_data = dict()

                try:
                    reply_name = reply.select_one(".name").get_text()
                except:
                    reply_name = "Unknown"
                try:
                    reply_post = reply.select_one(".postMessage").get_text()
                except:
                    reply_post = "Empty post"
                try:
                    reply_id = reply.select_one(".hand").get_text()
                except:
                    reply_id = "Unknown"
                try:
                    reply_flag = reply.find('span', {'class':'flag'})['title']
                except:
                    reply_flag = "No flag"

                # #OPTIONAL PRINT TO CONSOLE
                # print(" ")
                # print(reply_name)
                # print(reply_flag)
                # print(reply_id)
                # print(reply_post)
                # print(" ")

                reply_data['Flag'] = reply_flag
                reply_data['name'] = reply_name
                reply_data['id'] = reply_id
                reply_data['Post'] = reply_post

                thread_data['Replies'].append(reply_data)


            all_post_data.append(thread_data)

            #EXCLUDE IF NOT PRINTING THREADS
            #print("==========================================\n\n\n")



    #Save to JSON
    os.makedirs(os.path.dirname('.\\polscraper\\reports\\'), exist_ok=True)
    with open(f"polscraper\\reports\\{filename}", 'w+') as file:
        json.dump(all_post_data, file)
    print("Data saved in file: " + "reports\\" + filename)

    print("Running language analysis...")
    analyzer(filename)
    
    return len(pages), len(threads), len(replies)
    

def repeating(scan_delay, pages):
    scanpages = [*range(2, int(pages)+1)]
    scanpages.insert(0, "")

    hour_interval = int(scan_delay.split()[0])
    scan_delay = int(hour_interval) * 3600
    
    while True:
        pages, threads, replies = scanner(scanpages)
        current_time = datetime.datetime.now()#.strftime('%H%M:%S')
        next_scan_time = current_time + datetime.timedelta(seconds=int(scan_delay))
        print(f"Next scan will take place at: {str(next_scan_time.strftime('%H:%M:%S'))}")
        time.sleep(int(scan_delay))
        print("\nRestarting scan\n")
    return pages, threads, replies

def single(pages):
    if pages == 1:
        pages = [""]
    else:
        scanpages = [*range(2, int(pages)+1)]
        scanpages.insert(0, "")
        print("scanning:")
        print(scanpages)
        print("---")
    pages, threads, replies = scanner(scanpages)
    time.sleep(2)
    print("Scan complete. Program terminated.")
    # exit()
    return pages, threads, replies

def init():
    run_mode = input("Run scan once or in repeat?\n")
    scanpages = int(input("Number of pages to scan (1-10): "))
    if scanpages <= 10:
        pages = [*range(2, scanpages+1)]
        pages.insert(0, "")
    elif scanpages == 1:
        pages = [""]
    else:
        print("Error: number of pages must not exceed 10")
        init()

    if run_mode == "once":
        single(pages)
    elif run_mode == "repeat":
        scan_delay = int(input("Enter scan frequency (seconds): "))
        if scan_delay < 60:
            print("Scan delay must be at least 60 seconds")
            init()
        else:
            repeating(scan_delay, pages)
    else:
        print("Input not recognised. Please try again.")
        init()


