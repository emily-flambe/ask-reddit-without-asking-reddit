import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RedditForm from "./RedditForm";
import About from "./About";

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    {/* Define a route for the RedditForm component */}
                    <Route path="/" element={<RedditForm />} />
                    <Route path="/about" element={<About />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
