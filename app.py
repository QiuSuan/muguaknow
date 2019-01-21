# -* - coding:UTF-8 -*-

import os
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
mysql = MySQL(app)
appid = 'wxeb503dd88c262c1a'
appsecret = 'c295a9561e72aeb4eb3438b8057e778c'

@app.route('/')
def hello_world():
    return 'Hello Papaya!'

@app.route('/user/getuserinfo', methods=[ 'GET','POST'])
def getuserinfo():
    code = request.data.decode('utf-8')
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid,appsecret,code)
    r = requests.get(url)
    result = r.text
    resultdic=json.loads(result)
    openid=resultdic['openid']#至此获得了openid
    sqlstr="select * from mugua.comuser where mugua.comuser.openid="+"'"+openid+"'"
    cur = mysql.connection.cursor()
    cur.execute(sqlstr)
    rv = cur.fetchall()
    info = dict()
    info['openid']=openid
    if rv:
        info['isexist']="1"
    else:
        info['isexist'] = "0"
    return jsonify (info)

@app.route('/sendjson',methods=['GET'])
def sendjson():
    # 然后在本地对数据进行处理,再返回给前端
    info = dict()
    info['name'] = "pengshuang"
    info['lesson'] = "lesson"
    info['score'] = "score"
    return jsonify (info)

@app.route('/receivejson',methods=['POST'])
def receivejson():
    data = json.loads (request.get_data ())
    print(data['lesson'])
    return 'i love you'

@app.route('/getuniv')#,methods=['POST']
def getuniv():
    sqlstr = "select Univid,Univname from mugua.University"
    cur = mysql.connection.cursor ()
    cur.execute (sqlstr)
    rv = cur.fetchall ()
    info=dict(rv)
    return jsonify (info)


@app.route('/getcampus/<univid>',methods=['POST'])
def getcampus(univid):
    sqlstr = "select Campusid,Campusname from mugua.campus where Univid="+"'"+univid+"'"
    cur = mysql.connection.cursor ()
    cur.execute (sqlstr)
    rv = cur.fetchall ()
    info=dict(rv)
    return jsonify (info)

@app.route('/getschool/<univid>',methods=['POST'])
def getschool(univid):
    sqlstr = "select Snum,Sname from mugua.School where Univid="+"'"+univid+"'"
    cur = mysql.connection.cursor ()
    cur.execute (sqlstr)
    rv = cur.fetchall ()
    info=dict(rv)
    return jsonify (info)

@app.route('/getlabels/<mode>',methods=['POST'])
def getlabels(mode):
    #mode=0就是用户进入下一级的操作，1就是用户返回上一级的操作
    labelid = request.data.decode('utf-8')
    print(labelid)
    if mode=='0':
        if labelid=='null':
            sqlstr = "select Labelid,Labelname from mugua.Alllabels where Higherlabelid is null"
        else:
            sqlstr = "select Labelid,Labelname from mugua.Alllabels where Higherlabelid="+"'"+labelid+"'"
    else:
        sqlstr = "select Labelid,Labelname from mugua.Alllabels where Higherlabelid=(select Higherlabelid from mugua.Alllabels where labelid=)" + "'" + labelid + "'"
    cur = mysql.connection.cursor ()
    cur.execute (sqlstr)
    rv = cur.fetchall ()
    info=dict(rv)
    return jsonify (info)

@app.route('/user/signin',methods=['POST'])
def signin():
    sqlstrs = json.loads (request.get_data ())
    cur = mysql.connection.cursor ()
    for sqlstr in sqlstrs:
        print(sqlstr)
        cur.execute (sqlstr)
    mysql.connection.commit()
    return 'successfully signin, love you'

@app.route('/user/uploadPortrait',methods=['POST'])
def uploadPortrait():
    #上传头像
    sqlstrs = json.loads (request.get_data ())
    print(sqlstrs)
    return 'successfully signin, love you'


if __name__ == '__main__':
    app.run('127.0.0.1', debug=True, port=3000)