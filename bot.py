import os

import requests
from openai import OpenAI


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    webhook_url = os.getenv("WEBHOOK_URL")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no está configurada")
    if not webhook_url:
        raise RuntimeError("WEBHOOK_URL no está configurada")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Genera un texto corto y amigable para una publicación automática.",
    )

    generated_text = response.output_text.strip()
    requests.post(webhook_url, json={"text": generated_text}, timeout=30).raise_for_status()


if __name__ == "__main__":
    main()
