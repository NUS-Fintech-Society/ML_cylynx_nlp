from scrape import news_scrape_general
#from models import predictSentiment, predictNER #TODO: Replace with actual function name
import os
import pandas as pd
import datetime
from datetime import date

#? I think this file should be redundant with the new main.py file outside this directory

def main(): # Will run for today
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    news_scrape_general(start_date, end_date, './temp/')
    
    filename = f"./temp/{start_date}_to_{end_date}.csv"
    df = pd.read_csv(filename)
   
    '''
    Load models here
    '''

    '''
    Predict NER
    '''

    '''
    namedEntityTitle = [predictNER(x) for x in df['title']] # A list of named entities on titles
    namedEntityExcerpt = [predictNER(x) for x in df['excerpt']] # A list of named entites on excerpts
    '''

    ''' 
    Predict sentiment
    '''
    
    '''
    sentimentTitle = [predictSentiment(x) for x in df['title']]
    sentimentExcerpt = [predictSentiment(x) for x in df['excerpt']]
    '''

    '''
    Save to csv 
    '''
    
    df['NER_Title'] = [0 for i in range(len(df['title']))] # namedEntityTitle
    df['NER_Sentiment'] = [0 for i in range(len(df['title']))] # namedEntityExcerpt
    df['Sentiment_Title'] = [0 for i in range(len(df['title']))] #sentimentTitle
    df['Sentiment_Excerpt'] = [0 for i in range(len(df['title']))] #sentimentExcerpt
    df.to_csv(filename)
    

if __name__ == "__main__":
    main()
