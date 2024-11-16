# app/chatgpt_summarizer.py

import os
import requests


class ChatGPTSummarizer:
    def __init__(self):
        self.api_key = os.getenv("CHATGPT_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def summarize(self, topic, text):
        """
        Send a request to the ChatGPT API to summarize the given text.

        :param text: The content to be summarized.
        :return: A summary string or an error message if the request fails.
        """
        prompt = f"Please help me understand more about {topic} based on these Reddit posts: {text}"
        data = {
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are summarizing posts from multiple Reddit users in order to help me understand more about {topic}. Limit your response to 300 words.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.5,
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            # Extract and return the summary from ChatGPT's response
            chat_response = response.json()
            summary = chat_response["choices"][0]["message"]["content"]
            return summary
        else:
            # Handle error and return error details
            return f"Error: {response.status_code}, {response.text}"
