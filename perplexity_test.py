import requests
import os

url = "https://api.perplexity.ai/chat/completions"

API_KEY = os.environ.get("PERP_API_KEY")

from pydantic import BaseModel

class AnswerFormat(BaseModel):
    step_name: str
    short_des: str
    order: int

payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "system",
            "content": "Be concise and precise. You'll be asked to return a set of steps - return them as JSON objects with the following fields: step_name, description, is_current_step_bool. Only one step should be the current step. If no other context is provided, the first step should be the current one, so in that case set is_current_step_bool to true. Format the JSON in a way that it doesn't contain any irrelevant whitespace"
        },
        {
            "role": "user",
            "content": "How do I bake a tres leches cake"
        }
    ],
    "max_tokens": 1000,
    "temperature": 0.2,
    "top_p": 0.9,
    "search_domain_filter": None,
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "year",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1,
    "response_format": {
		    "type": "json_schema",
        "json_schema": {"schema": AnswerFormat.model_json_schema()},
    },
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload).json()
# print(response["choices"][0]["message"]["content"])
print(response["citations"])
