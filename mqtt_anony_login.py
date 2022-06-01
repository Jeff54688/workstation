#!/usr/bin/env python
# coding=utf-8
# Author: 王进福
import struct
import socket
import json

vulinfo = {
    'title': 'mqtt协议匿名登录',  # poc插件标题（漏洞标题）
    'is_code': 0,  # 1 代表这个插件，需要自己写检测代码；0，代表这个插件是个发包类型，只需要制定发包，回包匹配正则即可
    'vul_type': '',  # 漏洞类型
    'risk_level': 3,  # 1：低危, 2：中危, 3：高危, 4:严重
    'cve_id': '',
    'cnnvd_id': '',
    'desc':
        '''
        漏洞描述说明
        MQTT服务器默认允许匿名登录,在未配置账号密码的情况下,可直接登录向Broker中任意Topic发送或订阅消息,造成mqtt服务器和其他终端极大的不安全性
        ''',
    'solution':
        '''
        漏洞修复建议
        ''',
    'references': [
        ''
    ],  # 参考链接
}


def run(args):
    ip = args.get('ip')
    port = args.get('port')

    #poc逻辑开始
    print('check target: {}:{} for vuln {}'.format(ip, port, vulinfo.get('title')))

    # def anonymous_login(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    payload = b'\x10*\x00\x04MQTT\x04\x00\x00\t\x00\x1eamqtt_sub/4169-DESKTOP-7UHFD8D'
    s.send(payload)
    ret = s.recv(1024)
    # print(f'resp = {ret}')

    if ret == b' \x02\x01\x00' or b' \x02\x00\x00 ':
        out = {
            u'####################  验证信息': u'存在{} 漏洞'.format(vulinfo.get('title'))
        }
        return json.dumps(out, indent=4)

if __name__ == '__main__':    

    vul_target = {
        'ip': "3.233.221.125",
        'vul_id': 1,
        "port": 1883
    }

    print(run(vul_target))