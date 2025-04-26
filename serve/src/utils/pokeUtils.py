import random
import re

import utils.dataUtils as dataUtils

Types = ["一般", "火", "水", "电", "草", "冰", "格斗", "毒", "地面", "飞行", "超能力", "虫", "岩石", "幽灵", "龙", "恶",
         "钢", "妖精", "无"]
Gens = ["第一世代", "第二世代", "第三世代", "第四世代", "第五世代", "第六世代", "第七世代", "第八世代", "第九世代"]
Labels = [
    {
        "id": "Beginer",
        "name": "最初的伙伴",
        "weight": 30
    },
    {
        "id": "Dream",
        "name": "幻之宝可梦",
        "weight": 20
    },
    {
        "id": "Legend",
        "name": "传说的宝可梦",
        "weight": 30
    },
    {
        "id": "MaybeGod",
        "name": "大器晚成的宝可梦",
        "weight": 20
    },
    {
        "id": "Mouse",
        "name": "电气鼠宝可梦",
        "weight": 10
    },
    {
        "id": "Paradox",
        "name": "悖谬宝可梦",
        "weight": 10
    },
    {
        "id": "Stone",
        "name": "化石宝可梦",
        "weight": 5
    },
    {
        "id": "Yibu",
        "name": "伊布",
        "weight": 10
    },
    {
        "id": "ZMonster",
        "name": "究极异兽",
        "weight": 5
    },
    {
        "id": "Zskill",
        "name": "拥有专属Z招式",
        "weight": 5
    },
    {
        "id": "Mega",
        "name": "有Mega进化",
        "weight": 20
    },
    {
        "id": "Gmax",
        "name": "有超极巨化",
        "weight": 15
    }
]


def fliterPokeList(PokeList):
    i = 0
    newPokeList = []
    las = ""
    for x in PokeList:
        if (x["index"] != las):
            newPokeList.append(x)
        las = x["index"]
    return newPokeList


def OnlyNameGet(PokeList):
    NameList = []
    for x in PokeList:
        NameList.append(x["name"])
    return NameList


def getPokeByDf(PokeList, hard, ngen):
    ans = None
    while True:
        ans = None
        if (hard == 0):
            ans = random.randint(1, 1025) - 1
        else:
            Group = []
            if (random.random() < 0.25):
                Group = dataUtils.LabelGetter("hot")
            else:
                weights = [item['weight'] for item in Labels]
                names = [item['id'] for item in Labels]
                result = random.choices(names, weights=weights, k=1)
                Group = dataUtils.LabelGetter(result[0])
            ans = getPokeByName(PokeList, random.choice(Group))
        if (ans != None):
            if (ngen == 0):
                break
            gen = PokeList[ans]["generation"]
            if (ngen <= 9):
                if (Gens.index(gen) == ngen - 1):
                    break
            else:
                idx = Gens.index(gen)
                if ((((ngen - 10) >> idx) & 1) == 1):
                    break
    return ans


def getPokeByName(PokeList, name):
    i = 0
    for x in PokeList:
        if (x["name"] == name):
            return i
        i = i + 1
    return None


def TypeGet(Info):
    type = Info["forms"][0]["types"]
    t1 = type[0]
    if (len(type) == 1):
        t2 = "无"
    else:
        t2 = type[1]
    # x1=Types.index(t1)
    # x2=Types.index(t2)
    # if(x1>x2):
    #     t1,t2=t2,t1
    return [t1, t2]


def PowerSumGet(Info):
    state = Info["stats"][0]["data"]
    sum = 0
    for x in state.values():
        sum += int(x)
    return sum


def AbilityGet(Info):
    ability = Info["forms"][0]["ability"]
    ans = []
    for x in ability:
        ans.append(x["name"])
    return ans


def EvolutionGet(Info):
    EvolutionChain = Info["evolution_chains"][0]
    own = {}
    i = 0
    for Evolution in EvolutionChain:
        if (Evolution["name"] == Info["name"]):
            own = Evolution
            break
    if (own["stage"] == "不进化" or own["stage"] == "未进化" or own["stage"] == "幼年"):
        own["stage"] = "未进化/不进化"
    return own["stage"], own["text"]


def APTypeGet(Info):
    At = int(Info["stats"][0]["data"]["attack"])
    Pt = int(Info["stats"][0]["data"]["sp_attack"])
    Ad = int(Info["stats"][0]["data"]["defense"])
    Pd = int(Info["stats"][0]["data"]["sp_defense"])
    As = ""
    Ds = ""
    if (At == Pt):
        As = "物攻=特攻"
    elif (At > Pt):
        As = "物攻>特攻"
    elif (At < Pt):
        As = "物攻<特攻"

    if (Ad == Pd):
        Ds = "物防=特防"
    elif (Ad > Pd):
        Ds = "物防>特防"
    elif (Ad < Pd):
        Ds = "物防<特防"

    return As, Ds


