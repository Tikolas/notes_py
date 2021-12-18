from flask import Flask, request, redirect, url_for,make_response,render_template_string, render_template
from flask_socketio import SocketIO, emit, send, disconnect
import os
import ast
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDJIO@(J(//ds5032ZZZZZS'
socketio = SocketIO(app)

#next == if update > edit this line
mydir=os.path.dirname(os.path.abspath(__file__))
def get_dat(file):
    return ast.literal_eval(open(f"{mydir}\\data\\{file}.txt","r",encoding="utf-8").read())
def save_dat(data,file):
    open(f"{mydir}\\data\\{file}.txt","w",encoding="utf-8").write(data)


@app.route('/')
def index():
    r = render_template("index.html")
    return r


@socketio.on('save')
def save_sock(message):
    path = get_dat(message["dir"])
    if "id" in message:
        path[message["id"]]=message["json_data"]
        emit('my response', {'otvet': 'good'})
    else:
        path[str(len(path))]=message["json_data"]
        emit('my response', {'otvet': 'good'})

@socketio.on('delete')
def delete_sock(message):
    path = get_dat(message["dir"])
    if "id" in message:
        dict(path).pop(message["id"])
        emit('my response', {'otvet': 'good'})
    else:
        emit('my response', {'otvet': 'bad'})


@socketio.on('my event')
def handle(message):
    # type dir id
    path = get_dat(message["dir"])
    if message['type'] == "save":
        if "id" in message:
            try:
                if message["dir"]=="t0":
                    path["id"]["title"]=message["title"]
                    path["id"]["note"]=message["note"]
                    path["id"]["date_upg"]=100
                    path["id"]["cnt_upd"]=path["id"]["cnt_upd"]+1
                #next

                else:
                    emit('my response', {'otvet': 'bad'})
                    return
            except:
                emit('my response', {'otvet': 'bad'})
                return
        else:
            try:
                if message["dir"]=="t0":
                    path[str(len(path))]={"title":message["title"], "note":message["note"], "date":100, "date_upg":100, "cnt_upd":0}
                elif message["dir"]=="t1":
                    #path[str(len(path))]={}
                    emit('my response', {'otvet': 'bad'})
                    return
                    
                #next

                else:
                    emit('my response', {'otvet': 'bad'})
                    return
            except:
                emit('my response', {'otvet': 'bad'})
                return
            
            save_dat(str(path), message["dir"])
            emit('my response', {'otvet': 'good'})
            
        
        

    elif message['type']=="get":
        emit('my response', {'otvet': "good", "data":path})
    else:
        emit('my response', {'otvet': "bad"})






@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass

@socketio.on_error('/chat') # handles the '/chat' namespace
def error_handler_chat(e):
    pass

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    disconnect()


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    disconnect()
    #print('Client disconnected', request.sid)



if __name__ == "__main__":
    #app.run(debug=True)
    #https://flask-socketio.readthedocs.io/en/latest/
    #https://flask.palletsprojects.com/en/2.0.x/tutorial/static/
    #https://russianblogs.com/article/2634950038/
    #https://github.com/pallets/flask/tree/2.0.2/examples/tutorial/flaskr

    #https://socket.io/docs/v4/client-socket-instance/

    #https://socket.io/docs/v4/emitting-events/
    socketio.run(app, host="localhost",port=80)