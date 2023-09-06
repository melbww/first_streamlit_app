import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError




streamlit.title("My Parent New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =  streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
print(fruits_selected)
print(type(fruits_selected))
streamlit.text(fruits_selected)
streamlit.text(type(fruits_selected))

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())


streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please enter a fruit')
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

# streamlit.stop()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchone()
# streamlit.header("list of fruits from Snowflake")
# streamlit.text(my_data_row)
# my_data_rows = my_cur.fetchall()
# streamlit.dataframe(my_data_rows)

# streamlit.text('What fruit would you like to add to the list?')
# fruit_to_add = streamlit.text_input('What fruit would you like to add to the list?','jackfruit')
# streamlit.write('Thanks for adding ', fruit_to_add)

def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        my_data_rows = my_cur.fetchall()
        return my_data_rows
    
if streamlit.button('Show me the fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(my_cnx)
    streamlit.dataframe(my_data_rows)
streamlit.text('TESTING')    