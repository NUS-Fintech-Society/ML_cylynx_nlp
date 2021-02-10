import praw
import pandas as pd
import requests
import IPython
from datetime import datetime,timedelta
from psaw import PushshiftAPI
from utils import *


### Ideally all this should be placed in a YAML File
CLIENT_ID = "ZiucI09RvVbXPQ"
CLIENT_SECRET = "7arVbStENxW_9ERB9rrpXbH3HUYJrQ"
USER_AGENT = "crypto_scraper by u/data_science_dude"
subreddit_file = "scraping/data/subreddits.csv"

FIELDS = ['selftext',"title","created"]
#######################################


def get_reddit_instance():
    reddit = praw.Reddit(client_id = CLIENT_ID, 
                         client_secret = CLIENT_SECRET,
                         user_agent = USER_AGENT)
    return reddit


def get_subreddits(file_path):
    '''
    Obtain a list of subreddits to look at by reading a .csv file
    '''
    df = pd.read_csv(file_path)
    subreddit_list = df["subreddits"].tolist()
    return subreddit_list


def subreddit_scrape(subreddit,start_date,end_date,limit = 1000):
    """Scrape listings from a particular subreddit
    The scraping will be using the 

    Args:
        subreddit (Subreddit Object): Subreddit Object from the Reddit API Client
        start_date (datetime):
        end_date (datetime)

    Returns:
        df(pd.DataFrame): DataFrame containing the columns: 
                        [author, url, excerpt, subreddit, title, article_date,
                         type, entity, source_id, content
                         date_time_all, coin, source]
    """
    entries = []
    for submission in subreddit.hot(limit = limit):
        entry = {}
        #Convert to dictionary for better indexing 
        sub_dict= submission.__dict__
        for field in FIELDS:
            entry[field] = sub_dict[field]
        entries.append(entry)
    df = pd.DataFrame.from_dict(entries)
    df["created"] = df['created'].apply(lambda x:datetime.fromtimestamp(x))
    df.rename({"selftext":"text"})
    return df

def reddit_scrape_by_entity(entity, start_date, end_date):
    '''
    Retrieves posts relating to entity from reddit within the stipulated time frame 

    Input:
        entity(string): entity name to retrieve data on
        start_date(datetime): date to begin scraping from
        end_date(datetime): date to stop scraping
    Output:
        df(dataframe): dataframe with columns = [author, url, excerpt, subreddit, title, article_date, type, entity,
                                    	        source_id, content, date_time_all, coin, source]
    '''

    # initialise api
    api = PushshiftAPI()

    # convert datetime to timestamp
    start_epoch = int(start_date.timestamp())
    end_epoch = int(end_date.timestamp())

    # read in list of subreddits
    subreddits = pd.read_csv(subreddit_file)['subreddits'].tolist()
    entity = entity.lower()

    ############################## Submissions ################################
    
    # query and generate the related information
    gen_submission = api.search_submissions(q=entity,after= start_epoch, before = end_epoch,
            filter=['created_utc', 'title', 'selftext', 'permalink', 'author', 'subreddit', 'id'],
            subreddit = subreddits)

    # generate dataframe for required data

    df = pd.DataFrame.from_dict([post.d_ for post in gen_submission])

    # format dataframe 
    if len(df):
        df['title'] = df['title'].apply(lambda x: str(x).lower())
        df['date_time'] = df['created_utc'].apply(lambda x: datetime.fromtimestamp(x))
        df['selftext'] = df['selftext'].apply(lambda x: str(x).lower())
        df['permalink'] = df['permalink'].apply(lambda x: 'www.reddit.com'+ x)
        df['author'] = df['author'].apply(lambda x: x.lower())
        df['subreddit'] = df['subreddit'].apply(lambda x: x.lower())
        df['type'] = 'submission'

        #Remove unecessary columns of data
        df = df.drop(columns = ['created_utc','created'])

        df= df.rename(columns={'selftext': 'excerpt', 'permalink':'article_url'})
    else:
        print("Scraped DataFrame is Empty")
        return 
    
    
    df['entity'] = entity
    df["text"] = df["title"] + " " + df["excerpt"]

    # filter out irrelevant data

    # process duplicates
    df = process_duplicates(df)

    # find all coins that are relevant in text

    # reset index
    df = df.reset_index(drop=True)

    # add source column
    df['source'] = 'reddit'

    # rename dataframe using naming convention in final database
    df = df.rename({'text':'content', 'article_url':'url', 'date_time':'article_date','id':'source_id'}, axis = 1)
    
    # keep only relevant columns
    df = df[['source','source_id','article_date','content', 'url','entity', 'author']]

    return df


def reddit_scrape(entity_list, start, end):
    '''
    Retrieves posts relating to entitities in entity list from reddit within the stipulated time frame 

    Input:
        entity_list(list): list of entity names to retrieve data on
        start_date(datetime): date to begin scraping from
        end_date(datetime): date to stop scraping
    Output:
        df(dataframe): dataframe with columns = [author, url, excerpt, subreddit, title, article_date, type, entity,
                                    	        source_id, content,  date_time_all, coin, source]
    '''

    #Create empty dataframe
    output_df = pd.DataFrame()

    #Iterate through list of entities
    for entity in entity_list:

        #retrieve dataframe consisting of all data for each entity
        df = reddit_scrape_by_entity(entity, start, end)

        #Join the dataframes by column
        output_df = output_df.append(df)

    # reset index
    output_df = output_df.reset_index(drop=True)
    
    return output_df
# if __name__ == "__main__":
#     reddit = get_reddit_instance()
#     subreddit_list = get_subreddits(subreddit_file)
#     srs = [reddit.subreddit(i) for i in subreddit_list]

start_date = datetime(2020, 10, 15)
end_date = datetime(2020, 10, 26, 23, 59, 59)
df = reddit_scrape_by_entity("ethereum",start_date,end_date)
IPython.embed()
