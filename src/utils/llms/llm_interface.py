import pydantic
from pydantic import BaseModel
from src.config import get_openai_client

class LLMInterface:
    def __init__(self):
        self.client = get_openai_client()

    def get_response(self, system: str, user: str, response_model: type[BaseModel]):
        """
        Call the OpenAI API and instruct it to return a JSON structure that adheres to the provided Pydantic model.
        """
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            response_format=response_model,
        )
        return completion.choices[0].message.parsed
