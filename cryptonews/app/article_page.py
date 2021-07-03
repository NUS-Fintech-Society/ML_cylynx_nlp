import streamlit as st
import pandas as pd
from datetime import datetime
from ..db.getEntityScores import getScoresDateRange
from ..db.getEntities import getValidEntityData
from ..db.articles import getArticleData
from ..config import config
from typing import Union
DB_PATH = config.db_path
import plotly.graph_objects as go

def app():

    @st.cache
    def load_ent_data():
        # Function wrapper required for caching
        df = getValidEntityData(DB_PATH)
        df["date_time"] = pd.to_datetime(df["date_time"])
        df = df.drop_duplicates()
        ent_id_map = {name: idx for name,
                      idx in zip(df["name"], df["entity_id"])}
        return list(ent_id_map.keys()), ent_id_map

    @st.cache
    def get_date_range():
        date_range = getScoresDateRange(DB_PATH)
        min_date, max_date = min(date_range), max(date_range)
        min_date = datetime.strptime(min_date, "%Y-%m-%d")
        max_date = datetime.strptime(max_date, "%Y-%m-%d")
        return min_date, max_date

    def get_article_data(entity_id: str, start_date: datetime,
                         end_date: datetime, threshold: int):
        df = getArticleData(entity_id, threshold, DB_PATH)
        df["date_time"] = pd.to_datetime(df["date_time"])
        df = df.drop(["no_entity_flag","article_id"],axis=1)
        df = df.drop_duplicates()
        df = df[(df["date_time"]>=start_date)&(df["date_time"]<=end_date)]
        df["date_time"] = df["date_time"].dt.strftime('%Y-%m-%d')
        return df

    def plotly_df(df):
        fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),
                            align='left'),
                cells=dict(values=[df[col] for col in df.columns],
                        align='left'))
        ])
        return fig

    min_date, max_date = get_date_range()
    st.header("Article Visualisation")

    ent_names, id_map = load_ent_data()
    entity_name = st.selectbox("Entity:", options=ent_names)
    entity_id = id_map[entity_name]
    start_date, end_date = st.slider("Date Range:", min_date, max_date,
                                     value=(min_date, max_date))
    risk_thresh = st.slider("Article Risk Threshold", 0, 100, 50)

    df = get_article_data(entity_id,start_date,end_date,risk_thresh)
    fig = plotly_df(df)
    st.write(fig)
    # https://plotly.com/python/table/#use-a-pandas-dataframe