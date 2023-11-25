import pickle
from pathlib import Path
from streamlit.source_util import (page_icon_and_name, calc_md5, get_pages,_on_pages_changed)

import streamlit as st
import streamlit_authenticator as stauth
from dependencies import sign_up, fetch_users



st.set_page_config(page_title="Book Recommendation System", page_icon="📔", layout="centered", initial_sidebar_state="auto",menu_items=None)

def delete_page(main_script_path_str, page_name):

    current_pages = get_pages(main_script_path_str)

    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass
    _on_pages_changed.send()

def add_page(main_script_path_str, page_name):
    
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()


delete_page("HomePage", "Simple_Recommender")
delete_page("HomePage", "Content_Based_Filtering")
delete_page("HomePage", "Review_Based_Filtering")



try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='hehe', key='abcdefgh', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:

                add_page("HomePage", "Simple Recommender")
                add_page("HomePage", "Content Based Filtering")
                add_page("HomePage", "Review Based Filtering")


                st.write('# Book Recommendation System')
                st.write("""
                            Welcome to our book recommendation system!
                            In our website, there are three models available. Let us provide you a bit of insight into them.
                            1. Simple Recommender:
                            This model offers generalized recommendations to every user based on popularity and average rating of 
                            the book. This model does not provide user-specific recommendations.
                            
                            2.  Content Based Filtering:
                            To personalise our recommendations, you need to pick your favorite book. The model will suggest books that 
                            are most similar to a particular book that a user liked.
                            
                            3. Content and Review Based Filtering:
                            The mechanism to remove books with low ratings has been added on top of the content based filtering.
                            This model will return books that are similar to your input, are popular and have high ratings.

                            """)
                st.sidebar.title(f"Welcome {username}")


                Authenticator.logout("Logout","sidebar")
    

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except Exception as e:
    st.write({e})
    st.success('Refresh Page')