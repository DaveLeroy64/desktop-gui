import pandas as pd # pylint: disable=import-error
import json
import time
import datetime
from tqdm import tqdm # pylint: disable=import-error
# import polscraper# is this needed?
# from polscraper import filename
from .sent_terms import categories
from heapq import nlargest
import os


def analyzer(filename):
    all_categories = dict(vars(categories))
    scores = {}

    with open(f"polscraper\\reports\\{filename}") as sentfile:
        data = json.load(sentfile)


    i = 0

    print("Scanning " + str(len(data)) + " threads")
    time.sleep(2)


    # for thread in tqdmdata:
    #     if len(thread['Replies']) > 0:
            # i = 0

    for category, value in all_categories.items(): 
        if "_" not in str(category):
            scores[str(category)] = 0
            print(str(category) + " key words:")
            print(type(value))
            print(str(value))
            
            for thread in data:
                if len(thread['Replies']) > 0:
                    i = 0
                    reply = thread['Replies'][i]['Post']#is this needed?
                    for reply in thread['Replies']:
                        replytext = reply['Post']
                        print(replytext)
                        print(str(category) + " score: " + str(scores[str(category)]))
                        if any(word.lower() in replytext for word in value):
                            scores[str(category)] += 1
                    # print(str(category) + " score: " + str(scores[str(category)]))
                    print("\n\n")
                    i += 1

            print(scores)
            print("++++++++++")

    ## THIS FINALLY WORKS
    # NOW I JUST NEED TO CHANGE THE BELOW TO BE A FOR LOOP INSTEAD OF WHAT IT CURRENTLY IS!!!


    analysis_filename = datetime.datetime.now().strftime(f'{filename[:-5]}_analysis.json')

    new_df_data = []

    thedate = datetime.datetime.now().strftime('%Y-%m-%d')
    thetime = datetime.datetime.now().strftime('%H%M')
    #print(str(dateandtime))
    d = dict()
    d['Date'] = str(thedate)
    d['Time'] = str(thetime)
    d['Blacks'] = scores.blacks
    d['Jews'] = scores.jews
    d['Disease'] = scores.disease
    d['China'] = scores.china
    d['Africa'] = scores.africa
    d['Europe'] = scores.europe
    d['USA'] = scores.usa
    d['SouthKorea'] = scores.southkorea
    d['Japan'] = scores.japan
    d['NorthKorea'] = scores.northkorea
    d['War'] = scores.war
    d['Women'] = scores.women
    d['Trans'] = scores.trans
    d['Incels'] = scores.incel
    d['Sex'] = scores.sex
    d['Muslims'] = scores.muslims
    d['Climate'] = scores.climate
    d['MiddleEast'] = scores.middleeast
    d['Vegans'] = scores.vegans
    d['Boomers'] = scores.boomers
    d['Zoomers'] = scores.zoomers
    d['Millennials'] = scores.millennials

    new_df_data.append(d)

    with open(f"polscraper\\reports\\{analysis_filename}", 'w') as f:
        json.dump(new_df_data, f)

    print("Analysis saved to " + f"reports\\{analysis_filename}")

    if os.path.exists("Sentiment_analysis.csv"):
        needheader = False
    else:
        needheader = True
    df = pd.read_json(open(f"polscraper\\reports\\{analysis_filename}", 'r'))
    df.set_index('Date', inplace=True)
    df.to_csv("Sentiment_analysis.csv", mode='a', index='Date', header=needheader)
    #print(df)

    topics = d
    del topics['Date']
    del topics['Time']
    topics['Blacks'] = scores.blacks / 5
    topics['Jews'] = scores.jews / 5
    #del topics['Jews']
    topic = nlargest(3, d, key=topics.get)
    print("\nThe biggest topics of conversation at the moment are:")
    print(topic[0] + ", " + topic[1] + ", and " + topic[2])


    scores.blacks=0
    scores.jews=0
    scores.disease=0
    scores.china=0
    scores.africa=0
    scores.europe=0
    scores.usa=0
    scores.southkorea=0
    scores.japan=0
    scores.northkorea=0
    scores.war=0
    scores.women=0
    scores.trans=0
    scores.incel=0
    scores.sex=0
    scores.muslims=0
    scores.climate = 0
    scores.middleeast = 0
    scores.vegans = 0
    scores.boomers = 0
    scores.zoomers = 0
    scores.millennials = 0


