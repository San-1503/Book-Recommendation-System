import numpy as np
import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

st.set_page_config(page_title="Book Recommendation System", page_icon="📔", layout="centered", initial_sidebar_state="auto", menu_items=None)

# data loading
@st.cache_data()
def read_book_data():
    return pd.read_csv('data/books_cleaned.csv')


@st.cache_data()
def content(books):
    books['content'] = (pd.Series(books[['authors', 'title', 'genres', 'description']]
                                    .fillna('')
                                    .values.tolist()
                                    ).str.join(' '))

    tf_content = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
    tfidf_matrix = tf_content.fit_transform(books['content'])
    cosine = linear_kernel(tfidf_matrix, tfidf_matrix)
    index = pd.Series(books.index, index=books['title'])

    return cosine, index

def simple_recommender(books, n=5):
    v = books['ratings_count']
    m = books['ratings_count'].quantile(0.95)
    R = books['average_rating']
    C = books['average_rating'].median()
    score = (v / (v + m) * R) + (m / (m + v) * C)
    books['score'] = score
    qualified = books.sort_values('score', ascending=False)
    return qualified[['book_id', 'title', 'authors', 'score']].head(n)

def main():
    books = read_book_data().copy()

    # Call the content function
    cosine, index = content(books)

    # User input
    selected_book_num = st.selectbox('Number of books', options=[5, 10, 15, 20, 25])

    if st.button('Recommend'):
        try:
            recs = simple_recommender(books=books, n=selected_book_num)
            st.write(recs)
        except:
            st.error('Oops! Something went wrong.')

if __name__ == '__main__':
    main()
