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

def content_recommendation(books, title, n=5):
    cosine_sim, indices = content(books)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n + 1]
    book_indices = [i[0] for i in sim_scores]
    return books[['book_id', 'title', 'authors', 'average_rating', 'ratings_count']].iloc[book_indices]

def main():
    books = read_book_data().copy()

    # Call the content function
    cosine, index = content(books)

    # User input
    selected_book_num = st.selectbox('Number of books', options=[5, 10, 15, 20, 25])

    options = np.concatenate(([''], books["title"].unique()))
    book_title = st.selectbox('Pick your favorite book', options, 0)

    if st.button('Recommend'):
        if book_title == '':
            st.write('Please pick a book or use the Simple Recommender.')
            return
        try:
            recs = content_recommendation(books=books, title=book_title, n=selected_book_num)
            st.write(recs)
        except Exception as e:
           st.error(f'Oops! An error occurred: {str(e)}')


if __name__ == '__main__':
        main()
