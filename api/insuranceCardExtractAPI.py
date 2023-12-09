import httpx
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Constants for OpenAI API
OPENAI_API_KEY = "[API KEY]"

OPENAI_API_URL = "https://api.openai.com/v1/completions"
MODEL = "text-davinci-003"

# Questions and their corresponding key phrases for parsing
questions = [
    "What type of document is this?",
    "What is the NAIC?"
    "What is the insurance company?",
    "What is the registered owner's address?",
    "What is the vehicle identification number?",
    "Who are the registered owners?",
    "What is the make of the car?",
    "What is the year of the car?",
    "What is the effective date?",
    "What is the expiration date?",
    "What is the policy?",
    "What is the number?"
    
]

key_phrases = {
    "What type of document is this?": "This is a",
    "What is the NAIC?" : "The NAIC is",
    "What is the insurance company?": "The insurance company is",
    "What is the registered owner's address?": "The registered owner's address is",
    "What is the vehicle identification number?": "The vehicle identification number is",
    "Who are the registered owners?": "The registered owners are",
    "What is the make of the car?": "The make of the car is",
    "What is the year of the car?": "The year of the car is",
    "What is the effective date?": "The effective date is",
    "What is the expiration date?": "The expiration date is",
    "What is the policy?": "The policy is",
    "What is the number?": "The number is",
    
}


def extract_answers_to_json(answer_str, questions, key_phrases):
    sentences = [s.strip() for s in answer_str.split('.')]
    qa_pairs = {}
    for question, key_phrase in key_phrases.items():
        for sentence in sentences:
            if sentence.startswith(key_phrase):
                answer = sentence
                qa_pairs[question] = answer
                break
    return qa_pairs

async def query_gpt3(ocr_text):
    questions_prompt = "\n".join(f"- {q}" for q in questions)
    prompt = f"""The following text is extracted from a vehicle registration document: 
    {ocr_text}
    
    Please provide answers to these questions based on the text, and do not generate any additional questions:
    {questions_prompt}
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.3,
        "max_tokens": 150
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            answer_str = response.json()['choices'][0]['text'].strip()
            qa_pairs = extract_answers_to_json(answer_str, questions, key_phrases)
            return qa_pairs
    except httpx.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return {}  # Return empty dict in case of errors

# Example usage (within an async context)
# ocr_text = "Your OCR extracted text here"
# response = await query_gpt3(ocr_text)