import os
from functools import cache
from dotenv import load_dotenv

load_dotenv()
@cache
def get_openai_client():
    from openai import OpenAI
    openai_client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    return openai_client