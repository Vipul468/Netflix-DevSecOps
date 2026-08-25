const API_BASE = "http://127.0.0.1:8000";


// ===============================
// API HELPER
// ===============================

async function apiRequest(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
}


// ===============================
// MOVIES
// ===============================

async function loadMovies() {
    const container = document.getElementById("movieContainer");

    if (!container) {
        return;
    }

    container.innerHTML = `<p class="loading">Loading movies...</p>`;

    try {
        const data = await apiRequest(`${API_BASE}/api/movies`);

        displayMovies(data.movies || []);

    } catch (error) {
        console.error("Movies API Error:", error);

        container.innerHTML = `
            <p class="error-message">
                Unable to load movies from API.
            </p>
        `;
    }
}


// ===============================
// DISPLAY MOVIES
// ===============================

function displayMovies(movies) {
    const container = document.getElementById("movieContainer");

    if (!container) {
        return;
    }

    if (!movies || movies.length === 0) {
        container.innerHTML = `
            <p class="empty-message">
                No movies found.
            </p>
        `;
        return;
    }

    container.innerHTML = movies.map(movie => {

        const poster = movie.poster
            ? movie.poster
            : "https://via.placeholder.com/300x450?text=No+Poster";

        const rating = movie.rating !== undefined
            ? Number(movie.rating).toFixed(1)
            : "N/A";

        return `
            <div class="movie-card" onclick="openMovie(${movie.id})">

                <img
                    class="movie-poster"
                    src="${poster}"
                    alt="${escapeHtml(movie.title)}"
                    loading="lazy"
                    onerror="this.src='https://via.placeholder.com/300x450?text=No+Poster'"
                >

                <div class="movie-info">

                    <h3>${escapeHtml(movie.title)}</h3>

                    <p class="movie-meta">
                        ${escapeHtml(movie.category || "Movie")}
                        •
                        ${movie.year || "N/A"}
                    </p>

                    <p class="movie-genre">
                        ${escapeHtml(movie.genre || "Unknown")}
                    </p>

                    <p class="movie-rating">
                        ⭐ ${rating}
                    </p>

                </div>

            </div>
        `;

    }).join("");
}


// ===============================
// SERIES
// ===============================

async function loadSeries() {

    const container = document.getElementById("seriesContainer");

    if (!container) {
        console.error("seriesContainer not found in HTML");
        return;
    }

    container.innerHTML = `
        <p class="loading">
            Loading series...
        </p>
    `;

    try {

        const data = await apiRequest(
            `${API_BASE}/api/series`
        );

        console.log("Series API:", data);

        displaySeries(data.series || []);

    } catch (error) {

        console.error("Series API Error:", error);

        container.innerHTML = `
            <p class="error-message">
                Unable to load series from API.
            </p>
        `;
    }
}


// ===============================
// DISPLAY SERIES
// ===============================

function displaySeries(series) {

    const container = document.getElementById("seriesContainer");

    if (!container) {
        return;
    }

    if (!series || series.length === 0) {

        container.innerHTML = `
            <p class="empty-message">
                No series found.
            </p>
        `;

        return;
    }

    container.innerHTML = series.map(item => {

        const poster = item.poster
            ? item.poster
            : "https://via.placeholder.com/300x450?text=No+Poster";

        const rating = item.rating !== undefined
            ? Number(item.rating).toFixed(1)
            : "N/A";

        return `
            <div
                class="movie-card"
                onclick="openMovie(${item.id})"
            >

                <img
                    class="movie-poster"
                    src="${poster}"
                    alt="${escapeHtml(item.title)}"
                    loading="lazy"
                    onerror="this.src='https://via.placeholder.com/300x450?text=No+Poster'"
                >

                <div class="movie-info">

                    <h3>
                        ${escapeHtml(item.title)}
                    </h3>

                    <p class="movie-meta">
                        ${item.year || "N/A"}
                    </p>

                    <p class="movie-genre">
                        ${escapeHtml(item.genre || "Series")}
                    </p>

                    <p class="movie-rating">
                        ⭐ ${rating}
                    </p>

                </div>

            </div>
        `;

    }).join("");
}


// ===============================
// CATEGORIES
// ===============================

async function loadCategories() {

    const container =
        document.getElementById("categoryContainer");

    if (!container) {
        return;
    }

    container.innerHTML = `
        <p class="loading">
            Loading categories...
        </p>
    `;

    try {

        const data = await apiRequest(
            `${API_BASE}/api/categories`
        );

        displayCategories(data.categories || []);

    } catch (error) {

        console.error("Categories API Error:", error);

        container.innerHTML = `
            <p class="error-message">
                Unable to load categories.
            </p>
        `;
    }
}


