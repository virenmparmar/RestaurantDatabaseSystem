
import streamlit as st
import logingHelper
from configparser import ConfigParser
from index import createLayout


def getConfig(filename="database.ini", section="postgresql"):
    logingHelper.debug('Loading databse configurations')
    parser =  ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}



if __name__ == "__main__":
    createLayout()


