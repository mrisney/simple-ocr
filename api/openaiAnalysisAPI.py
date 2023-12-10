import httpx
import json
import logging
import re

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Constants for OpenAI API
OPENAI_API_KEY = "[API-KEY]"

OPENAI_API_URL = "https://api.openai.com/v1/completions"
MODEL = "text-davinci-003"

# Questions and their corresponding key phrases for parsing
questions = [
    "What type of document is this?",
    "What is the NAIC?",
    "What is the License Plate Number?",
    "What is the Vehicle Make?",
    "What is the Vehicle Color?",
    "What is the Type?",
    "What is the Year and or Model?",
    "What is the Vehicle Identification Number?",
    "What is the Vehicle Registration Number?",
    "What is the Date First Sold?",
    "What is the TCI Number?",
    "What is the Weight?",
    "What is the Class?",
    "What is the State Fee?",
    "What is the County Fee?",
    "What is the Last day of Registration?",
    "What is Day of Renewal?",
    "What is Date Issued?",
    "What is Emblem Number?",
    "What is the Inspection Date of the Vehicle?"
    "What is the Name of Insurance Company?",
    "What is the Name and Address of the Owners?"
    "Who are the Registered owner or owners of the vehicle?",
    "What is the Registered owners Street Address?",
    "Who are the Registered owners of the vehicle?",
    "What is the Effective Date?",
    "What is the Expiration Date?",
    "What is the Policy?",
    "What is the Policy Number?",
    "What is the Insurance Company?"     
]

def post_process_combined_answer(combined_answer, questions):
    qa_map = {q: "" for q in questions}
    segments = combined_answer.split("Question:")

    for segment in segments[1:]:
        parts = segment.split("Answer:")
        if len(parts) == 2:
            question = parts[0].strip()
            answer = parts[1].strip()

            # Remove repetition of the question in the answer
            answer = answer.replace(question, '').strip()

            # Exclude non-informative answers and redundancy
            if "not mentioned in the text" not in answer.lower() and answer != '' and question in qa_map:
                qa_map[question] = answer
            elif question not in qa_map:
                logging.warning(f"Question not recognized: {question}")
        else:
            logging.warning(f"Unexpected segment format: {segment}")

    return [{question: qa_map[question]} for question in questions if qa_map[question]]









async def query_gpt3(ocr_text):
    logging.info(f"OCR Text: {ocr_text}")
    questions_prompt = "\n".join(f"- {q}" for q in questions)
    prompt = f"""
    Based on the following text extracted from a scanned document, answer the following questions using the format 'Question: [question] Answer: [answer]'. 
    If the information for a question is not explicitly mentioned in the text, leave the question unanswered.
    
    Text:
    {ocr_text}

    Questions:
    {questions_prompt}
    """



    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.1,
        "max_tokens": 512
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_API_URL, headers=headers, data=json.dumps(data), timeout=10.0)
            response.raise_for_status()
            answer_str = response.json()['choices'][0]['text'].strip()
            logging.info(f"Received answer from chatGPT: {answer_str}")
            
            qa_pairs = post_process_combined_answer(answer_str, questions)

            if not qa_pairs:
                logging.warning("No question-answer pairs found.")
                return {"status": "No answers found"}
            else:
                return {"question_answer_pairs": qa_pairs}
    except httpx.TimeoutException as e:
        logging.error("Request timed out.")
        return {"status": "HTTP error occurred", "code": 503, "body": "Request timed out"}        
    except httpx.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err.response.status_code}")
        logging.error(f"Response: {http_err.response.text}")
        return {"status": "HTTP error occurred", "code": http_err.response.status_code, "body": http_err.response.text}
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return {"status": "Error occurred during processing"}


# The main function to execute the script
if __name__ == "__main__":
    import asyncio
    ocr_text = """
    CALIFORNIA EVIDENCE OF FINANCIAL RESPONSIBILITY
    Name and Address of Insured NAIC 25968
    """
    results = asyncio.run(query_gpt3(ocr_text))
    print(results)
