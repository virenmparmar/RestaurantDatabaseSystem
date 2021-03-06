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
def get_config(filename="/home/vmp2018/project_demo/database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


def checkEmail(email):
    if(email is None or email==''):
        st.error('Email cannot be blank')
    if(email):
        if(not re.search(regex,email)):
            st.error('Invalid email id')


def query_db(sql: str):
    print(sql)
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


def insert_query_db(sql: str):
    print(sql)
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
    sql_insert_user = 'insert into users (email, name, phone, dob)values ( \'' + email.strip() + '\' , \'' + name.strip() + '\' , ' + str(mobileNumber) + ' , \'' + str(dateOfBirth) + '\' );'
    try:
        df = insert_query_db(sql_insert_user)
        st.write('User Created!')
    except Exception as e:
        print(e)
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return


def reserveTable(email, business_id, dateOfReservation, timeOfReservation, tableNo):
    sql_insert_reservation = f'insert into reservations (date_reserved, time_reserved, Table_no, User_email, Restaurant_id) values (\'{str(dateOfReservation)}\' , \'{str(timeOfReservation)}\' , {str(tableNo)}, \'{email.strip()}\', \'{business_id.strip()}\' );' 
    try:
        df = insert_query_db(sql_insert_reservation)
        st.write('Reservation Successfull!')
    except Exception as e:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return  

def addAddress(userOrRestaurant, email, restaurantId, addressLine, city, state, zipcode):
    sql_insert_address = f'insert into address (address_line, city, state, zipcode) values (\'{addressLine.strip()}\', \'{city.strip()}\', \'{state.strip()}\', {str(zipcode)} ); \n'
    try:
        if userOrRestaurant  == 'User':
            sql_insert_address  = sql_insert_address + f'insert into users_address (U_email, Address_line, City ) values ( \'{email.strip()}\', \'{addressLine.strip()}\', \'{city.strip()}\');'
        if userOrRestaurant == 'Restaurant':
            sql_insert_address = sql_insert_address  + f'insert into restaurant_address(Reataurant_id, Address_line, City ) values ( \'{restaurantId.strip()}\' , \'{addressLine.strip()}\' , \'{city.strip()}\');'
        df = insert_query_db(sql_insert_address)
        st.write('Address saved successfully!')
    except Exception as e:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
    return

def insertReview(email, business_id, ambience, foodQuality, service, overallExperience, description):
    sql_insert_review = f'insert into reviews (ambience, food_quality, service, overall_experience, description, user_email, restaurant_id) values ( {ambience}, {foodQuality}, {service}, {overallExperience}, \'{description}\', \'{email}\', \'{business_id.strip()}\');'
    df = insert_query_db(sql_insert_review)
    st.write('Review submitted')
    return

def findEmail(email):
    sql_search_query = 'select count(1) as found from users where email = \'' + email + '\';'
    isvalid = query_db(sql_search_query)['found'].loc[0]
    return isvalid

def countAddress(email):
    sql_count_address = f'Select count(*) as address from users_address where u_email = \'{email}\';'
    count = query_db(sql_count_address)['address'].loc[0]
    return count

def queryAddress(email):
    sql_find_address = f'select a.address_line as line, a.city as city, a.state as state, a.zipcode as zip from users_address ua, address a  where ua.u_email = \'{email}\' and ua.Address_line = a.address_line and ua.city = a.city;'
    return query_db(sql_find_address)

def countReviews(email):
    sql_count_reviews = f'select count(*) as reviews from reviews where User_email = \'{email}\';'
    count = query_db(sql_count_reviews)['reviews'].loc[0]
    return count

def findRestByZip(zipcode):
    sql_find_rest = f'select r.restuarant_name as Name, a.address_line AS Address, a.city as City, a.zipcode as Zipcode from restaurant r, restaurant_address ra, address a where a.zipcode = {zipcode} and r.Restaurant_id = ra.Reataurant_id and ra.Address_line = a.address_line and ra.city = a.city;'
    return query_db(sql_find_rest)

def findRestByCity(city):
    sql_find_rest = f'select r.restuarant_name, ra.address_line, ra.city from restaurant r, restaurant_address ra where ra.city = \'{city}\'and r.Restaurant_id = ra.Reataurant_id;'
    return query_db(sql_find_rest)

def getReviews(business_id):
    sql_find_reviews = f'select r.restuarant_name as Name, re.ambience as ambience, re.food_quality as FoodQuality, re.service as Service, re.overall_experience OverallExperience, re.description from reviews re,restaurant r  where re.restaurant_id = \'{business_id}\' and r.Restaurant_id = re.restaurant_id'
    return query_db(sql_find_reviews)

def getOperatingHours(business_id):
    sql_get_operating_hours = f'select day , Time  from operating_hours where Restaurant_id  = \'{business_id.strip()}\''
    return query_db(sql_get_operating_hours)

def getCoupons(email):
    sql_get_coupons = f'select c.Coupon_id as Coupon, c.Expiry_date  as expiry, c.Discount_amt as Discount from coupons c, user_coupons uc where uc.user_email = \'{email.strip()}\' and  uc.Coupon_id = c.Coupon_id;'
    return query_db(sql_get_coupons)


def main():
    menu = ['New User' , 'Reserve a table', 'Add an address', 'Add a review','View All reviews','User Profile', 'Search Restaurant', 'Operating hours', 'View Coupons', 'Analyse Data']
    choice = st.sidebar.selectbox('Menu',menu)
    isvalid = 1

    if choice == 'New User':
        email = ''
        email =  st.text_input('Email ', max_chars=128)
        if(email):
            isvalid = findEmail(email)
            if isvalid == 1 :
                st.error("User already registered")
        name = st.text_input('Name ', max_chars=128)
        mobileNumber = st.number_input('Mobile number', max_value=9999999999, min_value=1000000000)
        dateOfBirth = st.date_input('Date of Birth')
        if isvalid == 0:
            if st.button('Submit'):
                insertUser(email, name, mobileNumber, dateOfBirth)
            
    elif choice == 'Reserve a table':
        email_r = ''
        email_r =  st.text_input('Email ', max_chars=128)
        isvalid = 0
        if(email_r):
            isvalid = findEmail(email_r)
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
        email = ''
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
        email = ''
        isvalid = 0
        email =  st.text_input('Email ', max_chars=128)
        if(email):
            isvalid = findEmail(email)
            if isvalid == 0:
                st.write("User not found")
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
        ambience = st.slider('Ambience: ',0,5) 
        foodQuality = st.slider('Food Quality: ',0,5) 
        service = st.slider('Service: ',0,5) 
        overallExperience = st.slider('Overall Experience',0,5) 
        description = st.text_input('Review', max_chars=256)
        if isvalid == 1:
            submit = st.button('Submit')
            if submit:
                insertReview(email, business_id, ambience, foodQuality, service, overallExperience, description)
            
    elif choice == 'User Profile':
        email = ''
        email =  st.text_input('Email ', max_chars=128)
        isvalid = 0
        if(email):
            isvalid = findEmail(email)
            if isvalid == 0:
                st.error("User not found")
            
            st.write('You have ' + str(countAddress(email)) + ' address registered!')
            st.write('\n\n Address ')
            st.dataframe(queryAddress(email))

            st.write('You have posted ' + str(countReviews(email)) + ' reviews.')
    elif choice == 'Search Restaurant':
        searchAttribute = st.selectbox('Find Restaurant by ', ['Zip code', 'City', 'Reviews'])
        if searchAttribute:
            if searchAttribute == 'Zip code':
                zipcode  = st.number_input('Zip Code: ', min_value=10000, max_value=99999, value=99999)
                if zipcode:
                    st.write(findRestByZip(zipcode))
            elif searchAttribute == 'City':
                city_search = st.text_input('City: ', max_chars=64)
                if city_search:
                    try:
                        sql_find_city = f'select distinct(ra.city) as city from restaurant_address ra where lower(ra.city) like \'%{city_search.lower()}%\';'

                        cities = query_db(sql_find_city)

                        city =   st.selectbox("Choose a restaurant", cities['city'].tolist())
                        if city:
                            st.write(findRestByCity(city))
                    except Exception as e:
                        st.write(e)
                        st.write('Something went wrong.')
            elif searchAttribute == 'Reviews':
                priority = st.selectbox('What is your priority' , ['Ambience', 'Food quality','Service'])
                if priority:
                    if priority == 'Ambience':
                        sql_search_rest = f'select re.restuarant_name, ra.address_line, ra.city from reviews r, restaurant re, restaurant_address ra where (r.ambience >= r.food_quality or r.ambience >= r.service) and r.Restaurant_id = re.Restaurant_id and r.Restaurant_id = ra.Reataurant_id;' 
                    elif priority == 'Food quality':
                        sql_search_rest = f'select re.restuarant_name, ra.address_line, ra.city from reviews r, restaurant re, restaurant_address ra where (r.food_quality >= r.ambience or r.food_quality >= r.service) and r.Restaurant_id = re.Restaurant_id and r.Restaurant_id = ra.Reataurant_id;'
                    elif priority == 'Service':
                        sql_search_rest = f'select re.restuarant_name, ra.address_line, ra.city from reviews r, restaurant re, restaurant_address ra where (r.service >= r.ambience or r.service >= r.food_quality) and r.Restaurant_id = re.Restaurant_id and r.Restaurant_id = ra.Reataurant_id;'
                    st.write(query_db(sql_search_rest))
    elif choice == 'View All reviews':
        restaurantName = st.text_input('Enter restaurant name: ')
        restName =''
        business_id = None
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
        if business_id:
            st.dataframe(getReviews(business_id))
    elif choice =='Operating hours':
        restaurantName = st.text_input('Enter restaurant name: ')
        restName =''
        business_id = None
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
        if business_id:
            st.dataframe(getOperatingHours(business_id))
    elif choice =='View Coupons':
        email = ''
        isvalid = 0
        email =  st.text_input('Email ', max_chars=128)
        if(email):
            isvalid = findEmail(email)
            if isvalid == 0:
                st.write("User not found")
            else:
                st.dataframe(getCoupons(email))
    elif choice =='Analyse Data':
        restGroupBy = st.selectbox('Analyse by', ['','Rating', 'City'])
        if restGroupBy == 'Rating':
            sql_group_by_rating = f'select CEILING((ambience + food_quality + service + overall_experience)/4) as Rating, count(*) as count from reviews group by rating;'
            st.dataframe(query_db(sql_group_by_rating))
        elif restGroupBy == 'City':
            sql_group_by_city = f'select city, count(*) as count from restaurant_address group by city order by city;'
            st.dataframe(query_db(sql_group_by_city))



if __name__ == '__main__':
    main()
