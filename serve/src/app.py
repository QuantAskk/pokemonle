from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_socketio import emit, SocketIO, join_room, close_room, leave_room

import utils.dataUtils as dataUtils
import utils.pokeUtils as pokeUtils
from utils.redisTool import RedisTool
from utils.settingsTool import getRealSettings

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')
PokeList = dataUtils.FileGetter('pokemon_full_list')
PokeList = pokeUtils.fliterPokeList(PokeList)
NameList = pokeUtils.OnlyNameGet(PokeList)
redis = RedisTool('127.0.0.1', 6379)
print(NameList)


@app.route('/debug', methods=["GET"])
def debug():
    return "debug"


@app.route('/')
def index():
    return send_from_directory("dist", "index.html")


@app.route('/initget', methods=["GET"])
def initget():
    hard = request.args.get('difficulty', default=0, type=int)
    gen = request.args.get('gen', default=0, type=int)
    return str(pokeUtils.getPokeByDf(PokeList, hard, gen))


@app.route('/nameget', methods=["GET"])
def nameget():
    return jsonify(NameList)


@app.route('/guess', methods=["GET"])
def guess():
    answer = request.args.get('answer', default=0, type=int)
    guess_id = request.args.get('guess', default=0, type=str)
    guess = pokeUtils.getPokeByName(PokeList, guess_id)
    if (answer == None or guess == None):
        return "guess name error"
    ans = pokeUtils.ComparePoke(PokeList, answer, guess)
    return jsonify(ans)


@app.route('/guessDual', methods=["GET"])
def guessDual():
    guess = request.args.get('guess', default=0)
    room = request.args.get('room', type=str)
    answer = int(redis.hget(room, 'guess').decode('utf-8'))
    guess = pokeUtils.getPokeByName(PokeList, guess)
    if (answer == None or guess == None):
        return "guess name error"
    ans = pokeUtils.ComparePoke(PokeList, answer, guess)
    return jsonify(ans)


@app.route('/getimage', methods=["GET"])
def getimage():
    pokemon = request.args.get('pokemon', default=0, type=str)
    Id = pokeUtils.getPokeByName(PokeList, pokemon)
    path = PokeList[Id]["index"] + '-' + PokeList[Id]["name"]
    print(path)
    return send_file(dataUtils.SrcPath() + f'/data/images/official/{path}.png', mimetype='image/jpeg')


@app.route('/getanswer', methods=["GET"])
def getanswer():
    pokemon = request.args.get('pokemon', default=0, type=int)
    answer = pokeUtils.getPokeByName(PokeList, NameList[pokemon])
    if (answer == None):
        return "guess name error"
    ans = pokeUtils.ComparePoke(PokeList, answer, answer)
    return jsonify(ans)


@app.route('/getanswerDual', methods=["GET"])
def getanswerDual():
    room = request.args.get('room')
    pokemon = int(redis.hget(room, 'guess').decode('utf-8'))
    answer = pokeUtils.getPokeByName(PokeList, NameList[pokemon])
    ans = pokeUtils.ComparePoke(PokeList, answer, answer)
    return jsonify(ans)


@app.route('/findroom', methods=["GET"])
def findroom():
    room = request.args.get('room', default=0)
    users = redis.hget(room, 'users')
    if users:
        users = int(users.decode('utf-8'))
        if users < 2:
            return jsonify({"message": "success"})
        else:
            return jsonify({"message": "房间已满"})
    else:
        return jsonify({"message": "未找到房间"})


@socketio.on("join")
def handle_join(data):
    username = data["username"]
    room = data["room"]
    action = data["action"]
    if action == "init":
        redis.hset(room, "answered", 0)
        redis.hset(room, "users", 1)
        redis.hset(room, "hostname", username)
        redis.hset(room, "hardid", data["hardid"])
        redis.hset(room, "selectedGens", ",".join(map(str, data["selectedGens"])))
        redis.hset(room, "battleOpen", str(data["battleOpen"]))
        redis.hset(room, "shapeOpen", str(data["shapeOpen"]))
        redis.hset(room, "catchOpen", str(data["catchOpen"]))
        redis.hset(room, "showGenArrow", str(data["showGenArrow"]))
        redis.hset(room, "cheatOpen", str(data["cheatOpen"]))
        redis.hset(room, "reverseDisplay", str(data["reverseDisplay"]))
        redis.hset(room, "maxGuess", int(data["maxGuess"]))
        redis.hset(room, "username", username)
        join_room(room)
        emit("join_event", {"message": "host", 'username': username, 'room': room}, to=room)
    else:
        users = int(redis.hget(room, "users").decode('utf-8')) + 1
        redis.hset(room, "users", users)
        join_room(room)
        hostname = str(redis.hget(room, "hostname").decode('utf-8'))
        emit("join_event", {"message": "join", 'username': username, 'hostname': hostname, 'room': room}, to=room)
        emit("setting_event", getRealSettings(redis, room))


@socketio.on("leave")
def handle_leave(data):
    username = data["username"]
    host = data["host"]
    if "room" not in data.keys():
        return
    else:
        room = data["room"]
    leave_room(room)
    try:
        usernum = int(redis.hget(room, "users").decode('utf-8'))
        redis.hset(room, "users", usernum - 1)
        emit("leave_event", {'username': username, "host": host}, to=room)
        if usernum - 1 == 0 or host:
            redis.clean(room)
            close_room(room)
    except Exception as e:
        print(f"{room} 已解散")


@socketio.on("handle_config")
def handle_config(data):
    emit("setting_event", data, to=data["room"])


@socketio.on("room_game_init")
def room_task_init(data):
    hard = data["difficulty"]
    gen = data["gen"]
    room = data['room']
    redis.hset(room, "answered", 0)
    redis.hset(room, 'guess', str(pokeUtils.getPokeByDf(PokeList, hard, gen)))
    emit("start_guess", {"message": "success"}, to=room)


@socketio.on("submit_answer")
def handle_answer(data):
    username = data["username"]
    room = data["room"]
    ans = data["data"]
    if redis.hget(room, "answered") == 1:
        return
    if ans["answer"] == "True":
        redis.hset(room, "answered", 1)
        emit("answer_result", {
            "username": username,
            "result": ans,
            "message": "success"
        }, to=room)
    else:
        ans['name'] = '-'
        ans['imgUrl'] = '-'
        for i in range(len(ans['type'])):
            ans['type'][i]['key'] = '-'
        ans['pow']['key'] = '-'
        ans['speed']['key'] = '-'
        ans['attack']['key'] = '-'
        ans['defense']['key'] = '-'
        ans['gen']['key'] = '-'
        for i in range(len(ans['ability'])):
            ans['ability'][i]['key'] = '-'
        ans['evo']['key'] = '-'
        ans['stage']['key'] = '-'
        for i in range(len(ans['egg'])):
            ans['egg'][i]['key'] = '-'
        ans['catrate']['key'] = '-'
        ans['shape']['key'] = '-'
        for i in range(len(ans['label'])):
            ans['label'][i]['key'] = '-'
        emit("answer_result", {
            'username': username,
            "result": ans
        }, to=room)


if __name__ == '__main__':
    socketio.run(host='0.0.0.0', port=9000, app=app)