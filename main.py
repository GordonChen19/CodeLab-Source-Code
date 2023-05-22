from Website import create_app
from flask_socketio import SocketIO,emit
import argparse

app=create_app()

# parser=argparse.ArgumentParser()
# parser.add_argument("host",nargs="?")
# parser.add_argument("port",nargs="?")

# parser.add_argument("-p","--portnum",default="5000")
# args = parser.parse_args()
# if not args.host:
#     args.host = "127.0.0.1"
# args.port = args.port or args.portnum
# print("Serving Sockets @ ws://%s:%s"%(args.host,args.port))


socketio=SocketIO(app)
if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
    
    
'''
chatgpt query
'''

def chatgpt(query):
    import openai

    openai.api_key = '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'
    messages = [ {"role": "system", "content": 
                "You are a intelligent assistant."} ]

    messages.append({"role": "system", "content": "You are a code assistant."})
    # messages.append({"role": "system", "content": "Give suggestions without directly writing any code"})
    if query:
        messages.append(
            {"role": "user", "content": query},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    return reply



'''
web Socket
'''

from Website.models import Chats,Room
from Website import db


@socketio.on('send_message')
def handle_message(message):
    user_message = message['content']

    generated_response=chatgpt(user_message)
    
    room_id=message['room_id']
    room=Room.query.filter_by(id=room_id).first()
    concept=room.room_concept
    new_chat=Chats(query=user_message,response=generated_response,room_id=message['room_id'])
    db.session.add(new_chat)
    db.session.commit()
    # Emit the response back to the client
    response = {'role': 'assistant', 'content': generated_response}
    emit('receive_message', response)
