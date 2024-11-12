# reddit-data

# Backend

Application Factory (__init__.py):

The create_app function in __init__.py sets up the Flask app, loads configurations, initializes the database, and registers the main blueprint from routes.py.
Entry Point (main.py):

main.py calls create_app() and runs the Flask application.
Routes and API Logic (routes.py and data_collector.py):

The routes in routes.py call the data collection and storage functions in data_collector.py.
data_collector.py handles interactions with the Reddit API and stores collected data in the database defined in models.py.
Database (models.py and db/):

Data is stored and managed through SQLAlchemy, with models defined in models.py.

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