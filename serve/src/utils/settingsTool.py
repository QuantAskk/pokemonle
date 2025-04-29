# -*-coding: utf-8 -*-
# @Time    : 2025/4/24 10:41
# @Author  : TyranitarX
def setSettings(redis, room, data):
    redis.hset(room, "hardid", data["hardid"])
    redis.hset(room, "selectedGens", ",".join(map(str, data["selectedGens"])))
    redis.hset(room, "battleOpen", str(data["battleOpen"]))
    redis.hset(room, "shapeOpen", str(data["shapeOpen"]))
    redis.hset(room, "catchOpen", str(data["catchOpen"]))
    redis.hset(room, "showGenArrow", str(data["showGenArrow"]))
    redis.hset(room, "cheatOpen", str(data["cheatOpen"]))
    redis.hset(room, "reverseDisplay", str(data["reverseDisplay"]))
    redis.hset(room, "maxGuess", int(data["maxGuess"]))


def getRealSettings(redis, room):
    hardid = str(redis.hget(room, "hardid").decode('utf-8'))
    selectedGens = str(redis.hget(room, "selectedGens").decode('utf-8')).split(',')
    battleOpen = str(redis.hget(room, "battleOpen").decode('utf-8'))
    shapeOpen = str(redis.hget(room, "shapeOpen").decode('utf-8'))
    catchOpen = str(redis.hget(room, "catchOpen").decode('utf-8'))
    showGenArrow = str(redis.hget(room, "showGenArrow").decode('utf-8'))
    cheatOpen = str(redis.hget(room, "cheatOpen").decode('utf-8'))
    reverseDisplay = str(redis.hget(room, "reverseDisplay").decode('utf-8'))
    maxGuess = int(redis.hget(room, "maxGuess").decode('utf-8'))
    selectedGens = [True if item == "True" else False for item in selectedGens]
    battleOpen = True if battleOpen == "True" else False
    shapeOpen = True if shapeOpen == "True" else False
    catchOpen = True if catchOpen == "True" else False
    showGenArrow = True if showGenArrow == "True" else False
    cheatOpen = True if cheatOpen == "True" else False
    reverseDisplay = True if reverseDisplay == "True" else False
    return {
        "hardid": hardid,
        "selectedGens": selectedGens,
        "battleOpen": battleOpen,
        "shapeOpen": shapeOpen,
        "catchOpen": catchOpen,
        "showGenArrow": showGenArrow,
        "cheatOpen": cheatOpen,
        "reverseDisplay": reverseDisplay,
        "maxGuess": maxGuess,
    }
