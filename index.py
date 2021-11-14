import streamlit as st
import user
import restaurant
import logingHelper

def onUserClick():
    user.onUserClick()

def onRestaurantClick():
    restaurant.onRestaurantClick()

def createLayout():
    user_label = 'I am a User'
    restaurant_label = 'I am a Restaurateur'
    user_key = 'user'
    restaurant_key = 'restaurant'
    user_on_click = 'onUserClick'
    res_on_click = 'onRestaurantClick'
    logingHelper.debug('Creating initial layout')
    st.title('Restaurant Recomender System')
    st.button(user_label, key=user_key,on_click=onUserClick)
    st.button(restaurant_label, key=restaurant_key, on_click=onRestaurantClick)