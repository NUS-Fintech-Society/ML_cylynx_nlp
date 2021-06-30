
from datetime import datetime,timedelta
import pandas as pd
import argparse

# Importing General Scraping Functions
from .scripts.bitnewstoday import bitnewstoday_scrape_general
from .scripts.coindesk import coindesk_scrape_general
from .scripts.cointelegraph import cointelegraph_scrape_general
from .scripts.cryptonews import cryptonews_scrape_general
from .scripts.cryptoslate import cryptoslate_scrape_general

# To change if more sources are added 
sources = ["bitnewstoday","coindesk","cointelegraph","cryptonews","cryptoslate"]


def news_scrape_general(start_datetime, end_datetime):
    """

    start_datetime and end_datetime  are datetime objects
    Args:
        start_date ([type]): [description]
        end_date ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    #TODO General Scraping Functions for insidebitcoins and nulltx

    scrapers = [eval(i+"_scrape_general") for i in sources] #Fetch the relevant scraper function from the news sources
    # news_df = [scraper(start_datetime,end_datetime) for scraper in scrapers]
    news_df = []
    for scraper, source in zip(scrapers,sources):
        print(f"Scraping {source}")
        news_df.append(scraper(start_datetime, end_datetime))
    news_df = pd.concat(news_df)
    return news_df

def save_scraped_data(df,name,dir_name="./scraping/data/"):
    df.to_csv(dir_name+name,index=False)