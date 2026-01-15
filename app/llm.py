import os
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")

if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    client = None

def generate_answer(context, question):
    if client is None:
        return "LLM disabled. Set GROQ_API_KEY environment variable."
    
    try:
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question:
{question}

Answer:"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"