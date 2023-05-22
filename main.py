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
web Socket
'''

from Website.models import Room
from Website import db
from Website import chatgpt


@socketio.on('send_message')
def handle_message(message):
    # if message['type'] == 'hint':
    #     user_message="give a hint to solve the "+message['problem']+" Begin with hint"
    # elif message['type']=='solution':
    #     user_message="give the solution to the "+message['problem']+" Begin with solution"
    # else:
    user_message = message['content']

    generated_response=chatgpt(user_message)
    
    # Emit the response back to the client
    response = {'role': 'assistant', 'content': generated_response}
    emit('receive_message', response)
