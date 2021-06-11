import streamlit as st
import app_utils
import pandas as pd
import plotly.express as px
# import seaborn as sns

@st.cache
def load_data():
    # Function wrapper required for caching
    df = app_utils.fetch_data()
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

pages = ["Entity Visualisation","Article Visualisation","Graph Visualisation"]
choice = st.sidebar.radio("App Page: ",pages)
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





st.markdown(
    """
    - [ ] Code to group entities with the same names together
    - [ ] Preprocessing Functions to better filter out unwanted items
    - [ ] Blacklist - Can put this as part of the app?
    - [ ] Threshold Tuning?
    - [ ] Airflow Automation
        - Can this be done without having to always turn on the VM and the specific time?
    - [ ] Add Neo4J Database
    - [ ] Docker and Docker Compose
    (?) 
    - [] CI/CD Pipeline - NER and Sentiment Scoring
        - More labelling of data?
    """
    
)
