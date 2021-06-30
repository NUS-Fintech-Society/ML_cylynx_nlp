# importing packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def bitcoin_scrape(entity, start_date, end_date):
    # create output df
    column_names = ['date_time', 'title', 'excerpt', 'article_url', 'image_url', 'category']
    output = pd.DataFrame(columns = column_names)

    page_number = 1
    continue_search = True

    # continue_search = False when date_time < start_date
    while continue_search:
        # retrieve HTML content
        html = requests.get("https://news.bitcoin.com/page/{}/?s={}".format(page_number, entity))
        html_content = html.content

        # locate relevant sections
        soup = BeautifulSoup(html_content, 'html.parser')
        news = soup.find_all('div', class_='td_module_16 td_module_wrap td-animation-stack')
        news_details = soup.find_all('div', class_='td-module-meta-info')
        news_excerpt = soup.find_all('div', class_='td-excerpt')

        # loop through all articles on the page
        for i in range(0, len(news)):
            # retrieve relevant attributes
            # note datetime string is in the format '2020-06-01T14:04:01+00:00'
            date_time_str = news[i].find('time')['datetime'][0:10]
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d')
            title = news[i].find('a')['title']
            article_url = news[i].find('a')['href']
            image_url = news[i].find('img')['src']
            excerpt = news_excerpt[i].get_text()
            try: 
                category = news_details[i].find('a').get_text()
            except:
                category = ''
                pass

            # check whether datetime is wihin range
            if (date_time <= end_date) and (date_time >= start_date):
                # append row to data frame
                output = output.append({'date_time': date_time, 'title': title, 'excerpt': excerpt, \
                                        'article_url': article_url, 'image_url': image_url, \
                                        'category': category}, ignore_index=True)
            
            # terminating conditions
            if (date_time < start_date):
                continue_search = False
        
        # break loop if no search results
        if len(news) == 0:
            break
        
        # increment page number
        page_number += 1
    
    return output

def get_date_string(dt):
    year = str(dt.year)[-2:]
    month = str(dt.month)
    day = str(dt.day)
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    date_string = day + month + year
    return date_string

def bitcoin_general_scrape(start_date, end_date):
    return bitcoin_scrape("", start_date, end_date)

def save_for_tagging(data, filepath):
    column_names = ['date_time', 'title', 'excerpt', 'article_url', 'image_url', 'category']
    data['tagging_text'] = data[['title', 'excerpt']].agg(' '.join, axis=1)
    data.drop(column_names, axis=1, inplace=True)
    data.to_csv(filepath + "tagging.csv", header=None, index=None)

##Testing
# entity="ethereum"
# start_date = datetime(2020, 7, 20)
# end_date = datetime(2020, 12, 30)
# start = get_date_string(start_date)
# end = get_date_string(end_date)
# name = start + "_to_" + end + ".csv"
# df = bitcoin_scrape(entity, start_date, end_date)
# df.to_csv("../data/bitcoin_feed/" + name)
##Save for labelling
# start_date = datetime(2021, 1, 1)
# end_date = datetime(2020, 2, 28)
# save_for_tagging(bitcoin_general_scrape(start_date, end_date), "../data/bitcoin_feed/")
