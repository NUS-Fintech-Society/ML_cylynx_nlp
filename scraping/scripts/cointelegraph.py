from bs4 import BeautifulSoup
import requests
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import json


tags = ["bitcoin","litecoin","business","technology","regulation","altcoin","blockchain",
        "ripple","ethereum"]
def cointelegraph_entity_scrape(entity, start_date, end_date):  
    # remove all ' ' characters in url
    entity = entity.replace(' ','+')

    # store data
    data = {'date_time':[], 'title':[], 'excerpt':[], 'article_url':[], 'image_url':[], 'author':[], 'author_url':[], 'source_id': [],"source":[]}

    # retrieve data from url
    url = 'https://cointelegraph.com/search?query=' + entity
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(req, 'html.parser')
    token = soup.find("meta",  attrs={'name':"csrf-token"})['content']
    print(token)

    
    # helper function to retrieve data by entity and page number
    def retrieve_data(entity, page_num, token):
        # retrieve data from cointelegraph API
        r = requests.post("https://cointelegraph.com/api/v1/content/search/result", \
                          params = dict(query=entity,
                                        page=page_num,
                                        _token =token), \
                          headers={'User-Agent': 'Mozilla/5.0'})
        # get results in json format
        results = r.json()
        return results['posts']
        
    page_num = 1
    page_data = retrieve_data(entity, page_num, token)

    # retrieve datetime for the last submission in the page
    last = end_date

    while last >= start_date:
        # stop if there are no search results
        if page_data == []:
            break

        else:
            for article in page_data:
                if article == None:
                    continue
                else:
                    date_time =  datetime.strptime(article['published']["date"], "%Y-%m-%d %H:%M:%S.000000")
                    last = date_time

                    # retrieve article information if it is within specified data range
                    if date_time <= end_date and date_time >= start_date: 
                        data['date_time'].append(date_time)

                        title = article['title']
                        data['title'].append(title)
                    
                        excerpt = article['lead']
                        data['excerpt'].append(excerpt)

                        article_url = article['url']
                        data['article_url'].append(article_url)

                        author_url = article['author_url']
                        data['author_url'].append(author_url)

                        author = article['author_title']
                        data['author'].append(author)

                        image = article['retina']
                        data['image_url'].append(image)

                        source_id = article['id']
                        data['source_id'].append(source_id)

                        data["source"].append("cointelegraph")

            # scrape next page
            page_num += 1
            page_data = retrieve_data(entity, page_num, token)

    df = pd.DataFrame(data)
    return df

def cointelegraph_scrape(start_date=datetime.today()-timedelta(hours=48),end_date= datetime.today()):
    base_url = "http://cointelegraph.com/"
    data = {'date_time':[], 'title':[], 'excerpt':[], 'article_url':[],'author':[],'text':[],"source":[]}


    for tag in tags:
        print(f"Scraping tag: {tag}")
        url = base_url + f"tags/{tag}"
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(req, 'html.parser')
        posts = soup.find_all("a", attrs={"class":"post-card-inline__figure-link"})
        for post in posts:
            link = base_url + post["href"]
            if link in data["article_url"] : continue
            req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
            soup2 = BeautifulSoup(req, 'html.parser')
            article = soup2.find("article")

            #Scraping information from article
            
            datetime_str = article.find("time").attrs["datetime"]
            dt = datetime.strptime(datetime_str,"%Y-%m-%d")

            if dt <start_date or dt > end_date:
                #print(dt)
                continue
            data["date_time"].append(datetime_str)

            text = article.find("div",class_ = "post-meta__author-name").text.strip()
            data["author"].append(text)

            text = article.find("h1",class_ = "post__title").text.strip()
            data["title"].append(text)

            text = article.find("p",class_ = "post__lead").text.strip()
            data["excerpt"].append(text)

            data["article_url"].append(link)
            
            content = article.find("div",class_ ="post-content")
            text = content.get_text().strip()
            data["source"].append("cointelegraph")
            data["text"].append(text)
            

    return pd.DataFrame(data)


import IPython
# url = "http://cointelegraph.com/tags/bitcoin"


# ######################################
article = cointelegraph_scrape(start_date = datetime.today()-timedelta(weeks=32))
article2 = cointelegraph_entity_scrape(" ",start_date = datetime.today()-timedelta(weeks=32),end_date=datetime.today())
IPython.embed()
article.to_csv("scraping/data/cointelegraph_samples.csv",index = False)
# IPython.embed()
# ############### testing ################
# entity = 'Ethereum'
# start_date = datetime(2020, 8, 1)
# end_date = datetime(2020, 10, 25, 23, 59, 59)
# df = cointelegraph_entity_scrape(entity, start_date, end_date)