// ===============================
// DISPLAY CATEGORIES
// ===============================

function displayCategories(categories) {

    const container =
        document.getElementById("categoryContainer");

    if (!container) {
        return;
    }

    if (!categories || categories.length === 0) {

        container.innerHTML = `
            <p class="empty-message">
                No categories found.
            </p>
        `;

        return;
    }

    container.innerHTML = categories.map(category => {

        return `
            <button
                class="category-btn"
                onclick="filterCategory('${escapeHtml(category)}')"
            >
                ${escapeHtml(category)}
            </button>
        `;

    }).join("");
}


// ===============================
// SEARCH
// ===============================

async function searchMovies() {

    const input =
        document.getElementById("searchInput");

    const container =
        document.getElementById("movieContainer");

    if (!input || !container) {
        return;
    }

    const query = input.value.trim();

    if (!query) {

        loadMovies();

        return;
    }

    container.innerHTML = `
        <p class="loading">
            Searching for "${escapeHtml(query)}"...
        </p>
    `;

    try {

        const data = await apiRequest(
            `${API_BASE}/api/search?q=${encodeURIComponent(query)}`
        );

        displayMovies(data.results || []);

    } catch (error) {

        console.error("Search API Error:", error);

        container.innerHTML = `
            <p class="error-message">
                Search failed.
            </p>
        `;
    }
}


// ===============================
// CATEGORY FILTER
// ===============================

async function filterCategory(category) {

    const container =
        document.getElementById("movieContainer");

    if (!container) {
        return;
    }

    container.innerHTML = `
        <p class="loading">
            Loading ${escapeHtml(category)}...
        </p>
    `;

    try {

        const data = await apiRequest(
            `${API_BASE}/api/movies`
        );

        const filtered = (data.movies || []).filter(movie => {

            return (
                movie.category &&
                movie.category.toLowerCase() ===
                category.toLowerCase()
            )
            ||
            (
                movie.genre &&
                movie.genre.toLowerCase() ===
                category.toLowerCase()
            );

        });

        displayMovies(filtered);

    } catch (error) {

        console.error("Category Error:", error);

        container.innerHTML = `
            <p class="error-message">
                Unable to filter movies.
            </p>
        `;
    }
}


// ===============================
// OPEN MOVIE
// ===============================

async function openMovie(movieId) {

    try {

        const movie = await apiRequest(
            `${API_BASE}/api/movies/${movieId}`
        );

        showMovieModal(movie);

    } catch (error) {

        console.error("Movie Details Error:", error);

    }
}


// ===============================
// MOVIE MODAL
// ===============================

function showMovieModal(movie) {

    const poster = movie.poster
        ? movie.poster
        : "https://via.placeholder.com/300x450?text=No+Poster";

    const rating = movie.rating !== undefined
        ? Number(movie.rating).toFixed(1)
        : "N/A";

    const modal = document.createElement("div");

    modal.className = "movie-modal";

    modal.innerHTML = `

        <div class="modal-content">

            <button
                class="close-modal"
                onclick="this.closest('.movie-modal').remove()"
            >
                ×
            </button>

            <div class="modal-body">

                <img
                    class="modal-poster"
                    src="${poster}"
                    alt="${escapeHtml(movie.title)}"
                    onerror="this.src='https://via.placeholder.com/300x450?text=No+Poster'"
                >

                <div class="modal-info">

                    <h2>
                        ${escapeHtml(movie.title)}
                    </h2>

                    <p>
                        <strong>Category:</strong>
                        ${escapeHtml(movie.category || "N/A")}
                    </p>

                    <p>
                        <strong>Genre:</strong>
                        ${escapeHtml(movie.genre || "N/A")}
                    </p>

                    <p>
                        <strong>Year:</strong>
                        ${movie.year || "N/A"}
                    </p>

                    <p>
                        <strong>Rating:</strong>
                        ⭐ ${rating}
                    </p>

                    <p class="overview">
                        ${escapeHtml(
                            movie.overview ||
                            "No description available."
                        )}
                    </p>

                </div>

            </div>

        </div>
    `;

    document.body.appendChild(modal);

    modal.addEventListener("click", event => {

        if (event.target === modal) {
            modal.remove();
        }

    });
}


// ===============================
// ESCAPE HTML
// ===============================

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ===============================
// SEARCH ENTER KEY
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
        document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {
                    searchMovies();
                }

            }
        );

    }

    // Initial API calls

    loadMovies();

    loadCategories();

    loadSeries();

});