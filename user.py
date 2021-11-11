import streamlit as st

logger

def newUser():
    email = st.text_input("Email", max_chars=128)
    mobileNumber = st.number_input("Mobile Number:", min_value=1000000000, max_value=999999999)
    name = st.text_input("Name", max_chars=128)
    dob = st.date_input("D.O.B.", min_value="")


def onUserClick():
    new_user = 'New User ? Click Me!'
    email = st.text_input('Please enter your email id')
    user = st.button(new_user)
    log.debug("Email entered is " + email)
    if(email):
        temp=0
    if(user):
        newUser()