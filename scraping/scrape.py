
from datetime import datetime
import IPython

# Importing General Scraping Functions
from scripts.bitnewstoday import bitnewstoday_scrape_general
from scripts.coindesk import coindesk_scrape_general
from scripts.cointelegraph import cointelegraph_scrape_general
from scripts.cryptonews import cryptonews_scrape_general
from scripts.cryptoslate import cryptoslate_scrape_general

# To change if more sources are added 
sources = ["bitnewstoday","coindesk","cointelegraph","cryptonews","cryptoslate"]


def news_scrape_general(start_date,end_date):
    """
    Scraping of News Data from all sources given start and end date
    If start-date and end-date are strings convert to YYYY-MM-DD

    Args:
        start_date ([type]): [description]
        end_date ([type]): [description]

    Returns:
        [type]: [description]
    """
    if type(start_date) == str:
        start_date = datetime.strptime(start_date,"%Y-%m-%d")
    if type(end_date) == str:
        end_date = datetime.strptime(end_date,"%Y-%m-%d")
    
    #TODO General Scraping Functions for insidebitcoins and nulltx

    scrapers = [eval(i+"_scrape_general") for i in sources]
    news_df = [scraper(start_date,end_date) for scraper in scrapers]
    
    return pd.concat(news_df)
hi = news_scrape_general("2021-01-01","2021-01-05")
IPython.embed()