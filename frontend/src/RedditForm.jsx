import React, { useState } from "react";
import axios from "axios";

function RedditForm() {
    const [query, setQuery] = useState("");
    const [subreddit, setSubreddit] = useState("");
    const [searchEntirePosts, setSearchEntirePosts] = useState(false);
    const [generateRedditQueryUsingAI, setGenerateRedditQueryUsingAI] = useState(false);
    const [summary, setSummary] = useState("");
    const [error, setError] = useState(null);
    const [posts, setPosts] = useState([]);
    const [reddit_api_params, setRedditAPIParams] = useState({});
    const [skipAI, setSkipAI] = useState(false);
    const [loading, setLoading] = useState(false); // New state for loading

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true); // Set loading to true when the request starts

        try {
            const response = await axios.post("http://127.0.0.1:5000/ask_reddit", {
                search_term: query,
                search_entire_posts: searchEntirePosts,
                generate_reddit_query_using_ai: generateRedditQueryUsingAI,
                subreddit: subreddit,
            });

            if (response.status === 200) {
                setSummary(response.data.summary);
                setPosts(response.data.posts);
                setRedditAPIParams(response.data.reddit_api_params);
                setSkipAI(response.data.skip_ai);
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
                    <input
                        type="text"
                        placeholder="gleba"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="input-field"
                    />
                </label>
                <label>
                    Subreddit (optional):
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
                    Search Entire Posts:
                    <input
                        type="checkbox"
                        checked={searchEntirePosts}
                        onChange={(e) => setSearchEntirePosts(e.target.checked)}
                    />
                </label>
                <br />
                <label>
                    Use fancy AI to query Reddit (ULTRA PREMIUM EXPERIENCE):
                    <input
                        type="checkbox"
                        checked={generateRedditQueryUsingAI}
                        onChange={(e) => setGenerateRedditQueryUsingAI(e.target.checked)}
                    />
                </label>
                <button type="submit" className="submit-button">
                    SUBMIT
                </button>
            </form>
            {loading && <p className="loading-message">Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {summary && (
                <div className="summary-box">
                    <h2>Summary:</h2>
                    <p>{summary}</p>
                    <br />
                    <h3>Query Parameters Used:</h3>
                    <div className="query-params-box">
                        <pre>{JSON.stringify(reddit_api_params, null, 2)}</pre>
                    </div>
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
