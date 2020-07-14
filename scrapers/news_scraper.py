import requests 
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import sqlite3
from sqlite3 import Error

import sys
import os
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

sites = ["https://www.bbc.co.uk/news", "https://news.sky.com/world", "https://www.ft.com/", "https://www.theguardian.com/world", "https://www.telegraph.co.uk/", "https://www.aljazeera.com/", "https://www.foxnews.com/world"]




        

def scanner():
    headlines = []
    print("=====")
    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}



    for site in sites:
        r = requests.get(site, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        if site == "https://www.bbc.co.uk/news":
            step1 = soup.select_one(".nw-c-top-stories__primary-item")
            step2 = step1.select_one("a")
            step3 = step2.select_one("h3").text
            storylink = 'https://www.bbc.co.uk' + step2['href']
            try:
                storypic = step1.select_one("img")['src']
            except:
                print("NO IMAGE")
                storypic = "https://images.propstore.com/198739.jpg"

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")

            print(storylink)
            print("=====")

            try:
                try: # if not the live blog
                    articletext1 = storypagescanner.select_one(".story-body__inner")
                    articletext2 = articletext1.select("p")
                    articletext3 = ''

                    for p in articletext2:
                        articletext3 = articletext3 + p.get_text() + "\n\n"
                except:# if its the stupid live blog
                    articletext1 = storypagescanner.select_one(".lx-commentary__stream")
                    articletext2 = articletext1.select("p")
                    articletext3 = ''
                    for p in articletext2:
                        articletext3 = articletext3 + p.get_text() + "\n\n"
            except:
                articletext3 = 'None'

                # for p in articletext2:
                #     articletext3 = articletext3 + p.get_text() + "\n\n"

                storypic = articletext1.select_one("img")['src']               

            storyitem = {'Name': 'BBC', 'image': storypic, 'story': step3, 'storylink': storylink, 'slug': slugify(step3), 'body': articletext3}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://news.sky.com/world":
            step1 = soup.select_one(".sdc-site-tile__headline")
            this_headline = step1.select_one("a")

            storylink = 'https://news.sky.com' + this_headline['href']
            storypic = soup.select_one(".sdc-site-tile__image")['src']

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")

            try:
                articletext1 = storypagescanner.select_one(".sdc-article-body")
                articletext2 = articletext1.select("p")
                articletext3 = ''

                for p in articletext2:
                    articletext3 = articletext3 + p.get_text() + "\n"
            except:
                articletext3 = 'None'

            storyitem = {'Name': 'Sky', 'image': storypic, 'story': this_headline.get_text(), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': articletext3}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://www.ft.com/":
            this_headline = soup.select_one(".js-teaser-heading-link")

            storylink = 'https://www.ft.com' + this_headline['href']
            storypic = soup.select_one(".o-teaser__image")['src']



            storyitem = {'Name': 'FT', 'image': storypic, 'story': this_headline.get_text(), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': 'None'}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://www.theguardian.com/world":
            this_headline = soup.select_one(".js-headline-text")

            storylink = soup.select_one(".fc-item__link")['href']
            storypic = soup.select_one("img")['src']

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")
            # currently a live blog - replace soon with a try/except, and if its a live blog dont paste this shitheap (open the page - you'll see)

            try:
                articletext1 = storypagescanner.select(".js-liveblog-body-content")
                articletext2 = ''

                for box in articletext1:
                    titles = box.select("h2")
                    bodies = box.select("p")

                    for title in titles:
                        articletext2 = articletext2 + "\n\n" + title.get_text() + "\n\n"
                    for body in bodies:
                        articletext2 = articletext2 + "\n\n" + body.get_text()
            except:
                articletext2 = 'None'



            storyitem = {'Name': 'The Guardian', 'image': storypic, 'story': this_headline.get_text(), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': articletext2}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://www.telegraph.co.uk/":
            this_headline = soup.select_one(".list-headline__link")

            storylink = 'https://www.telegraph.co.uk' + this_headline['href']
            storypic = 'https://www.telegraph.co.uk' + soup.select_one("img")['src']

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")

            try:
                try:
                    articletext1 = storypagescanner.select_one(".article__layout--content")
                except:
                    articletext1 = storypagescanner.select_one(".article__content")
                    
                articletext2 = articletext1.select("p")

                for p in articletext2:
                    articletext3 = articletext3 + p.get_text() + "\n"

            except:
                articletext3 = 'None'


            storyitem = {'Name': 'The Telegraph', 'image': storypic, 'story': this_headline.get_text().replace("\n", " "), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': articletext3}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://www.aljazeera.com/":
            # this_headline = soup.select_one(".queen-top-sec-title")
            this_headline = soup.select_one(".queen-top-sec-title")
            #this_headline = step1.select_one("a")

            storylink = 'https://www.aljazeera.com' + this_headline['href']

            piclink = requests.get(storylink)
            picpage = piclink.content
            picfinder = BeautifulSoup(picpage, "html.parser")

            try:
                storypic = 'https://www.aljazeera.com' + picfinder.select_one(".img-responsive")['src']
            except:
                storypic = 'https://network.aljazeera.net/sites/aj_corporate/files/styles/varbase_wysiwyg_image/public/shr_shbk_ljzyr_lsly__4.png?itok=RXdG2JNl'



            # storypic = step1.select_one("img")['src']

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")

            try:
                articletext1 = storypagescanner.select_one(".main-article-body")
                articletext2 = articletext1.select("p")

                articletext3 = ''
                for p in articletext2:
                    articletext3 = articletext3 + p.get_text() + "\n\n"
            except:
                articletext3 = 'Non'

            storyitem = {'Name': 'Al Jazeera', 'image': storypic, 'story': this_headline.get_text(), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': articletext3}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

        if site == "https://www.foxnews.com/world":
            step1 = soup.select_one(".info-header")
            step2 = step1.select_one("h2")
            this_headline = step2.select_one("a")

            pic = soup.select_one(".story-1")
            storypic = pic.select_one("img")['src']

            storylink = 'https://www.foxnews.com' + this_headline['href']

            storypage = requests.get(storylink, headers=headers)
            pagecontent = storypage.content
            storypagescanner = BeautifulSoup(pagecontent, "html.parser")

            try:
                articletext1 = storypagescanner.select_one(".article-body")

                # remove various random sign up here type elements
                unwanted_caption = articletext1.select_one(".caption")
                unwanted_caption.extract()
                unwanted_crap = articletext1.select_one(".speakable")
                unwanted_crap.extract()

                articletext2 = articletext1.select("p")

                articletext3 = ''
                for p in articletext2:
                    articletext3 = articletext3 + p.get_text() + "\n\n"
            except:
                articletext3 = 'None'

            storyitem = {'Name': 'FOX', 'image': storypic, 'story': this_headline.get_text(), 'storylink': storylink, 'slug': slugify(this_headline.get_text()), 'body': articletext3}
            headlines.append(storyitem)
            print(storyitem['Name'])
            print(storyitem['story'])

    print("================")
    print("================")

    



    for source in headlines:
        print(source['Name'])


# DJANGO DATABASE
    # if NewsItem.objects.count() < 7:
    #     for source in headlines:
    #         new_news_item = NewsItem(title=source['Name'], image=source['image'], desc=source['story'], addr=source['storylink'], slug= slugify(source['slug']), body=source['body'], archived=False)
    #         new_news_item.save()


    # for source in headlines: # this all now works, but in practice even though it says it has it doesnt change ARCHIVED to TRUE on the object...wtf
    #     #if NewsItem.objects.count() > 0:
    #     for item in NewsItem.objects.all():
    #         if source['Name'] == item.title:
    #             print("CHECKING " + item.title + " -- " + item.desc)
    #             if item.archived == False:
    #                 if source['storylink'] == item.addr:
    #                     print("NOTHING NEW FOR " + item.title)
    #                 else:
    #                     print("NEW STORY DETECTED FOR " + item.title)
    #                     print("CURRENT: " + item.desc)
    #                     print("NEW: " + source['story'])
    #                     # item.archived = True
    #                     item.archive() # this works as well as item.archived = True
    #                     item.save()
    #                     print(item.archived)
    #                     print("ARCHIVED: " + item.desc)
    #                     new_news_item = NewsItem(title=source['Name'], image=source['image'], desc=source['story'], addr=source['storylink'], slug= slugify(source['slug']), body=source['body'], archived=False)
    #                     new_news_item.save()
    #                     print("New article saved for " + item.title)
    #             else:
    #                 print("ARCHIVED. Ignoring.")




