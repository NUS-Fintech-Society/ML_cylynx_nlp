
from datetime import datetime,timedelta
import pandas as pd
import argparse

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

    start_date and end_date  are strings of format YYYY-MM-DD

    Args:
        start_date ([type]): [description]
        end_date ([type]): [description]

    Returns:
        [type]: [description]
    """

    start_datetime = datetime.strptime(start_date,"%Y-%m-%d")
    end_datetime = datetime.strptime(end_date,"%Y-%m-%d")
    
    #TODO General Scraping Functions for insidebitcoins and nulltx

    scrapers = [eval(i+"_scrape_general") for i in sources] #Fetch the relevant scraper function from the news sources
    news_df = [scraper(start_datetime,end_datetime) for scraper in scrapers]
    news_df = pd.concat(news_df)
    return news_df

def save_scraped_data(df,name,dir_name="./scraping/data/"):
    df.to_csv(dir_name+name,index=False)

def main(args):
    if not args.start_date:
        #If no Start Date, there will be no end date arg as well
        start_date = datetime.today() - timedelta(hours = 24)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = datetime.today()
        end_date = end_date.strftime("%Y-%m-%d")
    else: 
        start_date = args.start_date
        end_date = args.end_date
    df = news_scrape_general(start_date,end_date)
    if args.name:
        save_scraped_data(df,args.name)
    return df
        



if __name__ == "__main__":
    # Script will save data in a .csv form if run using command line
    parser  = argparse.ArgumentParser(description='Script to Scrape News Sources and save as .csv')
    parser.add_argument("start_date",type=str,help="Start Date of Scraping in YYYY-MM-DD format",
                        nargs="?")
    parser.add_argument("end_date",type=str,help="End Date of Scraping in YYYY-MM-DD format",
                        nargs="?")
    parser.add_argument("--name","-n",help="Name of saved file, leave blank to not save the file")
    args = parser.parse_args()
    df = main(args)
    