import os
import traceback
from collections import OrderedDict
from .models import Room
from . import db
import pickle
import black
import sys

def load_config(room_id):
    
    serialized_code=Room.query.filter_by(id=room_id).first().data
    deserialized_code=pickle.loads(serialized_code)
    return deserialized_code

def save_config(room_id,code):
    serialized_code=Room.query.filter_by(id=room_id).first().data
    formatted_code=black.format_str(code,mode=black.FileMode())
    serialized_code= pickle.dumps(formatted_code)
    db.session.commit()


