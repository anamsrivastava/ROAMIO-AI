from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# GROQ API KEY — paste your gsk_... key here
GROQ_API_KEY = "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"

# Using Groq's OpenAI-compatible endpoint
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        # Get form data
        mood = request.form.get('mood')
        energy = request.form.get('energy')
        budget = request.form.get('budget')
        time = request.form.get('time')
        weather = request.form.get('weather')
        priority = request.form.get('priority')

        # AI PROMPT
        prompt = f"""
You are PulsePlan AI — a smart student planner.

User Details:
Mood: {mood}
Energy: {energy}
Budget: {budget}
Time: {time}
Weather: {weather}
Priority: {priority}

Create a DAILY PLAN.

FORMAT:

PRODUCTIVE:
- ...

FUN:
- ...

SELF CARE:
- ...

FOOD:
- ...

Keep it short, practical, and student-friendly.
"""

        try:
            # CALL AI
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq model
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
