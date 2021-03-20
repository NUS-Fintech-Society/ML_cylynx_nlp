
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


def news_scrape_general(start_date,end_date,dir_name="./scraping/data/"):
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

    scrapers = [eval(i+"_scrape_general") for i in sources]
    news_df = [scraper(start_datetime,end_datetime) for scraper in scrapers]
    news_df = pd.concat(news_df)
    filename = dir_name + f"{start_date}_to_{end_date}.csv"
    print("Saving File to ",filename)
    news_df.to_csv(filename,index=False)

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
    if args.dir:
        news_scrape_general(start_date,end_date,args.dir)
    else:
        news_scrape_general(start_date,end_date)



if __name__ == "__main__":
    parser  = argparse.ArgumentParser(description='Script to Scrape News Sources and save as .csv')
    parser.add_argument("start_date",type=str,help="Start Date of Scraping in YYYY-MM-DD format",
                        nargs="?")
    parser.add_argument("end_date",type=str,help="End Date of Scraping in YYYY-MM-DD format",
                        nargs="?")
    parser.add_argument("--dir","-d",help="Directory Folder to Save .csv file")
    args = parser.parse_args()
    main(args)
    