import os
import requests


class AIHandler:
    def __init__(self, api_key=None, api_url="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send_request(
        self, messages, model="gpt-4o-mini-2024-07-18", temperature=0.5, max_tokens=300
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

    def generate_query_params(self, question):
        """
        Generate query parameters for a Reddit search from a natural language question.

        :param question: The natural language question.
        :return: Generated query parameters as a Python dictionary or an error message.
        """
        messages = [
            {
                "role": "system",
                "content": "You are an assistant that converts natural language questions into structured query parameters for a Reddit API search.",
            },
            {
                "role": "user",
                "content": f"Turn the following question into query parameters: {question}",
            },
        ]
        response = self.send_request(messages)
        try:
            return eval(
                response
            )  # Convert string to dictionary (ensure response is safe and validated).
        except Exception as e:
            return f"Error parsing response: {str(e)}"
