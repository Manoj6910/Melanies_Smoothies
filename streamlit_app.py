# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your custom smoothie""" 
        )
##option = st.selectbox(
 ##   "What is your favourite Fruit?",
##   ("Banana", "Strawberries", "Peachs"))

##st.write("You selected:", option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',my_dataframe
    ,max_selections = 5
)

if ingredients_list: 
    ##st.write(ingredients_list)
    ##st.text(ingredients_list)
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string +=fruit_choosen + ' '
    
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:

    #if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'' '+ name_on_order ,icon="✅");

#New session to display fruitywise information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_dv = st.dataframe(data = fruityvice_response.json(),use_container_width=True)
