import os
from openai import OpenAI
import sqlite3
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file
DB_FILE = "cache.db" # Database file for caching responses
# create a trable  
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                prompt TEXT PRIMARY KEY,
                response TEXT
            )
        ''')

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

# Get response from cache if available
def get_cached_response(prompt: str) -> str | None:
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT response FROM cache WHERE prompt = ?", (prompt,))
        row = cursor.fetchone()
        return row[0] if row else None

# Save response to cache
def save_to_cache(prompt: str, response: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT OR REPLACE INTO cache (prompt, response) VALUES (?, ?)", (prompt, response))

def get_quantum_insight(prompt: str) -> str:
    init_db()
    
    cached = get_cached_response(prompt)
    if cached:
        return f"(cached)\n{cached}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a quantum research assistant that answers questions concisely."},
                {"role": "user", "content": prompt}
                
            ],
            max_tokens=4000,
            temperature=0.7,
            top_p=1,
        )
        content = response.choices[0].message.content
        reply = content.strip() if content is not None else ""
        save_to_cache(prompt, reply)
        return reply
    except Exception as e:
        return f"Error generating response: {e}"
    
    

  