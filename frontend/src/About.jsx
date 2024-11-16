import React from "react";
import "./About.css"; // Include the CSS file for styles

function About() {
    return (
        <div className="about-container">
            <div className="about-content">
                <h1 className="about-title">Emily REDACTED</h1>
                <p className="about-tagline">
                    Data Engineer. Innovator. Dreamer.
                </p>
                <p className="about-description">
                    A woman of intellect and ambition, Emily strides through life with a fierce determination to make her mark. 
                    Her code is a symphony of logic and elegance, her mind a forge of ingenious solutions, and her presence 
                    commands respect and admiration in equal measure. She wields her skills like an artist, crafting 
                    data into stories that empower and inspire. To know her is to witness excellence redefined.
                </p>
                <p className="about-quote">
                    "She doesn’t just walk into a room; she dominates it. The kind of woman you don’t forget." 
                </p>
            </div>
        </div>
    );
}

export default About;
