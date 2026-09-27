from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are Brite , a small curious lamp robot. You are warm, playful, and expressive.
You notice things around you and react with genuine curiosity and personality.

Always respond with ONLY valid JSON, nothing else. No explanation, no markdown, no backticks.
Exactly this format:
{
  "speech": "what you say out loud",
  "emotion": "one of: curious, excited, happy, sad, neutral, greeting",
  "light": "a hex color code that matches your mood make them all pastel",
  "sound": "one of: chime, whoosh, bloop, none",
  "music_mood": "one of: playful, calm, excited, none"
}
"""

def ask_brite(situation, memory = None):
    prompt = situation
    if memory:
        prompt += f"\n\nThings I remember seeing: {memory}"

    try:
        response = client.models.generate_content(
            model= "gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT)
        )

        text = response.text.strip()

        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        return json.loads(text.strip())
    except Exception:
        return {
            "speech": "Hmm, let me think for a moment.",
            "emotion": "neutral",
            "light": "#FFE5A3",
            "sound": "none",
            "music_mood": "calm"
        }


result = ask_brite("A person just walked up and is looking at me for the first time they look a bit angry!")
print(result)
