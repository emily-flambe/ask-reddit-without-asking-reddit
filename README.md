# reddit-data

This is a web application that collects data from the Reddit API and does fun things with it.

# How to run locally

Set up a virtual environment, install dependencies, and run the Flask app.

```shell
cd backend
source .env
source .venv/bin/activate
flask run
```

Start the frontend.

```shell
cd frontend
npm run dev
```

### Data collection

This application can be run in the background to continually collect data from the Reddit API. The data is then stored in a database, which can be queried later, for fun and profit.

### Whaddaya Hear, Whaddaya Say

The user can specify a query and get a summary (generated by GPT3.5) of what people are saying about that topic in a specific subreddit.

### Ask Reddit Without Asking Reddit

Do you have a question that you want to ask Reddit, but you don't want to actually ask Reddit? Are you a busy person who doesn't have time to read through all the different threads that have already been created about a topic? This application has you covered. Specify a question and a subreddit and ChatGPT will look through relevant posts and comments to give you a summary of what people are saying.

The user can ask a question and get a summary of the responses from a specific subreddit. The response is generated by ChatGPT and is based on a query of Reddit posts and comments relevant to the user's question.

# Usage

Uhh this project doesn't have a real frontend yet, so here's how to run the Flask app. 

```shell
cd backend
source .env
source .venv/bin/activate
flask run
```

# Run with Docker (to be more legit)

Build the Docker image: 

```shell
docker build -t flask-reddit-app .
```


# Project Structure

```shell
app/
├── __init__.py               # Initializes the Flask app
├── config.py                 # Configuration settings
├── data_collector.py         # Handles data collection from the Reddit API
├── database_models.py        # Contains SQLAlchemy models for the database
├── db_setup.py               # Database setup and initialization
├── main.py                   # Entry point to start the Flask app
└── routes.py                 # Defines routes (endpoints) for the app
```

# Authentication to Reddit API (OAuth2)

```shell

source .env

# fetch access token
response=$(curl -X POST -d "grant_type=password&username=${REDDIT_USERNAME}&password=${REDDIT_PASSWORD}" --user "${OAUTH_CLIENT_ID}:${OAUTH_SECRET}" https://www.reddit.com/api/v1/access_token)

# Extract values using jq
ACCESS_TOKEN=$(echo "$response" | jq -r '.access_token')
EXPIRES_IN=$(echo "$response" | jq -r '.expires_in')

# Print values to verify
echo "Access Token: $access_token"
echo "Expires In: $expires_in"
```

# Example Request

```shell
curl -X GET "https://oauth.reddit.com/api/v1/me" \
     -H "Authorization: bearer ${ACCESS_TOKEN}" \
     -H "User-Agent: ChangeMeClient/0.1 by ${REDDIT_USERNAME}"
```

# OAuth2 for web app

- Obtain an access token from:  https://www.reddit.com/api/v1/authorize?client_id=9pm_xn3RqULPQedre524nQ&response_type=code&state=random&redirect_uri=https://www.google.com&duration=permanent&scope=identity -- hopefully only need to do this once in order to obtain a refresh token.
- Obtain the refresh token:

```shell
CLIENT_ID=foo
CLIENT_SECRET=bar
ACCESS_CODE=yeet

curl -X POST https://www.reddit.com/api/v1/access_token \
  -u "${CLIENT_ID}:${CLIENT_SECRET}" \
  -d "grant_type=authorization_code" \
  -d "code=${ACCESS_CODE}" \
  -d "redirect_uri=https://www.google.com" \
  -H "User-Agent: YourAppName/1.0"
```


# Fantasy Land 

Or maybe fantasies, who knows.

I should make these into Github issues lol

- [ ] Tell user about the cost before asking to confirm if asking reddit with Premium AI Experience
- [ ] Browser should show the exact API request that was made
- [ ] Make the frontend *aesthetic*
- [ ] Group the top posts by topic
- [ ] Add a scheduler to collect data at regular intervals
- [ ] Add more features to the data collection (e.g. collect comments, more metadata)
- [ ] Add data analysis and visualization
- [ ] Set up my own LLM with ollama
- [ ] Add a feature that fetches posts with screenshots and displays those screenshots in the UI, with captions based on the content of the post (This could be an entirely different project: Reddit Image Search)
- [ ] Add user management and enable a logged in user to save queries and results (how crazy would it be to implement google auth?)
- [ ] Use the Pushshift API to enable including comments in search results (Reddit API only supports searching top-level posts)
- [ ] Add the ability to ask ChatGPT follow up questions from the browser
- [ ] NEW FEATURE: Reddit Image Search
- [ ] NEW FEATURE: Reddit Topic Subscriber (get notified when a new post is made about a specific topic, like, I dunno, crows)