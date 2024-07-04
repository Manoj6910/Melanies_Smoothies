# Import python packages
import streamlit as st
import requests
import pandas
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
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
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_choosen + ' Nutrition Information')
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        fv_dv = st.dataframe(data = fruityvice_response.json(),use_container_width=True)
        
    
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
