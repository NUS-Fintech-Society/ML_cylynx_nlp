def process_duplicates(df):
    '''
    Accepts a pandas dataframe and outputs 
    '''
    if df.empty:
        df["count"] = 0
        df["date_time_first"] = ""
        return df
    
    # assign count based on text and entity
    df["count"] = df.groupby(by=["text", "entity"]).text.transform('size')

    # get array of all date times
    df = df.merge(df.groupby(['text', 'entity']).date_time.agg(list).reset_index(), 
              on=['text', 'entity'], 
              how='left',
                  suffixes=['', '_all'])
    
    # drop duplicates, keeping the first
    df = df.drop_duplicates(subset=["text", "entity"], keep='first')
    return df
