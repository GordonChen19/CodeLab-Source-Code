'''
chatgpt query
'''

import openai

def chatgpt(query):

    openai.api_key = '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'
    messages = [ {"role": "system", "content": 
                "You are a intelligent assistant."} ]

    messages.append({"role": "system", "content": "You are a code assistant."})
    # messages.append({"role": "system", "content": "Give suggestions without directly writing any code"})
    if query:
        messages.append(
            {"role": "user", "content": query}
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    return reply
