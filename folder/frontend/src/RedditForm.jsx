import React, { useState } from "react";
import axios from "axios";

function RedditForm() {
    const [query, setQuery] = useState("");
    const [searchEntirePosts, setSearchEntirePosts] = React.useState(false);
    const [summary, setSummary] = useState("");
    const [error, setError] = useState(null);
    const [posts, setPosts] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await axios.post("http://127.0.0.1:5000/ask_reddit", {
                search_term: query,
                search_entire_posts: searchEntirePosts,
            });

            if (response.status === 200) {
                setSummary(response.data.summary);
                setPosts(response.data.posts);
            }
        } catch (err) {
            console.error(err);
            setError("Failed to fetch data from the backend.");
        }
    };

    const truncateText = (text, wordLimit) => {
        const words = text.split(' ');
        if (words.length > wordLimit) {
            return words.slice(0, wordLimit).join(' ') + '...';
        }
        return text;
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
                <label>
                    Search Entire Posts:
                    <input
                        type="checkbox"
                        checked={searchEntirePosts}
                        onChange={(e) => setSearchEntirePosts(e.target.checked)}
                    />
                </label>
                <button type="submit" className="submit-button">
                    SUBMIT.
                </button>
            </form>
            {error && <p className="error-message">{error}</p>}
            {summary && (
                <div className="summary-box">
                    <h2>Summary:</h2>
                    <p>{summary}</p>
                    <br />
                    <h3>Posts included in summary:</h3>
                    <br />
                    <div>
                        {posts.map((post, index) => (
                            <div key={index} className="mb-4">
                                <a
                                    href={post.url}
                                    className="text-blue-500 underline"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {post.title}
                                </a>
                                <p className="mt-2 text-gray-700">
                                    {truncateText(post.text, 50)}
                                </p>
                                <br />
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default RedditForm;
