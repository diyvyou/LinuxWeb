import random
import requests
import json
import re
import time


member = {}
Scout, Listen, Inspiration, Stealth, Shooting, Fighting = 0,0,0,0,0,0
#侦察，聆听，灵感，潜行，射击，格斗

#R点
def Roll(message):
    total_sum = 0
    NumList = {}
    match = re.search(r"(\d+)D(\d+)", message)
    D1 , D2 = int(match.group(1)) , int(match.group(2))
    for i in range(D1):
        result = random.randint(1, D2)
        total_sum += result
        NumList[i+1] = result
    msg1 = str(NumList)
    msg2 = '共掷骰{}次,点数为{}'.format(D1,total_sum)
    return msg1,msg2

#菜单函数
def Menu():
    msg = '我是AI地狱疣,功能菜单如下\n\
            ~~~~\n·1,随机图片\n·2,来份涩图\
                \n·3,来点好东西\n4,Roll点车卡\n整点报时\
                \n~~~~\n其他功能正在开发,敬请期待喵~'
    return msg

#来份涩图
def Picture1():
    apiurl = 'https://api.lolicon.app/setu/v2'
    m = requests.get(apiurl).json()
    n = json.dumps(m) 
    getapi = re.search(r'"original": "(.*?)"', n).group(1)
    return getapi

#随机图片
def Picture2():
    url1 = 'https://api.yimian.xyz/img'
    url2 = 'https://api.ghser.com/random/api.php'
    url3 = 'https://api.paugram.com/wallpaper/'
    url4 = 'https://api.zbcode.cn/fj/rand.php'
    resm = requests.get(url1)
    getapi = resm.url
    return getapi

#来点好东西
def Picture3():
    apiurl = 'https://api.lolicon.app/setu/v2?r18=1'
    m = requests.get(apiurl).json()
    n = json.dumps(m) 
    getapi = re.search(r'"original": "(.*?)"', n).group(1) #getapi
    tags = m['data'][0]['tags']
    return tags,getapi

#召唤涩图记录
def Member(name):
    try:
        member[name] = member[name] + 1
    except:
        member[name] = 1

#报时函数
def Time():
    times = time.localtime()
    time.struct_time 