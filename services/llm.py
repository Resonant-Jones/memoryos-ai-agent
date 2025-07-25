import os
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, messages):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, base_url):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_response(self, messages):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content

def get_llm_provider(provider_name, **kwargs):
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=kwargs.get("api_key"),
            base_url=kwargs.get("base_url")
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
