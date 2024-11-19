import requests
import tiktoken


class AIHandler:
    def __init__(
        self, api_key=None, max_tokens = 200, openai_chat_model=None, api_url="https://api.openai.com/v1/chat/completions"
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.max_tokens = max_tokens
        self.openai_chat_model = openai_chat_model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def calculate_token_usage(self, messages):
        """
        Calculate the number of tokens used in a request.

        :param messages: List of message dicts for the chat (system and user messages).
        :param model: OpenAI model to use for the request (e.g., "gpt-3.5-turbo", "gpt-4").
        
        Returns:
        - Tuple containing the total number of tokens and the cost in USD.
        """
        try:
            # Get the tokenizer for the specified model
            encoding = tiktoken.encoding_for_model(self.openai_chat_model)

            # Tokenize each message and calculate total tokens
            total_tokens = 0
            for message in messages:
                tokens = encoding.encode(message["content"])
                total_tokens += len(tokens)

                # Add tokens for the role (e.g., "user" or "system")
                total_tokens += len(encoding.encode(message["role"]))
            total_cost = (total_tokens / 1_000_000) * 0.150

            return total_tokens, total_cost
        except Exception as e:
            return f"Error calculating token usage: {str(e)}"

    def send_request(
        self, messages, temperature=0.5
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
            "model": self.openai_chat_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": self.max_tokens,
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            chat_response = response.json()
            return chat_response["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"

    def generate_messages_summarize_posts(self, topic, text):
        """
        Summarize the given text using OpenAI's chat model.

        :param topic: The topic of the summarization.
        :param text: The content to summarize.
        :return: The message to send to the OpenAI chat model.
        """
        messages = [
            {
            "role": "system",
            "content": "You are an AI assistant tasked with summarizing information from Reddit posts. Focus solely on the provided content to generate an accurate and concise summary about the specified topic. Do not include opinions, assumptions, or information outside the provided text. Your summary should be no longer than 150 words and should avoid special formatting such as bullet points or markdown."
            },
            {
            "role": "user",
            "content": f"Here are some Reddit posts about this query: {topic}. If that topic seems like a question, answer the question. If not, provide some general information about the topic. Please provide your answer using the content of these posts fetched from Reddit: {text}. Even if the posts don't seem to answer the question, try to generate a relevant summary based on the information provided."
            }
        ]
        
        return messages

    def generate_messages_to_generate_query(self, search_term, subreddit=None):
        """
        Generate query parameters for a Reddit search from a natural language prompt.

        :param search_term: The natural language prompt provided by the user.
        """
        
        system_message_content = "You are an assistant that converts natural language questions into structured query parameters for a Reddit API search."

        if subreddit:
            subreddit_constraint = f"This must be set to '{subreddit}'."
        else:
            subreddit_constraint = "Suggest a subreddit (e.g., 'relationships', 'AskReddit', 'dating_advice') if the question implies a category, otherwise leave it None."
        
        user_message_content = f"""
        Turn the following prompt into query parameters for a Reddit API search. Generate the result as a Python dictionary.
        Keys:
        - search_term: A concise, effective search term derived from the prompt.
        - search_entire_posts: True if the question implies detailed answers, False otherwise.
        - limit: A reasonable number of posts to fetch (10-50) based on the complexity of the question.
        - sort: Choose between "relevance", "top", or "new".
        - time_period: Choose one of "day", "week", "month", "year", or "all".
        - restrict_sr: True if the question implies a specific subreddit, False otherwise.
        - subreddit: {subreddit_constraint}

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

        Prompt or Question: {search_term}
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

        return messages
        
    def generate_query_params(self, messages):
        """
        Generate query parameters for a Reddit search based on a natural language prompt.
        
        Parameters:
        - `messages` is created by `generate_messages_generate_query`.
        
        Returns:
        - A Python dictionary containing the query parameters.
        """

        response = self.send_request(messages)
        
        # OpenAI chat model returns the response in a code block. We need to extract the content from it.
        cleaned_response = response.strip("```python").strip("```").strip()
        try:
            return eval(cleaned_response)
        except Exception as e:
            return f"Error parsing response: {str(e)}"
        
