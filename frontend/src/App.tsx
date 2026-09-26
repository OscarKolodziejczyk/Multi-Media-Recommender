import { useState, useEffect, useRef } from 'react';
import './App.css';

// API response shapes

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

interface ColumnConfig {
  key: 'movies' | 'books' | 'games';
  label: string;
  icon: string;
  accentVar: string;
  items: MediaItem[];
}

function App() {
  const API_BASE_URL = "https://multi-media-recommender-app.nicecoast-7eaef372.canadacentral.azurecontainerapps.io";

  // State

  const [availableTitles, setAvailableTitles] = useState<string[]>([]);
  const [selectedTitle, setSelectedTitle] = useState<string>("");
  const [movies, setMovies] = useState<MediaItem[]>([]);
  const [books, setBooks] = useState<MediaItem[]>([]);
  const [games, setGames] = useState<MediaItem[]>([]);
  const [hasSearched, setHasSearched] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
  const [query, setQuery] = useState<string>("");
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close the dropdown on outside click

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fetch all available titles once on mount

  useEffect(() => {
    const fetchTitles = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/titles`);
        if (!response.ok) throw new Error("Failed to fetch titles");

        const data = await response.json();
        setAvailableTitles(data.titles);
      } catch (err) {
        console.error("Error fetching titles:", err);
        setError("Could not load titles from backend.");
      }
    };

    fetchTitles();
  }, []);

  // Search for recommendations

  const handleSearch = async () => {
    if (!selectedTitle) {
      alert("Please select a title first!");
      return;
    }

    try {
      setIsLoading(true);
      setError("");

      // Clean title: strip the trailing " (DataType)" suffix
      let cleanTitle = selectedTitle.slice(0, -7);
      if (cleanTitle.endsWith(" ")) {
        cleanTitle = cleanTitle.slice(0, -1);
      }

      const response = await fetch(`${API_BASE_URL}/recommend/${encodeURIComponent(cleanTitle)}`);
      if (!response.ok) throw new Error("Failed to fetch recommendations");

      const data: RecommendationResponse = await response.json();

      setMovies(data.movies);
      setBooks(data.books);
      setGames(data.games);
      setHasSearched(true);
    } catch (err) {
      console.error("Search error:", err);
      setError("Failed to fetch recommendations. Check network console.");
      setHasSearched(false);
    } finally {
      setIsLoading(false);
    }
  };

  const columns: ColumnConfig[] = [
    { key: 'movies', label: 'Movies', icon: '🎬', accentVar: 'var(--movies)', items: movies },
    { key: 'books', label: 'Books', icon: '📚', accentVar: 'var(--books)', items: books },
    { key: 'games', label: 'Games', icon: '🎮', accentVar: 'var(--games)', items: games },
  ];

  const filteredTitles = query.trim() === ""
    ? availableTitles
    : availableTitles.filter((title) => title.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="app-container">
      <header className="header">
        <h1>Cross-Media Recommendation Engine</h1>
        <div className="accent-strip" aria-hidden="true">
          <span style={{ background: 'var(--movies)' }} />
          <span style={{ background: 'var(--books)' }} />
          <span style={{ background: 'var(--games)' }} />
        </div>
        <p className="header-meta">
          <a href="https://github.com/OscarKolodziejczyk/Multi-Media-Recommender" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <span className="dot">·</span>
          Powered by Azure, Neon (PostgreSQL), Docker, React, &amp; FastAPI
        </p>
        <p className="byline">By Oscar Kolodziejczyk</p>
      </header>

      <div className="controls">
        <div className="dropdown" ref={dropdownRef}>
          <input
            type="text"
            className="dropdown-trigger"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedTitle("");
              setIsDropdownOpen(true);
            }}
            onFocus={() => setIsDropdownOpen(true)}
            placeholder="Search titles…"
            role="combobox"
            aria-expanded={isDropdownOpen}
            aria-haspopup="listbox"
            aria-controls="title-listbox"
            aria-autocomplete="list"
          />

          {isDropdownOpen && (
            <ul className="dropdown-list" role="listbox" id="title-listbox">
              {filteredTitles.length === 0 ? (
                <li className="dropdown-empty">No matching titles</li>
              ) : (
                filteredTitles.map((title, index) => (
                  <li
                    key={index}
                    role="option"
                    aria-selected={title === selectedTitle}
                    className={`dropdown-option${title === selectedTitle ? ' selected' : ''}`}
                    onClick={() => {
                      setSelectedTitle(title);
                      setQuery(title);
                      setIsDropdownOpen(false);
                    }}
                  >
                    {title}
                  </li>
                ))
              )}
            </ul>
          )}
        </div>

        <button
          className="search-button"
          onClick={handleSearch}
          disabled={isLoading || availableTitles.length === 0}
        >
          {isLoading ? "Searching…" : "Get Recommendations"}
        </button>
      </div>

      {error && <p className="error-message" role="alert">{error}</p>}

      {hasSearched && (
        <div className="columns-grid">
          {columns.map((column) => (
            <section className="column" key={column.key}>
              <h2 className="column-header" style={{ borderColor: column.accentVar }}>
                <span className="column-icon" aria-hidden="true">{column.icon}</span>
                {column.label}
                <span className="column-icon" aria-hidden="true">{column.icon}</span>
              </h2>

              {column.items.length === 0 ? (
                <p className="empty-state">No matches found.</p>
              ) : (
                <ul className="card-list">
                  {column.items.map((item, index) => (
                    <li className="card" key={index}>
                      <p className="card-title">{item.Title}</p>
                      <details className="card-details">
                        <summary>View description</summary>
                        <p className="card-description">{item.Description}</p>
                      </details>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
