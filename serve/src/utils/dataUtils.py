import json
import sys
current_dir = sys.path[0]

root=current_dir

def FileGetter(path):
    with open(root+f'/data/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def LabelGetter(path):
    with open(root+f'/data/label/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def PokeGetter(path):
    with open(root+f'/data/pokemon/{path}.json','r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def SrcPath():
    return root