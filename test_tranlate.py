import os
import requests

# Set your OpenRouter API key here or in environment variable OPENROUTER_API_KEY
API_KEY = "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"

# OpenRouter API endpoint for completions
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def translate_text_openrouter(text: str, target_lang: str) -> str:
    """
    Translate `text` to `target_lang` using OpenRouter chat completion API.
    target_lang: language name like 'Hindi', 'French', 'Spanish' etc.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Compose prompt to instruct model to translate
    prompt = f"Translate the following text to {target_lang}:\n\n{text}"

    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct",  # example model, replace if needed
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()

    try:
        # The generated translation will be in choices[0].message.content
        translated_text = data["choices"][0]["message"]["content"].strip()
        return translated_text
    except (KeyError, IndexError):
        return "Failed to parse translation response"

# Example usage
if __name__ == "__main__":
    text_to_translate = "Hello, how are you?"
    target_language = "Hindi"

    translation = translate_text_openrouter(text_to_translate, target_language)
    print("Translated Text:", translation)
