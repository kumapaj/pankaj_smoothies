# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie ! :cup_with_straw:")
st.write(
    """ Chose the fruits which you want in your smoothie !
    """
)



name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be : ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect("Choose up to 5 ingredients :", my_dataframe,max_selections=5)

if ingredients_list :
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + " "

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! ,{name_on_order} !", icon="✅")
