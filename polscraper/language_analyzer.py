import pandas as pd # pylint: disable=import-error
import json
import time
import datetime
from tqdm import tqdm # pylint: disable=import-error
# import polscraper# is this needed?
# from polscraper import filename
from .sent_terms import categories, scores
from heapq import nlargest
import os


def analyzer(filename):

    with open(f"polscraper\\reports\\{filename}") as sentfile:
        data = json.load(sentfile)


    i = 0

    print("Scanning " + str(len(data)) + " threads")
    time.sleep(2)


    for thread in tqdm(data):
        if len(thread['Replies']) > 0:
            i = 0
            reply = thread['Replies'][i]['Post']#is this needed?
            for reply in thread['Replies']:
                replytext = reply['Post']
                if any(word.lower() in replytext for word in categories.jews):
                    scores.jews = scores.jews + 1

                if any(word in replytext for word in categories.blacks):
                    scores.blacks = scores.blacks + 1

                if any(word in replytext for word in categories.disease):
                    scores.disease = scores.disease + 1

                if any(word in replytext for word in categories.china):
                    scores.china = scores.china + 1

                if any(word.lower() in replytext for word in categories.africa):
                    scores.africa = scores.africa + 1

                if any(word in replytext for word in categories.europe):
                    scores.europe = scores.europe + 1

                if any(word in replytext for word in categories.usa):
                    scores.usa = scores.usa + 1

                if any(word in replytext for word in categories.southkorea):
                    scores.southkorea = scores.southkorea + 1

                if any(word in replytext for word in categories.japan):
                    scores.japan = scores.japan + 1

                if any(word in replytext for word in categories.northkorea):
                    scores.northkorea += 1

                if any(word in replytext for word in categories.war):
                    scores.war = scores.war + 1

                if any(word in replytext for word in categories.women):
                    scores.women = scores.war + 1

                if any(word in replytext for word in categories.trans):
                    scores.trans = scores.trans + 1

                if any(word in replytext for word in categories.sex):
                    scores.sex = scores.sex + 1

                if any(word in replytext for word in categories.incel):
                    scores.incel = scores.incel + 1

                if any(word in replytext for word in categories.muslims):
                    scores.muslims = scores.muslims + 1

                if any(word in replytext for word in categories.climate):
                    scores.climate = scores.climate + 1

                if any(word in replytext for word in categories.middleeast):
                    scores.middleeast = scores.middleeast + 1

                if any(word in replytext for word in categories.vegans):
                    scores.vegans = scores.vegans + 1

                if any(word in replytext for word in categories.boomers):
                    scores.boomers = scores.boomers + 1

                if any(word in replytext for word in categories.zoomers):
                    scores.zoomers = scores.zoomers + 1

                if any(word in replytext for word in categories.millennials):
                    scores.zoomers = scores.millennials + 1
                
            i += 1



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


