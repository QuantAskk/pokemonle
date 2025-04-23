from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
import utils.dataUtils as dataUtils
import utils.pokeUtils as pokeUtils
import json
import random
import time

app=Flask(__name__)
CORS(app)

PokeList=dataUtils.FileGetter('pokemon_full_list')
PokeList=pokeUtils.fliterPokeList(PokeList)
NameList=pokeUtils.OnlyNameGet(PokeList)
cache = pokeUtils.cache
print(NameList)

@app.route('/debug',methods=["GET"])
def debug():
    return "debug"

@app.route('/initget',methods=["GET"])
def initget():
    key = int(time.time())
    id = cache.get(key)
    if id != None:
        return jsonify(
            {"ans": key, "gen": pokeUtils.Gens.index(PokeList[id]["generation"])}
        )
    hard=request.args.get('difficulty', default=0, type=int)
    gen=request.args.get('gen', default=0, type=int)
    return jsonify(pokeUtils.getPokeByDf(PokeList,hard,gen))

@app.route('/nameget',methods=["GET"])
def nameget():
    return jsonify(NameList)

@app.route('/guess',methods=["GET"])
def guess():
    answer=request.args.get('answer', default=0, type=int)
    guess_id=request.args.get('guess', default=0, type=str)
    guess=pokeUtils.getPokeByName(PokeList,guess_id)
    if(answer==None or guess==None):
        return "guess name error"
    ans=pokeUtils.ComparePoke(PokeList,answer,guess)
    if ans == None:
        return "guess name error"
    return jsonify(ans)

@app.route('/getimage',methods=["GET"])
def getimage():
    pokemon=request.args.get('pokemon', default=0, type=str)
    Id=pokeUtils.getPokeByName(PokeList,pokemon)
    path=PokeList[Id]["index"]+'-'+PokeList[Id]["name"]
    print(path)
    return send_file(dataUtils.SrcPath()+f'/data/images/official/{path}.png',mimetype='image/jpeg')

@app.route('/getanswer',methods=["GET"])
def getanswer():
    id = request.args.get("pokemon", default=0, type=int)
    pokemon = cache.get(id)
    if pokemon == None:
        return "guess name error"
    answer=pokeUtils.getPokeByName(PokeList,NameList[pokemon])
    if(answer==None):
        return "guess name error"
    ans=pokeUtils.ComparePoke(PokeList,id,answer)
    return jsonify(ans)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9000)