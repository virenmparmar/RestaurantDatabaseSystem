import streamlit as st
from configparser import ConfigParser
from loghelp import initLogging
logger = initLogging('root')


@st.cache
def getConfig(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

def query_db(sql:str):
    logger.debug('Inside Query DB. Executing ', sql)
    db_info = getConfig()
    #conn = psycopg2.connect(**db_info)