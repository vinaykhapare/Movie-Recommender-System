import pickle
import streamlit as st
import requests

@st.cache_resource
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url).json()
        poster_path = response.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return None
    except Exception:
        return None

def recommend(movie, movies, similarity):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommendations = [
            (movies.iloc[i[0]].title, movies.iloc[i[0]].movie_id)
            for i in distances[1:6]
        ]
        return recommendations
    except Exception:
        st.error("An error occurred while fetching recommendations.")
        return []

def display_recommendations(recommendations):
    cols = st.columns(len(recommendations))
    for col, (movie_name, movie_id) in zip(cols, recommendations):
        with col:
            st.text(movie_name)
            poster_url = fetch_poster(movie_id)
            if poster_url:
                st.image(poster_url)
            else:
                st.warning("Poster not available.")

st.header('🎥 Movie Recommender System')

try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Ensure 'movie_list.pkl' and 'similarity.pkl' are present.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendations'):
    recommendations = recommend(selected_movie, movies, similarity)
    if recommendations:
        display_recommendations(recommendations)
    else:
        st.error("No recommendations available for this movie.")
