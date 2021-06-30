import pandas as pd
import requests
from datetime import datetime, timedelta
import time

def coindesk_scrape(entity, start_date, end_date):

    # dictionary to store the relevant data
    data_store = {'date_time':[], 'title':[], 'excerpt':[], 'article_url':[],  'author':[], 'image_url':[], 'source':[]}

    # request and get url
    def retrieve_data(entity, page):
        # link to retrieve data from
        url = 'https://www.coindesk.com/wp-json/v1/search?keyword=' + str(entity) + '&page=' + str(page)
        data = requests.get(url).json()
        return data['results']

    page = 1
    page_data = retrieve_data(entity, page)

    # retrieve datetime for the last submission in the page
    last = end_date

    while last >= start_date:
        # if there are no search results, stop
        if page_data == []:
            break
        else:
            for article in page_data:
                #add 8 hours to convert to SGT
                date_time =  datetime.strptime(article['date'], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)
                last = date_time

                # retrieve relevant information from article
                if date_time <= end_date and date_time >= start_date: 
                    data_store['date_time'].append(date_time)
                    data_store["source"].append("coindesk")
                    title = article['title']
                    data_store['title'].append(title)
                
                    excerpt = article['text']
                    data_store['excerpt'].append(excerpt)

                    article_url = article['url']
                    article_url = article_url.replace("\\", "")
                    data_store['article_url'].append(article_url)

                    author = article['author'][0]['name']
                    data_store['author'].append(author)

                    # try except block for articles without image url
                    try:
                        image = article['images']['images']['desktop']['src']
                        data_store['image_url'].append(image)
                    except:
                        data_store['image_url'].append('')
            
            # increment page number
            page += 1
            page_data = retrieve_data(entity, page)

    df = pd.DataFrame(data_store)
    return df

def coindesk_scrape_general(start_date, end_date):
    return coindesk_scrape("", start_date, end_date)


##########Testing entity function ##########
##entity = 'ethereum'
##start_date = datetime(2021, 1, 1)
##end_date = datetime(2021, 1, 31,23,59,59)
##df = coindesk_scrape(entity, start_date, end_date)
##df.to_csv("../data/coindesk_feed/010121_to_310121.csv")
########################################

######### Testing general function ########
##start_date = datetime(2021, 1,22)
##end_date = datetime(2021, 2, 21,23,59,59)
##df = coindesk_scrape_general(start_date, end_date)
##sample = df.sample(n=200,random_state=1)
##sample["text"] = sample["title"] + " " + sample["excerpt"]
##sample.to_csv("./sample.csv")
########################################
