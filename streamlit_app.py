# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


cnx=st.connection("snowflake")
name_on_order = st.text_input("Name on Smoothie:")
st.write("The nam on your Smoothie will be:",name_on_order )


#Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

#We can use the st.write() and st.text() methods to take a closer look at what is contained in our ingredients LIST. 
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    # Create the INGREDIENTS_STRING Variable 
    ingredients_string=''

    #To convert the LIST to a STRING we can add an FOR LOOP block
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '

    #st.write(ingredients_string)

    #Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()

    
    time_to_insert=st.button('Submit Order')

    #Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered!, {name_on_order}',icon="✅")
        
