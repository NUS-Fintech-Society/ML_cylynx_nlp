import streamlit as st
from db.getEntities import getValidEntityData
import pandas as pd
import plotly.express as px
# import seaborn as sns

from app import ent_page,article_page,graph_page
pages = {
    "Entity Visualisation": ent_page,
    "Article Visualisation": article_page,
    "Graph Visualisation": graph_page

}

#Navigation
page_selections = list(pages.keys())
choice = st.sidebar.radio("App Page: ",pages)
page = pages[choice]
page.app()

