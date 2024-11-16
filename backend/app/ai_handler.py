import os
import requests


class AIHandler:
    def __init__(
        self, api_key=None, api_url="https://api.openai.com/v1/chat/completions"
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send_request(
        self, messages, model="gpt-4o-mini-2024-07-18", temperature=0.5, max_tokens=200
    ):
        """
        Send a request to the OpenAI API with the given parameters.

        :param messages: List of message dicts for the chat (system and user messages).
        :param model: OpenAI model to use for the request.
        :param temperature: Sampling temperature for the response.
        :param max_tokens: Maximum tokens in the response.
        :return: The API response content or an error message.
        """
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            chat_response = response.json()
            return chat_response["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"

    def summarize(self, topic, text):
        """
        Summarize the given text using OpenAI's chat model.

        :param topic: The topic of the summarization.
        :param text: The content to summarize.
        :return: The summary or an error message.
        """
        messages = [
            {
                "role": "system",
                "content": f"You are summarizing posts from multiple Reddit users to help me understand more about {topic}. Limit your response to 300 words.",
            },
            {
                "role": "user",
                "content": f"Please help me understand more about {topic} based on these Reddit posts: {text}",
            },
        ]
        return self.send_request(messages)

    def generate_query_params(self, natural_language_prompt):
        """
        Generate query parameters for a Reddit search from a natural language prompt.

        :param natural_language_prompt: The natural language prompt provided by the user.
        :return: Generated query parameters as a Python dictionary or an error message.
        """

        system_message_content = "You are an assistant that converts natural language questions into structured query parameters for a Reddit API search."
        user_message_content = f"""
        Turn the following prompt into query parameters for a Reddit API search. Generate the result as a Python dictionary.
        Keys:
        - search_term: A concise, effective search term derived from the prompt.
        - search_entire_posts: True if the question implies detailed answers, False otherwise.
        - limit: A reasonable number of posts to fetch (10-50) based on the complexity of the question.
        - sort: Choose between "relevance", "top", or "new".
        - time_period: Choose one of "day", "week", "month", "year", or "all".
        - restrict_sr: True if the question implies a specific subreddit, False otherwise.
        - subreddit: Suggest a subreddit (e.g., "relationships", "AskReddit", "dating_advice") if the question implies a category, otherwise leave it None.

        Example question: "How to tell if a boy likes you?"
        Expected output:
        {{
            "search_term": "boy likes me",
            "search_entire_posts": True,
            "limit": 20,
            "sort": "relevance",
            "time_period": "all",
            "restrict_sr": True,
            "subreddit": "dating_advice"
        }}

        Prompt or Question: {natural_language_prompt}
        """

        messages = [
            {
                "role": "system",
                "content": system_message_content,
            },
            {
                "role": "user",
                "content": user_message_content,
            },
        ]

        response = self.send_request(messages, max_tokens=1000)  # increase max_tokens for a PREMIUM experience. Parameterize this later maybe.
        
        # OpenAI chat model returns the response in a code block. We need to extract the content from it.
        cleaned_response = response.strip("```python").strip("```").strip()
        try:
            return eval(cleaned_response)
        except Exception as e:
            return f"Error parsing response: {str(e)}"
