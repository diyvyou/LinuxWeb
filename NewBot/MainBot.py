# -*- coding: UTF-8 -*-
import json
import requests
from flask import request, Flask,render_template
import re
import plugins

with open("config.json", "r", encoding='utf-8') as jsonfile:
    config_data = json.load(jsonfile)
    qq_config = config_data["qq_bot"]
    qq_no = qq_config['qq_no']
    cqhttp_url = qq_config['cqhttp_url']
server = Flask(__name__)



@server.route('/', methods=["POST"])
def get_message():
    if request.get_json().get('message_type') == 'group': 
        global gid,uid
        gid = request.get_json().get('group_id')  
        uid = request.get_json().get('sender').get('user_id')  # 发言者的qq号
        message = request.get_json().get('raw_message')  # 获取原始信息
        print("收到消息：{}".format(message))
        if re.match(r"^r", message):
            msg1,msg2 = plugins.Roll(message)
            SendMsg(msg1)
            SendMsg(msg2)
        if message == '菜单':
            msg = plugins.Menu()
            SendMsg(msg)
        if message == '随机图片':
            getapi = plugins.Picture2()
            SendPic(getapi)
        if message == '来份涩图':
            getapi = plugins.Picture1()
            SendPic(getapi)
        if message == '来点好东西':
            tags,getapi = plugins.Picture3()
            SendMsg(tags)
            SendMsg(getapi)
            plugins.Member(uid)   
        if message == '来点好东西/':
            tags,getapi = plugins.Picture3()
            SendMsg(tags)
            SendPic(getapi)
            plugins.Member(uid)
        if re.match(r"^查询/", message):
            match = re.search(r"(\d+)D(\d+)", message)
            num = plugins.member[match]
            try:
                SendMsg("UID:{}/共召唤涩图{}份".format(match,num))
            except:
                SendMsg("UID:{}/无法查询".format(match))
        return 'ok'

def SendMsg(message):
    print("发送消息:{}".format(message))
    res = requests.post(url=cqhttp_url + "/send_group_msg",  params={'group_id': int(gid), 'message': message}).json()
    if res["status"] == "ok":
        print("消息发送成功")
    else:
        print("消息发送失败，错误信息：" + str(res['wording']))

def SendPic(getapi):
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