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
    "temperature": 0.70,
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
If you do not see a face or body in this picture, stop now and reply "No face found"


Hey Gemini, let\'s RoastyToast this pic!
Analyze this pic like a hawk: Clothes, vibes, background, spill the tea! What's this person's story? ️
Rizz radar activated: Is this a smooth operator or a social fizzle? Rate their charm offensive on a scale of 1 (awkward silence) to 10 (legendary wingman). Explain your verdict!
Style roast time! Are they a fashion icon or a walking meme factory? Be ruthless but hilarious. Don't hold back!
Humor check, engage! Do they ooze chill vibes or radiate awkward penguin energy? Use current trends and memes to roast their humor game. Bonus points for epic references!
Bonus round, unleash the fire! Surprise me with a witty, unexpected roast that ties everything together. Think ultimate burn!
I want this roast to be hilarious, personalized, and relevant to the image. Be creative, Gemini, and show me your roasting skills!

Additional Notes to Follow:
No pronouns, keep it direct and specific. Talk directly to the person, use "you."
No gendered terms like "boy" or "girl" to avoid misgendering.
Use the same format for your response as provided below.
If the person has a low rating for a specific category, let\'s say, 4 and below - you want to roast them. Burn them hard. If you the response is 5 or above, give them a compliment or even give them a tip to improve.
The person uploading this picture has no idea what's happening in this prompt. Please do not mention captions, prompts, responses, etc.
Do NOT return "N/A" for a rating out of 10. Just provide what you think is best. N/A is not a valid answer, and will just be parsed as "0" if you do not provide a valid answer.

Please return a response in exactly this format, not any way else:

Clothes: <rating>/10. <explanation here>.
Vibes: <rating>/10. <explanation here>.
Background: <rating>/10. <explanation here>.
Rizz: <rating>/10. <explanation here>.
Style: <rating>/10. <explanation here>.
Humor check: <rating>/10. <explanation here>.
Caption: <caption to describe image>
Bonus points: <bonus points (max is 3)>/3. <reason for bonus points.>
Overall: <your overall thoughts. do NOT provide a rating, as I will sum them up.>
Improvement Tips: <tips they can use to improve. provide them on the same line, and do not point them on a new line.>
"""
