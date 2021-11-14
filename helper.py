import streamlit as st
from configparser import ConfigParser
import logingHelper


@st.cache
def getConfig(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

def query_db(sql:str):
    logingHelper.debug('Inside Query DB. Executing '+ sql)
    db_info = getConfig()
    #conn = psycopg2.connect(**db_info)