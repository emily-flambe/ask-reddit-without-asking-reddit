# reddit-data

This is a web application that collects data from the Reddit API and does fun things with it.

# How to run locally

## Docker

This app uses Vite, which has a known issue with installing Rollup. To work around this, we need to run these two commands in order to start the app:

```shell
docker compose run frontend npm i
docker-compose up --build
```

But fear not! The friendly Makefile lets you do this in one command:

```shell
make build
```

TODO: Add a Makefile command to prompt the user to setup environment variables (including API keys for integrations like OpenAI).

## Without Docker

Don't feel like running the app in Docker? I mean, I guess that's fine. It can be useful for debugging. Here's how you can run the app without Docker.

Start the backend:

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

I should make these into Github issues or something lol

- [ ] Add a button enabling the user to fetch more posts to incorporate into the summary
- [ ] Add a text box for the user to ask follow up questions to the AI
- [ ] Even Smarter Search: Some way of executing multiple queries and combining the results to answer a question
- [ ] Group the top posts by topic
- [ ] Add a scheduler to collect data at regular intervals
- [ ] Add more features to the data collection (e.g. collect comments, more metadata)
- [ ] Add data analysis and visualization
- [ ] Set up my own LLM with ollama
- [ ] Enable app to be run with ollama OR with OpenAI API based on config
- [ ] Add a feature that fetches posts with screenshots and displays those screenshots in the UI, with captions based on the content of the post (This could be an entirely different project: Reddit Image Search)
- [ ] Add user management and enable a logged in user to save queries and results (how crazy would it be to implement google auth?)
- [ ] Use the Pushshift API to enable including comments in search results (Reddit API only supports searching top-level posts)

Some additional ideas for larger spin-off projects:

### Reddit Image Search

Something like Google Image Search, but specifically using Reddit posts?

### Reddit Topic Subscriber

Get email digest of new posts relating to a topic and/or within a specific subreddit

### Reddit Scraper

Set up some search params, hit "go", and let the app scrape Reddit for you, running at regular intervals to collect new relevant posts and add them to a database. (Could this involve spinning up k8s pods?)