def EggGroupGet(Info):
    return Info["forms"][0]["egg_groups"]


def checkLevelEvo(s):
    pattern = r'^等级.+以上.*$'
    return bool(re.fullmatch(pattern, s))


def isLabel(Info, Label):
    for x in Info["forms"]:
        if (Label in x["name"]):
            return True
    return False


def checkLabel(Info, Label):
    Group = dataUtils.LabelGetter(Label)
    return (Info["name"] in Group)


def getLabel(Info):
    Label = []
    if (isLabel(Info, "阿罗拉")):
        Label.append("有阿罗拉地区形态")
    if (isLabel(Info, "洗翠")):
        Label.append("有洗翠地区形态")
    if (isLabel(Info, "帕底亚")):
        Label.append("有帕底亚地区形态")
    if (isLabel(Info, "伽勒尔")):
        Label.append("有伽勒尔地区形态")
    for x in Labels:
        if (checkLabel(Info, x["id"])):
            Label.append(x["name"])
    return Label


def ComparePoke(PokeList, Id1, Id2):
    Path1 = PokeList[Id1]["index"] + '-' + PokeList[Id1]["name"]
    Path2 = PokeList[Id2]["index"] + '-' + PokeList[Id2]["name"]
    Info1 = dataUtils.PokeGetter(Path1)
    Info2 = dataUtils.PokeGetter(Path2)

    ans = {"name": PokeList[Id2]["name"]}
    if (PokeList[Id2]["name"] == PokeList[Id1]["name"]):
        ans["answer"] = "True"
    else:
        ans["answer"] = "False"
        
    ans["index"] = PokeList[Id2]["index"]

    # 属性检查
    types = []
    Type1 = TypeGet(Info1)
    Type2 = TypeGet(Info2)

    s1 = (Type1[0] == Type2[0]) + (Type1[1] == Type2[1])
    s2 = (Type1[0] == Type2[1]) + (Type1[1] == Type2[0])
    if (s2 > s1):
        Type1[0], Type1[1] = Type1[1], Type1[0]

    for i in range(0, 2):
        if (Type1[i] == Type2[i]):
            types.append({"key": Type2[i], "value": "True"})
        else:
            types.append({"key": Type2[i], "value": "False"})
    ans["type"] = types

    # 种族值检查
    Pow1 = PowerSumGet(Info1)
    Pow2 = PowerSumGet(Info2)
    if (Pow2 == Pow1):
        ans["pow"] = {"key": Pow2, "value": "equiv"}
    elif (Pow2 > Pow1):
        ans["pow"] = {"key": Pow2, "value": "low"}
    else:
        ans["pow"] = {"key": Pow2, "value": "high"}
    if (Pow1 == Pow2):
        ans["pow"]["dis"] = "equiv"
    if (abs(Pow1 - Pow2) <= 50):
        ans["pow"]["dis"] = "near"
    else:
        ans["pow"]["dis"] = "far"

    # 速度检查
    Spd1 = int(Info1["stats"][0]["data"]["speed"])
    Spd2 = int(Info2["stats"][0]["data"]["speed"])
    if (Spd2 == Spd1):
        ans["speed"] = {"key": Spd2, "value": "equiv"}
    elif (Spd2 > Spd1):
        ans["speed"] = {"key": Spd2, "value": "low"}
    else:
        ans["speed"] = {"key": Spd2, "value": "high"}
    if (Spd1 == Spd2):
        ans["speed"]["dis"] = "equiv"
    if (abs(Spd1 - Spd2) <= 10):
        ans["speed"]["dis"] = "near"
    else:
        ans["speed"]["dis"] = "far"

    # 攻防检查
    At1, Df1 = APTypeGet(Info1)
    At2, Df2 = APTypeGet(Info2)
    if (At1 == At2):
        ans["attack"] = {"key": At2, "value": "True"}
    else:
        ans["attack"] = {"key": At2, "value": "False"}
    if (Df1 == Df2):
        ans["defense"] = {"key": Df2, "value": "True"}
    else:
        ans["defense"] = {"key": Df2, "value": "False"}

    # 蛋组/捕获率检查
    EggGroup1 = EggGroupGet(Info1)
    EggGroup2 = EggGroupGet(Info2)
    abt = []
    for x in EggGroup2:
        flag = False
        for y in EggGroup1:
            if (x == y):
                flag = True
                break
        if (flag):
            abt.append({"key": x, "value": "True"})
        else:
            abt.append({"key": x, "value": "False"})
    ans["egg"] = abt

    CatRate1 = int(Info1["forms"][0]["catch_rate"]["number"])
    CatRate2 = int(Info2["forms"][0]["catch_rate"]["number"])
    if (CatRate2 == CatRate1):
        ans["catrate"] = {"key": CatRate2, "value": "equiv"}
    elif (CatRate2 > CatRate1):
        ans["catrate"] = {"key": CatRate2, "value": "low"}
    else:
        ans["catrate"] = {"key": CatRate2, "value": "high"}

    # 外形检查
    Shape1 = Info1["forms"][0]["shape"]
    Shape2 = Info2["forms"][0]["shape"]
    Col1 = Info1["forms"][0]["color"]
    Col2 = Info2["forms"][0]["color"]
    if (Shape1 == Shape2):
        ans["shape"] = {"key": Shape2, "value": "True"}
    else:
        ans["shape"] = {"key": Shape2, "value": "False"}
    if (Col1 == Col2):
        ans["col"] = {"key": Col2, "value": "True"}
    else:
        ans["col"] = {"key": Col2, "value": "False"}

    # 世代检查
    Gen1 = Gens.index(PokeList[Id1]["generation"])
    Gen2 = Gens.index(PokeList[Id2]["generation"])
    if (Gen1 == Gen2):
        ans["gen"] = {"key": PokeList[Id2]["generation"], "value": "equiv"}
    elif (Gen1 < Gen2):
        ans["gen"] = {"key": PokeList[Id2]["generation"], "value": "low"}
    else:
        ans["gen"] = {"key": PokeList[Id2]["generation"], "value": "high"}
    if (Gen1 == Gen2):
        ans["gen"]["dis"] = "equiv"
    if (abs(Gen1 - Gen2) <= 1):
        ans["gen"]["dis"] = "near"
    else:
        ans["gen"]["dis"] = "far"

    # 特性信息
    Ability1 = AbilityGet(Info1)
    Ability2 = AbilityGet(Info2)
    abt = []
    for x in Ability2:
        flag = False
        for y in Ability1:
            if (x == y):
                flag = True
                break
        if (flag):
            abt.append({"key": x, "value": "True"})
        else:
            abt.append({"key": x, "value": "False"})
    ans["ability"] = abt

    # 进化信息
    Stage1, Evo1 = EvolutionGet(Info1)
    Stage2, Evo2 = EvolutionGet(Info2)
    if (Stage1 == Stage2):
        ans["stage"] = {"key": Stage2, "value": "True"}
    else:
        ans["stage"] = {"key": Stage2, "value": "False"}

    if (Evo1 == Evo2):
        ans["evo"] = {"key": Evo2, "value": "equiv"}
    elif (Evo1 == None or Evo2 == None):
        ans["evo"] = {"key": Evo2, "value": "far"}
    elif ("使用" in Evo1 and "使用" in Evo2):
        ans["evo"] = {"key": Evo2, "value": "near"}
    elif ("来到" in Evo1 and "来到" in Evo2):
        ans["evo"] = {"key": Evo2, "value": "near"}
    elif (checkLevelEvo(Evo1) and checkLevelEvo(Evo2)):
        ans["evo"] = {"key": Evo2, "value": "near"}
    elif ("亲密度" in Evo1 and "亲密度" in Evo2):
        ans["evo"] = {"key": Evo2, "value": "near"}
    else:
        ans["evo"] = {"key": Evo2, "value": "far"}

    Label1 = getLabel(Info1)
    Label2 = getLabel(Info2)
    Label = []
    
    # 检查两只宝可梦是否都有形态变化
    form_labels_1 = [l for l in Label1 if "形态" in l or any(region in l for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])]
    form_labels_2 = [l for l in Label2 if "形态" in l or any(region in l for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])]
    
    has_form_1 = len(form_labels_1) > 0
    has_form_2 = len(form_labels_2) > 0
    
    for x in Label2:
        exact_match = x in Label1
        
        # 检查是否是形态标签
        is_form_label = "形态" in x or any(region in x for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])
        
        if exact_match:
            # 完全匹配，前端会渲染为绿色
            Label.append({"key": x, "value": "True"})
        else:
            # 不完全匹配，检查是否是形态标签且双方都有形态变化
            if is_form_label and has_form_1 and has_form_2:
                Label.append({"key": x, "value": "False", "col": "warning"})
            else:
                # 其他情况
                Label.append({"key": x, "value": "False"})
    
    ans["label"] = Label
    
    return ans

# PokeList=dataUtils.FileGetter('pokemon_full_list')
# PokeList=fliterPokeList(PokeList)
# print(OnlyNameGet(PokeList))
# a=getPokeByName(PokeList,"妙蛙草")
# b=getPokeByName(PokeList,"妙蛙花")
# print(ComparePoke(PokeList,a,b))

# Info=dataUtils.PokeGetter("0004-小火龙")
# print(TypeGet(Info))

# Info=dataUtils.PokeGetter("1024-太乐巴戈斯")
# print(PowerSumGet(Info))

# for i in range(10):
#     print(PokeList[getPokeByDf(PokeList,0,0)]["name"])
