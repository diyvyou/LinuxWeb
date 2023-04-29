# -*- coding: UTF-8 -*-
import json
import requests
from flask import request, Flask,render_template
import re
import time
import datetime
import threading
import CPU
import plugins


AdminNum = 3282995855
with open("config.json", "r", encoding='utf-8') as jsonfile:
    config_data = json.load(jsonfile)
    qq_config = config_data["qq_bot"]
    qq_no = qq_config['qq_no']
    cqhttp_url = qq_config['cqhttp_url']

server = Flask(__name__)

#接受信息
@server.route('/', methods=["POST"])
def get_message():
    if request.get_json().get('message_type') == 'group': 
        global gid,uid #群号 QQ号
        gid = request.get_json().get('group_id')  
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')  # 获取原始信息
        print("{}:{}".format(uid,message))
        plugins.MessageRemory(gid,uid,message)

        if message == '服务器状态':
            sCpu,sMemory,sDisk=CPU.Push()
            LinuxCpu = "{}\n{}\n{}".format(sCpu,sMemory,sDisk) 
            SendMessage(LinuxCpu)

        elif message == '来点好东西':
            tags,getapi = plugins.NicePic()
            SendMessage(tags)
            SendMessage(getapi)
            SendPicture(getapi)
            plugins.Remory(uid)

        elif message == '查询召唤数量':
            NumStr = plugins.QueryPicNum()
            SendMessage(NumStr)
        
        elif message == '查询最近信息' :
            DeWithDrawLog = plugins.DeWithDraw(gid)
            SendMessage(DeWithDrawLog)

        return 'ok'


#发送文字消息  
def SendMessage(message):
    print("发送消息:{}".format(message))
    res = requests.post(url=cqhttp_url + "/send_group_msg",  params={'group_id': int(gid), 'message': message}).json()
    if res["status"] == "ok":
        print("消息发送成功")
    else:
        print("消息发送失败，错误信息：" + str(res['wording']))
#发送图片消息
def SendPicture(getapi):
    print("发送消息:{}".format(getapi))
    message = "[CQ:image,file=" + getapi + "]"
    message = str('[CQ:at,qq=%s]\n' % uid) + message
    res = requests.post(url=cqhttp_url + "/send_group_msg",params={'group_id': int(gid), 'message': message}).json()
    if res["status"] == "ok":
        print("消息发送成功")
    else:
        print("消息发送失败，错误信息：" + str(res['wording']))


if __name__ == '__main__':
    server.run(port=7777, host='0.0.0.0', use_reloader=False)