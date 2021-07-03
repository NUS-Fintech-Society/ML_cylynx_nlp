import streamlit as st
from ..db.getEntities import getValidEntityData
import pandas as pd
import plotly.express as px

from ..config import config
DB_PATH = config.db_path

def app():
    
    @st.cache
    def load_data():
        # Function wrapper required for caching
        df = getValidEntityData(DB_PATH)
        df["date_time"] = pd.to_datetime(df["date_time"])
        ent_names = df["name"].unique()
        return df,ent_names
        
    def single_entity_chart(df,ent_name):

        df_slice = df[df["name"] == ent_name].copy()
        df_slice = df_slice.sort_values(by="date_time",ascending=True)
        fig = px.line(df_slice,x="date_time",y="entity_score")
        fig.update_yaxes(range=(0,100))
        return fig

    def multiple_entity_chart(df,ent_names):
        if not ent_names:
            return px.line()
        df_slice = df[df["name"].isin(ent_names)].copy()
        df_slice = df_slice.sort_values(by="date_time",ascending=True)
        fig = px.line(df_slice,x="date_time",y="entity_score",color ="name")
        return fig

    df,ent_names = load_data()
    st.title("Blockchain Risk Visualisation")
    st.markdown("This is a tool which is used to visualise the risk score "
        "of entities over a period of time")

    st.subheader("Single Entity Visualisation")
    df,ent_names = load_data()

    entity_name = st.selectbox("Entity:",options = ent_names)
    st.plotly_chart(single_entity_chart(df,entity_name))


    st.subheader("Multiple Entity Visualisation")
    entity_names = st.multiselect("Select Entities:",options = ent_names)
    st.plotly_chart(multiple_entity_chart(df,entity_names))
