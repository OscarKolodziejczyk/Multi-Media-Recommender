import {useState, useEffect} from 'react';
import './App.css';


// Create interfaces for our API responses:

interface MediaItem {
    Title: string;
    Description: string;
    DataType: string;
    "Match Score": number;
    }

interface RecommendationResponse {
    searched_title: string;
    movies: MediaItem[];
    books: MediaItem[];
    games: MediaItem[];
    }


function App() {
    const API_BASE_URL = "https://multi-media-recommender-app.nicecoast-7eaef372.canadacentral.azurecontainerapps.io";

    // Set state variables

    const [availableTitles, setAvailableTitles] = useState<string[]>([]);
    const [selectedTitle, setSelectedTitle] = useState<string>("");
    const [recommendations, setRecommendations] = useState<MediaItem[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");

    // Fetch all titles:
    useEffect(() => {
        const fetchTitles = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/titles`);

                if (!response.ok) throw new Error("Failed to fetch titles");

                const data = await response.json();
                setAvailableTitles(data.titles); // TODO: could have to be changed b/c data is expecting a certain response, idk what it is for sure
                } catch (err) {
                    console.error("Error fetching titles:", err);
                    setError("Could not load titles from backend.");
                    }
            };

            fetchTitles();
        }, []); // Empty array here ensures this only runs once (why?)

    // Actual search for recommednations:

    const handleSearch = async () => {
        if (!selectedTitle) {
            alert("Please select a title first!");
            return;
            }
        try {

        setIsLoading(true);
        setError("");
        setRecommendations([]);

        // Clean titles: get rid of media type at the end
        let cleanTitle = selectedTitle.slice(0, -7);
        if (cleanTitle.endsWith(" ")) {
            cleanTitle = cleanTitle.slice(0, -1);
        }

        const response = await fetch(`${API_BASE_URL}/recommend/${encodeURIComponent(cleanTitle)}`);
        if (!response.ok) throw new Error("Failed to fetch recommendations");

        const data: RecommendationResponse = await response.json();

        const combinedResults = [...data.movies, ...data.books, ...data.games];
        setRecommendations(combinedResults);

    } catch (err) {
        console.error("Search error:", err);
        setError("Failed to fetch recommendations. Check network console");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1>Cross-Media Semantic Engine</h1>
                <p>Find visually and thematically similar Movies, Books, and Games.</p>
            </header>

            {/* Buttons and Interactive Tools*/}
            <div className="controls">
                <select
                    className="title-dropdown"
                    value={selectedTitle}
                    onChange={(e) => setSelectedTitle(e.target.value)}
                >
                    <option value="">-- Select a Movie --</option>
                    {availableTitles.map((title, index) => (
                        <option key={index} value={title}>{title}</option>
                        ))}
                </select>

                <button
                    className="search-button"
                    onClick={handleSearch}
                    disabled={isLoading || availableTitles.length == 0}
                >
                    {isLoading ? "Searching..." : "Get Recommendations"}
                </button>
            </div>

            {/* Error Message Display*/}
            {error && <div style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>{error}</div>}

            {/* Resulting Recommendations Area */}
            <div className="results-grid">
                {recommendations.map((rec, index) => (
                    <div key={index} className="card">
                        <span className={'badge ${rec.DataType.toLowerCase()}'}>{rec.DataType}</span>
                        <span style ={{ float: 'right', fontSize: '0.8rem', color: '#666', fontWeight: 'bold'}}>
                            Score: {rec['Match Score']}
                        </span>
                        <h3>{rec.title}</h3>
                        <p>{rec.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
    }

export default App
