# -*- coding: UTF-8 -*-
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from flask import request
from flask import jsonify
import os
import time

app = Flask(__name__)
    

#上传功能
@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['myfile']
    file_name = request.form['filename']
    file_ext = file.filename.rsplit('.', 1)[1]
    file.save('/opt/Web/File/' + file_name + '.' + file_ext)

    Time = time.asctime( time.localtime(time.time()) )
    f = open('/opt/Web/UpLog.log','a+')
    f.write("\n时间 [{}], IP [{}] , 上传 [{}]".format(Time,request.remote_addr,file_name))
    f.close()
    return '文件上传成功！'


#下载功能
@app.route('/list')
def list_files():
    Time = time.asctime( time.localtime(time.time()) )
    f = open('/opt/Web/DownLog.log','a+')
    f.write("\n时间 [{}], IP [{}] 访问".format(Time,request.remote_addr))
    f.close()
    files = os.listdir('/opt/Web/File')
    return render_template('files.html', files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    Time = time.asctime( time.localtime(time.time()) )
    f = open('/opt/Web/DownLog.log','a+')
    f.write("\n时间 [{}], IP [{}] 下载[{}]".format(Time,request.remote_addr,filename))
    f.close()
    return send_from_directory('/opt/Web/File', filename, as_attachment=True)


#删除功能
@app.route('/delete/<path:filename>',methods=['POST'])
def delete_file(filename):
    os.remove('/opt/Web/File/' + filename)

    Time = time.asctime( time.localtime(time.time()) )
    f = open('/opt/Web/DownLog.log','a+')
    f.write("\n时间 [{}], IP [{}] 删除[{}]".format(Time,request.remote_addr,filename))
    f.close()

    return redirect(url_for('list_files'))



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

