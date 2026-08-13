import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Multi Media Recommender", page_icon="🍿", layout="centered")

# Azure Container App URL
API_BASE_URL = "https://multi-media-recommender-app.nicecoast-7eaef372.canadacentral.azurecontainerapps.io"

# Fetch titles and CACHE them in memory:
@st.cache_data
def fetch_titles():
    try:
        response = requests.get(f"{API_BASE_URL}/titles")
        if response.status_code == 200:
            return response.json().get("titles", [])
        return []
    except Exception as e:
        st.error(f"Could not fetch media titles from backend: {e}")
        return []

available_titles = fetch_titles()

st.title("Cross Media Recommendation Engine")
st.markdown("[GitHub Link](https://github.com/OscarKolodziejczyk/Multi-Media-Recommender) | Powered by Azure, Neon (PostgreSQL), Docker, StreamLit, & FastAPI")
st.markdown("\- By Oscar Kolodziejczyk")
st.divider()

user_query = st.selectbox(
    "Choose a movie to get recommendations for:",
    options=available_titles,
    index=None,
    placeholder="Select a title..."
)

if st.button("Get Recommendations"):
    if user_query:
        # Have to strip the data type into our input...
        user_query = user_query[:-7]
        if user_query[-1] == " ":
            user_query = user_query[:-1]
        with st.spinner(f"Calculating recommendations for {user_query}..."):
            try:
                response = requests.get(f"{API_BASE_URL}/recommend/{user_query}", json={"query": user_query})

                if response.status_code == 200:
                    results = response.json()

                    st.success("Recommendations:")

                    # Set up displays in 3 columns:
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("🎬 Movies 🎬")
                        for movie in results.get("movies", []):
                            st.markdown(f"**{movie['Title']}**")
                            with st.expander(f"View Description"):
                                st.caption(movie['Description'])
                            st.write("---")

                    with col2:
                        st.subheader("📚 Books 📚")
                        for book in results.get("books", []):
                            st.markdown(f"**{book['Title']}**")
                            with st.expander(f"View Description"):
                                st.caption(book['Description'])
                            st.write("---")

                    with col3:
                        st.subheader("🎮 Games 🎮")
                        for game in results.get("games", []):
                            st.markdown(f"**{game['Title']}**")
                            with st.expander(f"View Description"):
                                st.caption(game['Description'])
                            st.write("---")

                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to backend. Check Azure and DB connections: {e}")
    else:
        st.error("Invalid title entered")
