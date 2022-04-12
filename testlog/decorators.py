from functools import wraps
from flask import redirect, session


def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'user_id' in session:
            print(session['user_id'])
            return a(*args,**kwargs)
            
        else:
            
            return redirect('login')
    return wrap