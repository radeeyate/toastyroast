import os
import dotenv
import google.generativeai as genai
from pymongo import MongoClient

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_KEY"))
client = MongoClient(os.getenv("CONNECTION_STRING"))
db = client["toastyroast"]
coll = db["roasts"]

generation_config = {
    "temperature": 0.85,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

prompt = """
In front of you, is an image. If it does not contain a human face, please return "Face not found" and stop.
If it does contain a face or a human body, we want to roast it. We have some categories we want to roast/rate it on.
The ratings must be numeric, and not floats or "N/A". Categories rated as "N/A" will be denied and not accepted.

These are the we want to rated and roasted of the following:

* Rizz: scale of 1 (awkward silence) to 10 (legendary wingman)
* Clothes: scale of 1 (thrift store chic) to 10 (red capted ready)
* Vibes: scale of 1 (awkward silence) to 10 (very energetic and exciting)
* Background: scale of 1 (ugly, boring, unhappy background) to 10 (beautiful landscape, vibrant scenery)
* Style: scale of 1 (questionable fashion choices) to 10 (trendsetter)
* Humor: scale of 1 (crickets) to 10 (everyone is laughing)

I have some guidelines for the ratings and reasons:
No pronouns, keep it direct and specific. Talk directly to the person, use "you."
No gendered terms like "boy" or "girl" to avoid misgendering.
Use the same format for your response as provided below.
If the person has a low rating for a specific category, (4 and below), roast them, burn them hard. If you the response is 5 or above, give a compliment or tip to improve.
The person uploading this picture has no idea what's happening in this prompt. Please do not mention captions, prompts, responses, etc.
N/A is not an answer. If you provide N/A, it is not a valid answer. You can always judge by the image, do not be afraid.
Be ruthless but hilarious. Don't hold back!
Surprise me with a witty, unexpected roast that ties everything together. Think ultimate burn!
Do not provide short reasons. We want content.
"N/A" is not a rating, because nobody is saying N/A/10. That doesn't make sense. Always provide a numerical rating.

This is the exact format I want your response in, and only use this format:

Clothes: <rating>/10. <explanation here>.
Vibes: <rating>/10. <explanation here>.
Background: <rating>/10. <explanation here>.
Rizz: <rating>/10. <explanation here>.
Style: <rating>/10. <explanation here>.
Humor: <rating>/10. <explanation here>.
Caption: <caption to describe image>
Bonus points: <bonus points (max is 3)>/3. <reason for bonus points.>
Overall: <your overall thoughts. do NOT provide a rating, as I will sum them up.>
Improvement Tips: <tips they can use to improve. provide them on the same line, and do not point them on a new line.>
"""
