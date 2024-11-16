import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RedditForm from "./RedditForm";
import SmarterAskReddit from "./SmarterReddit";
import About from "./About";

function Layout() {
    return (
        <div className="layout">
            {/* Left Navigation Bar */}
            <nav className="nav-container">
                <h3>Navigation</h3>
                <ul>
                    <li>
                        <Link to="/">About</Link>
                    </li>
                    <li>
                        <Link to="/reddit-form">Reddit Form</Link>
                    </li>
                    <li>
                        <Link to="/smarter-ask-reddit">Smarter Ask Reddit</Link>
                    </li>
                </ul>
            </nav>

            {/* Main Content Area */}
            <div className="main-content">
                <Routes>
                    <Route path="/" element={<About />} />
                    <Route path="/reddit-form" element={<RedditForm />} />
                    <Route path="/smarter-ask-reddit" element={<SmarterAskReddit />} />
                </Routes>
            </div>
        </div>
    );
}


function App() {
    return (
        <Router>
            <Layout />
        </Router>
    );
}

export default App;
