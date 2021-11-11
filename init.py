
import streamlit as st
from loghelp import initLogging
from configparser import ConfigParser
from index import createLayout

log = initLogging('root')

def getConfig(filename="database.ini", section="postgresql"):
    log.debug('Loading databse configurations')
    parser =  ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}



if __name__ == "__main__":
    createLayout()


