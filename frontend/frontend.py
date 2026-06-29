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
st.markdown("Powered by PostgreSQL, pgvector, and FastAPI")
st.divider()

user_query = st.selectbox(
    "Choose a movie to get recommendations for:",
    options=available_titles,
    index=None,
    placeholder="Select a movie..."
)

if st.button("Get Recommendations"):
    if user_query:
        with st.spinner(f"Calculating recommendations for {user_query}..."):
            try:
                response = requests.post(f"{API_BASE_URL}/recommend/{user_query}", json={"query": user_query})

                if response.status_code == 200:
                    results = response.json()

                    st.success("Recommendations:")

                    # Set up displays in 3 columns:
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("🎬 Movies 🎬")
                        for movie in results.get("movies", []):
                            st.write(f"- {movie['title']}")

                    with col2:
                        st.subheader("📚 Books 📚")
                        for book in results.get("books", []):
                            st.write(f"- {book['title']}")

                    with col3:
                        st.subheader("🎮 Games 🎮")
                        for game in results.get("games", []):
                            st.write(f"- {game['title']}")

                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to backend. Check Azure and DB connections: {e}")
    else:
        st.error("Invalid title entered")
