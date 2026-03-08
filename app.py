from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_brand_voice(brand):

    brand = brand.lower()

    if "nike" in brand:
        return "Energetic, motivational, performance-driven, youth focused"

    elif "apple" in brand:
        return "Premium, minimal, innovative, design-focused"

    elif "starbucks" in brand:
        return "Friendly, lifestyle-focused, warm, community-driven"

    elif "tesla" in brand:
        return "Futuristic, bold, innovative, tech-driven"

    elif "amazon" in brand:
        return "Convenient, customer-focused, practical, fast-paced"

    else:
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    brand = data["brand"]
    industry = data["industry"]
    objective = data["objective"]
    product = data["product"]

    # -------- BRAND VOICE ANALYSIS --------

    auto_voice = detect_brand_voice(brand)

    if auto_voice:
        brand_voice = auto_voice

    else:

        prompt_voice = f"""
Analyze the brand voice for the following brand.

Brand: {brand}
Industry: {industry}
Product: {product}

Return exactly 4 short insights:

1. Brand Tone
2. Target Audience
3. Content Themes
4. Communication Style

Keep each insight concise (1 sentence).
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt_voice}]
        )

        brand_voice = response.choices[0].message.content

    # -------- TWEET GENERATION --------

    tweet_prompt = f"""
You are a social media marketing expert.

Brand voice:
{brand_voice}

Campaign objective: {objective}

Generate 10 engaging Twitter posts with emojis and hashtags.

Rules:
- Make them short and catchy
- Match the brand voice
- Include relevant emojis
- Include 1–2 hashtags
- Mix promotional, witty and engaging styles
"""

    tweet_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": tweet_prompt}]
    )

    tweets = tweet_response.choices[0].message.content

    return jsonify({
        "voice": brand_voice,
        "tweets": tweets
    })


if __name__ == "__main__":
    app.run(debug=True)