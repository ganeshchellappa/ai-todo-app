import os
import requests
from dotenv import load_dotenv
import re

load_dotenv()  # Load .env variables

# HF_API_URL = "https://api-inference.huggingface.co/models/facebook/m2m100_418M"
# HF_API_KEY = os.getenv("HF_API_KEY")

API_KEY = ""
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

LANG_CODES = {
    "english": "en",
    "hindi": "hi",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
}

# print("api_key_1",API_KEY)

def translate_text(text, target_lang):
    lang_ids = {
        "en": 250004, "hi": 250044, "fr": 250018, "de": 250019,
        "es": 250026, "zh": 250039, "ja": 250036, "ko": 250037,
    }
   
    lang_id = lang_ids.get(target_lang.lower())
    print("language used",lang_id)

    if lang_id is None:
        return "Unsupported language"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    } 

    # Compose prompt to instruct model to translate
    prompt = f"Translate the following text to {target_lang}:\n\n{text}"
    # print("prompt",prompt)

    payload = {
        "model": "moonshotai/kimi-k2:free",  # example model, replace if needed
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    # print("response", response)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()
    # print('the main data: ', data)

    try:
        # The generated translation will be in choices[0].message.content
        translated_text = data["choices"][0]["message"]["content"].strip()

        matches = re.findall(r"\*\*(.*?)\*\*", translated_text, re.DOTALL)
        if matches:
            # Return the first match which should be the main translated sentence
            return matches[0].strip()

        print(matches)  # Debugging: print translated text


        return translated_text
    except (KeyError, IndexError):
        return "Failed to parse translation response"

# Example usage:
print(translate_text("Hello, how are you?", "hi"))

