import os
import csv
import re
import requests
from dotenv import load_dotenv
from groq import Groq
from prompt import get_phase_one, get_phase_two
from source_material import source_material

# Load environment variables from .env file
load_dotenv()

# GROQ Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),  # Use os.getenv to get the key
)

# WINSTON Auth
winston_key = os.getenv("WINSTON_API_KEY")
print(winston_key)
WINSTON_headers = {
    "Authorization": f"Bearer {winston_key}",
    "Content-Type": "application/json",
}


# GROQ: Get score based on quality and relevance metrics
def get_phase_score(question, essay, phase, source_material=""):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    get_phase_one(question, essay)
                    if phase == 1
                    else get_phase_two(question, essay, source_material)
                ),
            }
        ],
        model="llama3-8b-8192",
    )

    # Get the response content
    response_content = chat_completion.choices[0].message.content.strip()

    # Try to convert the response to a float to check if it's a number
    try:
        score = float(response_content)
        return score  # Return the score if it's a valid number
    except ValueError:
        # If it's not a valid number, search for the first number in the response text
        numbers = re.findall(
            r"\d+\.?\d*", response_content
        )  # Find all numbers (including decimals)

        if numbers:
            return float(numbers[0])  # Return the first number found as a float
        else:
            return None  # Return None if no numbers were found


def get_plagiarism_score(answer, headers):
    url = "https://api.gowinston.ai/v2/plagiarism"

    payload = {
        "text": answer,
        "language": "en",
        "country": "ph",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the plagiarism score
        score = json_response.get("result", {}).get("score", None)

        if score is not None:
            return score
        else:
            print("Score not found in the response.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def get_ai_score(answer, headers):
    url = "https://api.gowinston.ai/v2/plagiarism"

    payload = {
        "text": answer,
        "version": "2.0",
        "sentences": True,
        "language": "en",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the plagiarism score
        score = json_response.get("result", {}).get("score", None)

        if score is not None:
            return score
        else:
            print("Score not found in the response.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
