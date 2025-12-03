# src/models/llm.py
"""
LLM wrapper using the Groq API.

This replaces any local Torch/Transformers model and avoids all local GPU/CPU issues.
It keeps the same LocalLLM.chat(system_prompt, user_prompt) interface used by the orchestrator.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq

from src.config import LLM_MODEL_NAME


class LocalLLM:
    def __init__(self, max_new_tokens: int = 512, temperature: float = 0.3):
        # Load environment variables from .env (if present)
        load_dotenv()

        api_key: Optional[str] = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Please add it to your environment or .env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = LLM_MODEL_NAME
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        print(f"[Groq LLM] Using Groq model: {self.model}")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a chat completion request to the Groq API and return the model's reply text.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_new_tokens,
            temperature=self.temperature,
        )

        # Groq returns choices[0].message.content
        return response.choices[0].message.content.strip()
