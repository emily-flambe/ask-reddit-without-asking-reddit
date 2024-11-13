import React, { useState } from "react";

function RedditForm() {
    const [query, setQuery] = useState("");
    const [summary, setSummary] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`http://localhost:5000/ask_reddit`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ q: query }),
            });

            if (response.ok) {
                const data = await response.json();
                setSummary(data.summary);
            } else {
                setError("Failed to retrieve summary. Please try again.");
            }
        } catch (err) {
            setError("An error occurred. Please check your connection and try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Reddit Summarizer</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Enter your query:
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        required
                    />
                </label>
                <button type="submit" disabled={loading}>
                    {loading ? "Loading..." : "Submit"}
                </button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {summary && (
                <div>
                    <h2>Summary:</h2>
                    <p>{summary}</p>
                </div>
            )}
        </div>
    );
}

export default RedditForm;
