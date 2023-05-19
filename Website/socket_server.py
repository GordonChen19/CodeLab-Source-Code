from flask import current_app, Flask,request
from flask_login import current_user
from .models import *
from flask_socketio import join_room,leave_room,SocketIO,disconnect,emit

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('codelab-socketio')

# def emit2(event,*args,**kwargs):
#     emit(event,*args,**kwargs)
class ActiveUsers:
    active_users_by_room={} 
    active_sids = set()

    @staticmethod 
    def get_by_room(room_id):
        return ActiveUsers.active_users_by_room.setdefault(room_id,[])
    #returns all sid of users in a given room
    
    @staticmethod
    def remove_user(sid):
        def remove_user_from_room(room_id):
            users_in_room=ActiveUsers.active_users_by_room[room_id] #{'sid':username,'sid':username...}
            index=[user['sid'] for user in users_in_room].index(sid)
            log.debug("%s has left the lab" % users_in_room[index]['username'] )
            del users_in_room[index]
        
        ActiveUsers.active_sids.remove(sid)
        return remove_user_from_room
        
    @staticmethod
    def add_to_room(room_id):
        current_user_sid = request.sid
        if current_user_sid in ActiveUsers.active_users_by_room[room_id]:
            raise Exception("User is already in lab")
        user=User.query.filter_by(id=current_user.id).first()
        user.sid=current_user_sid
        name=user.first_name
        db.session.commit()
       
        ActiveUsers.active_sids.add(current_user_sid)
        ActiveUsers.active_sids_by_room.setdefault(room_id,set()).add(current_user_sid)
        
        log.debug("%s has entered the lab!" %name)

    
socketio = SocketIO()
@socketio.on('connect')
def on_connect():
    print( "OK CONNECTED:",request.sid )
    
@socketio.on("disconnect")
def on_disconnect():
    user=User.query.filter_by(sid=socketio.sid).first()
    for room_id in ActiveUsers.active_users_by_room.keys():
        removeUser=ActiveUsers.remove_user(user.sid)
        removeUser(room_id)
        emit('user_left', {'username': user.first_name}, room=room_id)

@socketio.on('join')
def on_join(data):
    log.info("JOIN:%s - %s"%(data,request.sid))
    
    user = User.query.filter_by(id=current_user.id)
    
    username = data['username']
    room_id = data['room']
    join_room(room_id)
    
    ActiveUsers.add_to_room(room_id)
    emit('user_joined',{'username':username}, room=room_id)


@socketio.on('run')
def on_run(data):
    emit('user_run', {'username': data['username']}, room=data['room'])

@socketio.on('speak')
def on_speech(data):
    data['message'] = data['message'].replace("\"","&quot;").replace("'","&#39;")
    emit('user_speech', data, room=data['room_details']['room'])

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room_id = data['room']
    emit('user_left', {'username': username}, room=room_id)


@socketio.on('message')
def handle_message(message):
    print('received message.. ' + message)

def handle_change_message(data):
    room = data['room_details']['room']
    #retreiving from models.py
    current_text_lines=Room.query.filter_by(id=room).first().data
    current_text_lines = get_latest_prog(room).splitlines()
    start_line = data['start']['row']
    end_line = data['end']['row']
    try:
        end_line_text = current_text_lines[end_line]
    except IndexError:
        end_line_text = ""
    try:
        start_line_text = current_text_lines[start_line]
    except:
        start_line_text=""
    if (data['action'] == "insert"):
        print("INSERT?",data)
        line0 = data['lines'].pop(0)
        lhs = start_line_text[0:data['start']['column']]
        rhs = start_line_text[data['start']['column']:]
        if (not data['lines']):
            try:
                current_text_lines[start_line] = lhs + line0 + rhs
            except IndexError:
                current_text_lines.append(lhs + line0 + rhs)
        else:
            current_text_lines[start_line] = lhs + line0
            lineN = data['lines'].pop()
            data['lines'].append(lineN+rhs)
            current_text_lines[start_line + 1:start_line + 1] = data['lines']


    elif (data['action'] == "remove"):
        try:
            lhs = start_line_text[0:data['start']['column']]
        except:
            lhs = ""
        try:
            rhs = end_line_text[data['end']['column']:]
        except IndexError:
            rhs = ""
        new_line = lhs + rhs
        current_text_lines[start_line:end_line+1] = [new_line,]
    update_latest_prog(room,"\n".join(current_text_lines))

@socketio.on('on_editor_change')
@ActiveUsers.require_authentication
def handle_editor_change(message):
    socketio = current_app.extensions['socketio']
    room = message['room_details']['room']
    emit2('editor_change_event',message, room=room)
    handle_change_message(message)

