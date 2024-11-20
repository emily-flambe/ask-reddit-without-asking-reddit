import React, { useState } from "react";
import axios from "axios";

function RedditForm() {
    const [query, setQuery] = useState("");
    const [subreddit, setSubreddit] = useState("");
    const [searchEntirePosts, setSearchEntirePosts] = useState(false);
    const [AIGenerateSummary, setAIGenerateSummary] = useState(false);
    const [AIGenerateQuery, setAIGenerateQuery] = useState(false);
    const [summary, setSummary] = useState("");
    const [error, setError] = useState(null);
    const [posts, setPosts] = useState([]);
    const [reddit_api_params, setRedditAPIParams] = useState({});
    const [totalCost, setTotalCost] = useState(false);
    const [loading, setLoading] = useState(false); // New state for loading

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        // Validation: Check if the search term is not empty
        if (!query.trim()) {
            setError("Search term is required. What exactly do you think you are doing?");
            return;
        }

        setLoading(true); // Set loading to true when the request starts

        try {
            const response = await axios.post("http://127.0.0.1:5000/ask_reddit", {
                search_term: query,
                search_entire_posts: searchEntirePosts,
                ai_generate_summary: AIGenerateSummary,
                ai_generate_query: AIGenerateQuery,
                subreddit: subreddit,
            });
            if (response.status === 200) {
                setSummary(response.data.summary);
                setPosts(response.data.posts);
                setRedditAPIParams(response.data.reddit_api_params);
                setTotalCost(response.data.total_cost);
            }
        }  catch (err) {
            console.error(err);
            // Check for server error response
            if (err.response && err.response.data && err.response.data.message) {
                setError(err.response.data.message); // Set server-provided error message
            } else {
                setError("Failed to fetch data from the backend: " + err.message);
            }
        } finally {
            setLoading(false); // Set loading to false when the request completes
        }
    };

    const truncateText = (text, wordLimit) => {
        const words = text.split(" ");
        if (words.length > wordLimit) {
            return words.slice(0, wordLimit).join(" ") + "...";
        }
        return text;
    };

    return (
        <div className="form-container">
            <h1>Ask Reddit</h1>
            <h2><i>without asking Reddit</i></h2>
            <br />
            <form onSubmit={handleSubmit}>
                <label>
                    Search Term:
                    <br />
                    <input
                        type="text"
                        placeholder="gleba"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="input-field"
                    />
                </label>
                <br />
                <label>
                    Subreddit (optional):
                    <br />
                    <input
                        type="text"
                        placeholder="factorio"
                        value={subreddit}
                        onChange={(e) => setSubreddit(e.target.value)}
                        className="input-field"
                    />
                </label>
                <br />
                <label>
                    <input
                        type="checkbox"
                        checked={searchEntirePosts}
                        onChange={(e) => setSearchEntirePosts(e.target.checked)}
                    />
                    Search entire text of Reddit posts (costlier, probably better)
                </label>
                <br /><br />
                <h3 >Premium AI Experiences:</h3>
                <label>
                    <input
                        type="checkbox"
                        checked={AIGenerateSummary}
                        onChange={(e) => setAIGenerateSummary(e.target.checked)}
                    />
                    Summarize the Reddit posts to answer your question
                </label>
                <br />
                <label>
                    <input
                        type="checkbox"
                        checked={AIGenerateQuery}
                        onChange={(e) => setAIGenerateQuery(e.target.checked)}
                    />
                    Improve (maybe) the Reddit search query
                </label>
                <button type="submit" className="submit-button">
                    SUBMIT
                </button>
            </form>
            {loading && <p className="loading-message">Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {reddit_api_params && Object.keys(reddit_api_params).length > 0 && (
                <div className="query-params-box">
                    <h3>Query Parameters Used:</h3>
                    <pre>{JSON.stringify(reddit_api_params, null, 2)}</pre>
                </div>
            )}
            {summary && (
                <div className="summary-box">
                    <br />
                    {totalCost > 0 && ( // Conditionally display cost if totalCost is greater than zero
                        <>
                            <h3>Total Cost:</h3>
                            <p>${totalCost.toFixed(2)}</p>
                            <br />
                        </>
                    )}
                    <h2>Summary:</h2>
                    <p>{summary}</p>
                    <br />
                    <h2>Reddit Posts:</h2>
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
