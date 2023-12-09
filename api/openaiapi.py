import httpx
import os
import json

os.environ["OPENAI_API_KEY"] = "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"

async def query_gpt3(ocr_text):
    prompt = f"""The following text is extracted from a vehicle registration document: 
    {ocr_text}
    
    Please provide answers to these questions based on the text, and do not generate any additional questions:
    - What type of document is this?
    - What is the inusrance company?
    - What is the registered owner's address?
    - What is the vehicle identication number?
    - Who are the registered owners?
    - What is the make of the car?
    - What is the year of the car?
    - What is the effective date ?
    - What is the expiration date ?
    - What is the policy number?
    """

    url = "https://api.openai.com/v1/completions"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150  # Adjust based on your needs
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=json.dumps(data))
        return response.json()['choices'][0]['text'].strip()
