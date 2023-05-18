from Website import create_app
from flask_socketio import SocketIO
import argparse

app=create_app()

parser=argparse.ArgumentParser()
parser.add_argument("host",nargs="?")
parser.add_argument("port",nargs="?")

parser.add_argument("-p","--portnum",default="5000")
args = parser.parse_args()
if not args.host:
    args.host = "127.0.0.1"
args.port = args.port or args.portnum
print("Serving Sockets @ ws://%s:%s"%(args.host,args.port))

socketio=SocketIO(app)
    
if __name__=='__main__':
    socketio.run(app,args.host,args.port,debug=True)