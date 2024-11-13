import React, { useState } from "react";
import axios from "axios";

function RedditForm() {
    const [query, setQuery] = useState("");
    const [summary, setSummary] = useState("");
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await axios.post("http://127.0.0.1:5000/ask_reddit", {
                q: query,
            });

            if (response.status === 200) {
                setSummary(response.data.summary);
            }
        } catch (err) {
            setError("Failed to fetch data from the backend.");
        }
    };

    return (
        <div style={{ maxWidth: "500px", margin: "0 auto", padding: "20px" }}>
            <h1>Reddit Summarizer</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="input-field"
                />
                <button type="submit" className="submit-button">
                    Submit
                </button>
            </form>
            {error && <p className="error-message">{error}</p>}
            {summary && (
                <div className="summary-box">
                    <h2>Summary:</h2>
                    <p>{summary}</p>
                </div>
            )}
        </div>
    );
}

export default RedditForm;
