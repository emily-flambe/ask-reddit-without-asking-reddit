# reddit-data

https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

# Authenticate to Reddit API (OAuth2)
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