import random
import requests
import json
import re
import time

PicNum = {3282995855:0}
#gid - message
Remessages = {}

#来点好东西
def NicePic():
    apiurl = 'https://api.lolicon.app/setu/v2?r18=1'
    m = requests.get(apiurl).json()
    n = json.dumps(m) 
    getapi = re.search(r'"original": "(.*?)"', n).group(1) #getapi
    tags = str(m['data'][0]['tags'])
    return tags,getapi

#召唤计数器
def Remory(QQNum):
    PicNum[QQNum] = int(PicNum[QQNum]) + 1

#查询召唤次数
def QueryPicNum(QQNum):
    if QQNum == 0000:
        NumStr = str(PicNum)
        return NumStr
    else:
        try:
            Num = PicNum[QQNum]
            NumStr = "{}的召唤次数为{}次".format(QQNum,Num)
        except:
            NumStr = "{}的召唤次数为0次".format(QQNum)
        return NumStr

#聊天记录记载
def MessageRemory(gid,uid,message):
    if gid not in Remessages:
        Remessages[gid] = []
    Remessages[gid].append((uid, message))
    Remessages[gid] = Remessages[gid][-10:]

#聊天记录查询
def DeWithDraw(gid):
    if gid in Remessages:
        messages = []
        for uid, message in Remessages[gid]:
            messages.append(f"UID: {uid} - Message: {message}")
        Log = "\n".join(messages)
        DeWithDrawLog = (f"Messages for gid {gid}:\n{Log}")
        return DeWithDrawLog
    else:
        DeWithDrawLog = (f"No messages found for gid {gid}")
        return DeWithDrawLog
    
#来份涩图
def Picture():
    apiurl = 'https://api.lolicon.app/setu/v2'
    m = requests.get(apiurl).json()
    n = json.dumps(m) 
    getapi = re.search(r'"original": "(.*?)"', n).group(1)
    return getapi

