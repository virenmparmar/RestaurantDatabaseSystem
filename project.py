from os import error
import streamlit as st
import datetime
import configparser
import logging
import re

from streamlit.type_util import OptionSequence
#import psycopg2

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'  


@st.cache
def getConfig(section):
    return {k: v for k, v in section}

config = configparser.ConfigParser()
config.read('database.ini')
databaseConfig = getConfig(config.items('postgresql'))
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    logging.basicConfig(filename=config['logging']['path']+'logs.txt',level=config['logging']['level'], force=True, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()



def checkEmail(email):
    if(email is None or email==''):
        st.error('Email cannot be blank')
    if(email):
        if(not re.search(regex,email)):
            st.error('Invalid email id')

@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = getConfig()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

def insertUser(email, name, mobileNumber, dateOfBirth):
    
    checkEmail(email)

    if(dateOfBirth>datetime.date.today()):
        st.error('Date is invalid')
    return

def reserveTable():
    return  

def addAddress():
    return

def main():
    menu = ['New User' , 'Reserve a table', 'Add an address', 'Add a review','View All reviews','Search for restaurants']
    choice = st.sidebar.selectbox('Menu',menu)


    if choice == 'New User':
        email = st.text_input('Email ', max_chars=128)
        name = st.text_input('Name ', max_chars=128)
        mobileNumber = st.number_input('Mobile number', max_value=9999999999, min_value=1000000000)
        dateOfBirth = st.date_input('Date of Birth')
        if st.button('Submit'):
            insertUser(email, name, mobileNumber, dateOfBirth)
    elif choice == 'Reserve a table':
        email =  st.text_input('Email ', max_chars=128)
        restaurantName = st.text_input('Enter restaurant name: ')
        if restaurantName:
            try:
                temp=0
            except Exception as e:
                print(e)


        dateOfReservation = st.date_input('When: ' , min_value=datetime.date.today(), value=datetime.date.today())
        timeOfReservation = st.time_input('What time: ')
        if st.button('Submit'):
            reserveTable()
    
    elif choice == 'Add an address':
        userOrRestaurant = st.selectbox('I am a ', options=['User', 'Restaurant'])
        if userOrRestaurant == 'User':
            email = st.text_input('Email: ', max_chars=128)
        elif userOrRestaurant == 'Restaurant':
            restaurantId = st.text_input('Restaurant Id: ', max_chars=32)
        addressLone = st.text_input('Line 1: ', max_chars=128)
        city = st.text_input('City: ', max_chars=64)
        state = st.text_input('State: ', max_chars=64)
        zipcode  = st.number_input('Zip Code: ', min_value=10000, max_value=99999, value=99999)
        if st.button('Submit'):
            addAddress()
    
    elif choice == 'Add a review':
        email = st.text_input('Email: ', max_chars=128)
        restaurantId = st.text_input('Restaurant Id: ', max_chars=32)
        ambience = st.slider('Ambience: ',0,5) 
        foodQuality = st.slider('Food Quality: ',0,5) 
        service = st.slider('Service: ',0,5) 
        overallExperience = st.slider('Overall Experience',0,5) 
        description = st.text_input('Review', max_chars=256)


if __name__ == '__main__':
    main()