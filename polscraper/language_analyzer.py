import pandas as pd # pylint: disable=import-error
import json
import time
import datetime
from tqdm import tqdm # pylint: disable=import-error
from .sent_terms import categories
from heapq import nlargest
import os
import glob

def country_analyzer(reports, country):
    all_categories = dict(vars(categories))
    scores = {}

    for category in all_categories:
        if "_" not in category:
            scores[category] = 0

    # print("init scores")
    # print(scores)

    for reportfile in glob.glob(f"polscraper\\reports\\*_pol_sentiment_analysis.json"):

        if reportfile[19:35] in reports:
            print(reportfile[19:35])

            with open(f"{reportfile}", encoding="utf-8") as file:
                data = json.load(file)

                countrydata = data[1]
                # print(countrydata)

                for countrydata_object, countrydata_scores in countrydata.items():
                    if countrydata_object == country:
                        # print(countrydata_object)
                        for category_object, number in countrydata_scores.items():
                            for key, value in scores.items():
                                if key == category_object:
                                    scores[key] += number
    
    return scores







def analyzer(filename, numpages):
    all_categories = dict(vars(categories))
    scores = {}
    country_scores = {}

    with open(f"polscraper\\reports\\{filename}") as sentfile:
        data = json.load(sentfile)


    i = 0

    print("Scanning " + str(len(data)) + " threads")
    time.sleep(2)

    # tally up all categories and categories by country
    for category, value in tqdm(all_categories.items()): 
        if "_" not in str(category):
            scores[str(category)] = 0
            
            for thread in data:

                if len(thread['Replies']) > 0:
                    i = 0
                    reply = thread['Replies'][i]['Post']#is this needed?

                    for reply in thread['Replies']:
                        replytext = reply['Post']
                        replyflag = reply['Flag']

                        if replyflag not in country_scores.keys():
                            country_scores[replyflag] = {}
                        
                        if category not in country_scores[replyflag].keys():
                            country_scores[replyflag][category] = 0

                        if any(word.lower() in replytext for word in value):
                            scores[str(category)] += 1
                            country_scores[replyflag][category] += 1

                    i += 1


    analysis_filename = datetime.datetime.now().strftime(f'{filename[:-5]}_analysis.json')

    new_df_data = []

    thedate = datetime.datetime.now().strftime('%Y-%m-%d')
    thetime = datetime.datetime.now().strftime('%H%M')

    d = dict()
    d['Date'] = str(thedate)
    d['Time'] = str(thetime)
    d['Pages'] = numpages

    for key, value in scores.items():
        d[key] = value

    # print("saving:")
    # print(new_df_data)
    # print("******")
    # print(country_scores)
    time.sleep(5)

    new_df_data.append(d)
    new_df_data.append(country_scores)

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

    topics = d
    del topics['Date']
    del topics['Time']
    del topics['Pages']

    # accounting for the community's excessive use of specific slurs
    if topics['blacks'] > 0:
        topics['blacks'] = topics['blacks'] / 5
    if topics['jews'] > 0:
        topics['jews'] = topics['jews'] / 5


    topic = nlargest(3, d, key=topics.get)
    print("\nThe biggest topics of conversation at the moment are:")
    print(topic[0] + ", " + topic[1] + ", and " + topic[2])



