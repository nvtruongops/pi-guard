import os
from abc import ABC, abstractmethod

import httpx


class BaseLLMProvider(ABC):
    """Abstract interface for API-driven downstream LLM backends behind PI-Guard."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generates a response from the downstream target LLM via Cloud API."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """Simulated LLM backend for local testing, automated pytest CI, and offline benchmarks."""

    def __init__(self, model_name: str = "mock-llm-v1"):
        self.model_name = model_name

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        return f"[{self.model_name} Safe Response] Successfully generated response for: '{prompt[:45]}...'"


class OpenAILLMProvider(BaseLLMProvider):
    """Cloud OpenAI API Provider (supports gpt-4o-mini, gpt-4o, gpt-3.5-turbo)."""

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str | None = None, base_url: str = "https://api.openai.com/v1"):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "[OpenAI Error]: Missing OPENAI_API_KEY in environment."

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.0
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI API Error on {self.model_name}]: {str(e)}"


class GeminiLLMProvider(BaseLLMProvider):
    """Google Gemini Cloud API Provider (supports gemini-1.5-flash, gemini-1.5-pro)."""

    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: str | None = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "[Gemini Error]: Missing GEMINI_API_KEY in environment."

        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Context: {system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow the instructions."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        headers = {
            "Content-Type": "application/json"
        }
        params = {"key": self.api_key}
        payload = {
            "contents": contents,
            "generationConfig": {"temperature": 0.0}
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(self.endpoint_url, params=params, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"[Gemini API Error on {self.model_name}]: {str(e)}"


class GroqCloudLLMProvider(BaseLLMProvider):
    """Ultra-fast Serverless API Provider via Groq / OpenAI-compatible Cloud (supports Llama-3.1-8b, Mistral-7b, Qwen-2.5-7b)."""

    def __init__(self, model_name: str = "llama-3.1-8b-instant", api_key: str | None = None, base_url: str = "https://api.groq.com/openai/v1"):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "[Groq/Cloud Error]: Missing GROQ_API_KEY in environment."

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.0
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Cloud API Error on {self.model_name}]: {str(e)}"


def get_llm_provider(provider_type: str = "mock", model_name: str | None = None) -> BaseLLMProvider:
    """Factory to instantiate pure API-driven LLM providers without local GPU overhead."""
    provider_type = provider_type.lower()
    if provider_type == "openai":
        return OpenAILLMProvider(model_name=model_name or "gpt-4o-mini")
    elif provider_type == "gemini":
        return GeminiLLMProvider(model_name=model_name or "gemini-1.5-flash")
    elif provider_type in ["groq", "cloud_open_weights"]:
        return GroqCloudLLMProvider(model_name=model_name or "llama-3.1-8b-instant")
    else:
        return MockLLMProvider(model_name=model_name or "mock-api-llm")
