'''
chatgpt query
'''

import openai
import os
from dotenv import load_dotenv
load_dotenv()
CHATGPT_SECRET_KEY = os.getenv("CHATGPT_SECRET_KEY")

def chatgpt(query):

    openai.api_key = CHATGPT_SECRET_KEY
    messages = [ {"role": "system", "content": 
                "You are an intelligent assistant."} ]

    messages.append({"role": "system", "content": "You are a code assistant."})
    # messages.append({"role": "system", "content": "Give suggestions without directly writing any code"})
    if query:
        messages.append(
            {"role": "user", "content": query}
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=200
        )
    reply = chat.choices[0].message.content
    return reply
