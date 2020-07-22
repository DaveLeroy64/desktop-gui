import pandas as pd # pylint: disable=import-error
import json
import time
import datetime
from tqdm import tqdm # pylint: disable=import-error
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


    for category, value in tqdm(all_categories.items()): 
        if "_" not in str(category):
            scores[str(category)] = 0
            
            for thread in data:

                if len(thread['Replies']) > 0:
                    i = 0
                    reply = thread['Replies'][i]['Post']#is this needed?

                    for reply in thread['Replies']:
                        replytext = reply['Post']

                        if any(word.lower() in replytext for word in value):
                            scores[str(category)] += 1

                    i += 1



    analysis_filename = datetime.datetime.now().strftime(f'{filename[:-5]}_analysis.json')

    new_df_data = []

    thedate = datetime.datetime.now().strftime('%Y-%m-%d')
    thetime = datetime.datetime.now().strftime('%H%M')

    d = dict()
    d['Date'] = str(thedate)
    d['Time'] = str(thetime)

    for key, value in scores.items():
        d[key] = value

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

    topics = d
    del topics['Date']
    del topics['Time']
    if topics['blacks'] > 0:
        topics['blacks'] = topics['blacks'] / 5
        print("Weighting BLACK topic down")
    if topics['jews'] > 0:
        topics['jews'] = topics['jews'] / 5
        print("Weighting JEW topic down")


    topic = nlargest(3, d, key=topics.get)
    print("\nThe biggest topics of conversation at the moment are:")
    print(topic[0] + ", " + topic[1] + ", and " + topic[2])



