import {useState} from 'react';
import './App.css';


// Create a Recommendation blueprint
interface Recommendation {
    id: number;
    title:string;
    category: 'Movie' | 'Book' | 'Game';
    description: string;
    }


function App() {

    // First we set state variables

    const [availableTitles, setAvailableTitles] = useState<string[]>(["The Matrix", "Inception", "Interstellar", "Dune"]);

    const [selectedTitle, setSelectedTitle] = useState<string>("");
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleSearch = () => {
        if (!selectedTitle) {
            alert("Please select a title first!");
            return;
            }


        setIsLoading(true);

        setTimeout(() => {
            setRecommendations([
                { id: 1, title: "Neuromancer", category: "Book", description: "A classic cyberpunk novel." },
                { id: 2, title: "Cyberpunk 2077", category: "Game", description: "An open-world RPG." },
                { id: 3, title: "Blade Runner", category: "Movie", description: "A neo-noir sci-fi film." }
            ]);
            setIsLoading(false);
            }, 1000);
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
                    disabled={isLoading}
                >
                    {isLoading ? "Searching..." : "Get Recommendations"}
                </button>
            </div>

            {/* Resulting Recommendations Area */}
            <div className="results-grid">
                {recommendations.map((rec) => (
                    <div key={rec.id} className="card">
                        <span className={'badge ${rec.category.toLowerCase()}'}>{rec.category}</span>
                        <h3>{rec.title}</h3>
                        <p>{rec.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
    }

export default App
