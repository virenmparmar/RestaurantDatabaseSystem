from os import error
import streamlit as st
import psycopg2
import datetime
from configparser import ConfigParser
import logging
import re
import pandas as pd

from streamlit.type_util import OptionSequence
#import psycopg2

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'  


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


def checkEmail(email):
    if(email is None or email==''):
        st.error('Email cannot be blank')
    if(email):
        if(not re.search(regex,email)):
            st.error('Invalid email id')

@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

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

@st.cache
def insert_query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return

def insertUser(email, name, mobileNumber, dateOfBirth):
    
    checkEmail(email)

    if(dateOfBirth>datetime.date.today()):
        st.error('Date is invalid')
    sql_insert_user = 'insert into users values ( \'' + email + '\' , \'' + str(mobileNumber) + '\' , ' + name + ' , \'' + str(dateOfBirth) + '\' );'
    try:
        df = insert_query_db(sql_insert_user)
        st.write('User Created!')
    except Exception as e:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return


def reserveTable(email, business_id, dateOfReservation, timeOfReservation, tableNo):
    sql_insert_reservation = f'insert into reservations (date_reserved, time_reserved, Table_no, User_email, Restaurant_id) values (\'{str(dateOfReservation)}\' , \'{str(timeOfReservation)}\' , {str(tableNo)}, \'{email}\', \'{business_id}\' );' 
    try:
        df = insert_query_db(sql_insert_reservation)
        st.write('Reservation Successfull!')
    except Exception as e:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return  

def addAddress(userOrRestaurant, email, restaurantId, addressLine, city, state, zipcode):
    sql_insert_address = f'insert into address (address_line, city, state, zipcode) values (\'{addressLine}\', \'{city}\', \'{state}\', {str(zipcode)} ); \n'
    try:
        if userOrRestaurant  == 'User':
            sql_insert_address  = sql_insert_address + f'insert into users_address (U_email, Address_line, City ) values ( \'{email}\', \'{addressLine}\', \'{city}\');'
        if userOrRestaurant == 'Restaurant':
            sql_insert_address = sql_insert_address  + f'insert into restaurant_address(Reataurant_id, Address_line, City ) values ( \'{restaurantId}\' , \'{addressLine}\' , \'{city}\');'
        df = insert_query_db(sql_insert_address)
        st.write('Address saved successfully!')
    except Exception as e:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return

def findEmail(email):
    sql_search_query = 'select count(1) as found from users where email = \'' + email + '\';'
    isvalid = query_db(sql_search_query)['found'].loc[0]
    return isvalid

def main():
    menu = ['New User' , 'Reserve a table', 'Add an address', 'Add a review','View All reviews','Search for restaurants']
    choice = st.sidebar.selectbox('Menu',menu)
    isvalid = 0

    if choice == 'New User':
        email = st.text_input('Email ', max_chars=128)
        name = st.text_input('Name ', max_chars=128)
        mobileNumber = st.number_input('Mobile number', max_value=9999999999, min_value=1000000000)
        dateOfBirth = st.date_input('Date of Birth')
        if st.button('Submit'):
            insertUser(email, name, mobileNumber, dateOfBirth)
    elif choice == 'Reserve a table':
        email =  st.text_input('Email ', max_chars=128)
        if(email):
            isvalid = findEmail(email)
            if isvalid == 0:
                st.error("User not found")

        restaurantName = st.text_input('Enter restaurant name: ')
        restName =''
        if restaurantName:
            sql_find_rest = 'select Restaurant_id as id, restuarant_name as name from restaurant where lower(restuarant_name) like \'%' + restaurantName + '%\' ;'
            
            try:
                restaurants = query_db(sql_find_rest)

                restName =   st.selectbox("Choose a restaurant", restaurants['name'].tolist())
                if restName:
                    business_id = restaurants.loc[restaurants['name'] == restName, 'id'].iloc[0]
            except Exception as e:
                st.write(e)
                st.write('Something went wrong.')

        dateOfReservation = st.date_input('When: ' , min_value=datetime.date.today(), value=datetime.date.today())
        timeOfReservation = st.time_input('What time: ')
        tableNo = st.selectbox("Select a table number ", [1,2,3,4,5])
        if isvalid == 1:
            if st.button('Submit'):
                if restName == '':
                    st.error('You need to select a Restaurant')
                reserveTable(email, business_id, dateOfReservation, timeOfReservation, tableNo)
    
    elif choice == 'Add an address':
        addressLine = ''
        city = ''
        state = ''
        zipcode = 0
        restName =''
        business_id = ''
        userOrRestaurant = st.selectbox('I am a ', options=['User', 'Restaurant'])
        if userOrRestaurant == 'User':
            email =  st.text_input('Email ', max_chars=128)
            isvalid = 0
            if(email):
                isvalid = findEmail(email)
                if isvalid == 0:
                    st.error("User not found")
        elif userOrRestaurant == 'Restaurant':
            restaurantName = st.text_input('Restaurant Name: ', max_chars=32)
            if restaurantName:
                sql_find_rest = 'select Restaurant_id as id, restuarant_name as name from restaurant where lower(restuarant_name) like \'%' + restaurantName + '%\' ;'
                try:
                    restaurants = query_db(sql_find_rest)

                    restName =   st.selectbox("Choose a restaurant", restaurants['name'].tolist())
                    if restName:
                        business_id = restaurants.loc[restaurants['name'] == restName, 'id'].iloc[0]
                except Exception as e:
                    st.write(e)
                    st.write('Something went wrong.')
        addressLine = st.text_input('Line 1: ', max_chars=128)
        city = st.text_input('City: ', max_chars=64)
        state = st.text_input('State: ', max_chars=64)
        zipcode  = st.number_input('Zip Code: ', min_value=10000, max_value=99999, value=99999)
        if isvalid == 1:
            if st.button('Submit'):
                if addressLine == '':
                    st.write('Address line cannot be blank')
                if city == '':
                    st.write('City cannot be left blank')
                if state == '':
                    st.write('State cannot be blank')
                addAddress(userOrRestaurant, email, business_id, addressLine, city, state, zipcode)
    
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
