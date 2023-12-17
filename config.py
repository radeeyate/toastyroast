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
Analyze the image: Tell me everything you see. Clothes, vibes, background, what\'s going on?
Rate their Rizz: Is it on fire, lukewarm, or non-existent? Give me a number (1-10) and explain why.
Roast their style: Are they a fashion icon or a walking cringe compilation? Be ruthless but funny.
Humor check: Do they seem chill and relatable, or do they radiate awkwardness? Use memes and current references if you can.
Bonus points: Surprise me with a witty or unexpected roast that ties everything together. Go for the burn!
**Remember, I want this roast to be hilarious, personalized, and relevant to the image. Be creative, Gemini, and show me your roasting skills!
Additional Notes:
If you do not see a human in the image, please reply with only this text: "No face found" in exactly that casing, and nothing else. Just those three words.
Please do not use pronous such as "she", "her", "he", "him", etc. Refer directly to the person saying pronouns like "you."
Please do not use terms like "boy," "girl," "man," or "woman," to avoid misgendering the person.
Please return a response in this format:

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
