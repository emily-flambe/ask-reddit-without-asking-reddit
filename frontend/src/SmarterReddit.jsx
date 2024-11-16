import React, { useState } from "react";
import axios from "axios";

function SmarterAskReddit() {
    const [query, setQuery] = useState("");
    const [subreddit, setSubreddit] = useState("");
    const [searchEntirePosts, setSearchEntirePosts] = useState(false);
    const [summary, setSummary] = useState("");
    const [error, setError] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false); // New state for loading

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true); // Set loading to true when the request starts

        try {
            const response = await axios.post("http://127.0.0.1:5000/smarter_ask_reddit", {
                search_term: query,
                search_entire_posts: searchEntirePosts,
                subreddit: subreddit,
            });

            if (response.status === 200) {
                setSummary(response.data.summary);
                setPosts(response.data.posts);
            }
        } catch (err) {
            console.error(err);
            setError("Failed to fetch data from the backend.");
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
        <div style={{ maxWidth: "500px", margin: "0 auto", padding: "20px" }}>
            <h1>Smarter Ask Reddit</h1>
            <h2><i>Let the magical internet brain sort out the querying</i></h2>
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
                <button type="submit" className="submit-button">
                    SUBMIT
                </button>
            </form>
            {loading && <p>Loading...</p>} {/* Display loading message */}
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

export default SmarterAskReddit;
