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
    "What is the License Number?"
    "What is the Make?",
    "What is the Type?",
    "What is the Year Model?",
    "Who are the Vehicle Registration Number?",
    "What is the Date First Sold?",
    "What is the TCI Number?",
    "What is the Weight?",
    "What is the Class?",
    "What is the State Fee?",
    "What is the County Fee?",
    "What is the Last day of Registration?",
    "What is day of Renewal?",
    "What is date Issued?",
    "What is validation Emblem Number?"   
]

key_phrases = {
    "What type of document is this?": "This is a",
    "What is the License Number?" : "The License Number is",
    "What is the Make?": "The Make is",
    "What is the Type?": "The Type is",
    "What is the Year Model?": "The Year Model is",
    "Who are the Vehicle Registration Number?": "The Vehicle Registration Number is",
    "What is the Date First Sold?": "The Date First Sold is",
    "What is the TCI Number?": "The TCI Number is",
    "What is the Weight?": "The Weight is",
    "What is the Class?": "The Class is",
    "What is the State Fee?": "The State Fee is",
    "What is the County Fee?": "The County Fee is",
     "What is the Last day of Registration?": "The Last day of Registration is",
    "What is day of Renewal?" : "The day of Renewal is",
    "What is date Issued?" : "The date Issued is",
    "What is validation Emblem Number?" :  "The validation Emblem Number is"
    
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
        "temperature": 0.2,
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