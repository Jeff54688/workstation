#!/usr/bin/env python
# coding=utf-8
# Author: POC编写人
import requests
import json
import random
try:
    from urllib.parse import urlparse
    from urllib.parse import unquote, quote
except BaseException:
    from urlparse import urlparse
    from urllib import quote, unquote
try:
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
except Exception as e:
    pass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vulinfo = {
    'title': '',  # poc插件标题（漏洞标题）
    'is_code': 1,  # 1 代表这个插件，需要自己写检测代码；0，代表这个插件是个发包类型，只需要制定发包，回包匹配正则即可
    'vul_type': '',  # 漏洞类型
    'risk_level': 3,  # 1：低危, 2：中危, 3：高危, 4:严重
    'cve_id': '',
    'cnnvd_id': '',
    'desc':
        '''
        漏洞描述说明
        ''',
    'solution':
        '''
        漏洞修复建议
        ''',
    'references': [
        ''
    ],  # 参考链接
}
proxies = {}    # 代理，不要删除


def check_dnslog(key):
    try:
        resp = requests.get(
            url="http://admin.dnslog.bid:9002/api/dns/ser/%s/" % key, timeout=15)
        if resp.status_code == 200 and 'true' in resp.text.lower():
            return True
    except Exception as e:
        print(e)
    return False


def getkey(length=8):
    return ''.join(random.sample(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o',
         'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], length))


def parse_response(response, content=''):
    """格式化返回报文。"""
    parsed_response = '\n'.join(['HTTP/1.1 %s %s' % (
    response.status_code if hasattr(response, 'status_code') else response.status, response.reason)] +
                                  ['%s: %s' % (k, v)
                                   for k, v in dict(response.headers
                                                    if hasattr(response, 'headers')
                                                    else response.getheaders()).items()] +
                                  [''] + [response.text if hasattr(response, 'text') else content])
    return parsed_response[:2048].replace('\x00', '')


def parse_requst_from_response(response):
    """基于request的resp 打印带payload的请求报文。"""
    body = response.request.body if response.request.body else ''
    if 'Host' in str(response.request.headers.keys()):
        header_list = ['%s: %s' % (k, v) for k, v in dict(response.request.headers).items()]
    else:
        header_list = ['%s: %s' % (k, v) for k, v in dict(response.request.headers).items()]
        header_list.append('Host: {}'.format(urlparse(response.url).netloc))
    parsed_request = '\n'.join(['%s %s %s' % (response.request.method, response.request.path_url, 'HTTP/1.1')] +
                                 header_list + [''] + ['']) + str(body)
    return parsed_request[:2048].replace('\x00', '')


def parse_requsted(method, url, headers, params):
    """打印带payload的请求报文。"""
    parser_url = urlparse(url)
    return '\n'.join(['%s %s %s' % (method, parser_url.path, 'HTTP/1.1')] +
                       ['{}: {}'.format(key, value) for key, value in headers.items()] + ['', '']) + str(params)


def run(args):
    ip = args.get('ip')
    port = args.get('port')
    service = args.get('service')   # 服务
    product = args.get('product')   # 应用
    url = args.get('url')           # Web指纹对应的url,可能已经处理过跳转
    vul_id = args.get('vul_id')     # 插件ID
    if url:
        parser_url = urlparse(url)
        base_url = '{}://{}'.format(parser_url.scheme, parser_url.netloc)
    else:
        if service == 'https':
            url = 'https://%s:%s' % (ip, port)
        else:
            url = 'http://%s:%s' % (ip, port)
        base_url = url
    url = url.strip('/')

    try:
        key = getkey()
        users = []                      # 插件默认的弱账号列表
        passwords = []                       # 插件默认的弱口令列表
        u_users = args.get('users')     # 弱口令类型插件， 用户自定义的用户组
        u_pwds = args.get('pwds')       # 弱口令类型插件， 用户自定义的密码组
        if u_users:
            users = u_users if isinstance(
                u_users, list) else u_users.replace(
                '\r', '').split('\n')
        if u_pwds:
            passwords = u_pwds if isinstance(
                u_pwds, list) else u_pwds.replace(
                '\r', '').split('\n')
        users = list(set(users))
        passwords = list(set(passwords))

        if vul_id and ip:
            vul_id_tag = '{:04x}'.format(vul_id)
            ip_tag = '{:02x}{:02x}{:02x}{:02x}'.format(*tuple([int(i) if i.isdigit() else 0 for i in ip.split('.', 3)])) if ip.count('.') == 3 else 'wwww'
            mark = '{}.{}'.format(vul_id_tag, ip_tag)
            dnslog = '{}.{}.ser.dnslog.bid'.format(mark, key)
        else:
            dnslog = '1234.abcdefgh.{}.ser.dnslog.bid'.format(key)

        # POC逻辑开始
        print('check target: {}:{} for vuln {}'.format(ip, port, vulinfo.get('title')))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) '
                          'Chrome/41.0.2228.0 Safari/537.21',
            'Accept': '*/*',
            'Connection': 'close'
        }
        
        for check_url in {base_url, url, base_url+'/solr/'}:     # login为特定路径
            # http请求，最好加上allow_redirects=False，防止跳转导致误报的出现
            resp = requests.request(url=check_url, method="GET", headers=headers, timeout=10, verify=False,
                                    allow_redirects=True, stream=True, proxies=proxies)
            if resp.status_code == 200:     # poc验证成功的规则
                out = {
                    u'####################  验证信息': u'存在{} 漏洞'.format(vulinfo.get('title')),
                    u'####################  请求链接': check_url,
                    u'####################  请求数据包': parse_requst_from_response(resp),       # 打印请求数据包
                    u'####################  返回数据包': parse_response(resp),                   # 打印返回数据包
                }
                return json.dumps(out, indent=4)
        # POC逻辑结束
    except Exception as e:
        print(e)
    return False


if __name__ == '__main__':
    proxies = {
        'http': 'http://127.0.0.1:18080',
        'https': 'http://127.0.0.1:18080'
    }
    vul_target = {
        'ip': "112.121.123.123",
        'vul_id': 1,
        "port": 60001,
        "service": "unknown",    # 对应nmap的service
        'product': '',           # 对应nmap的prudoct
        "url": "http://www.cubesec.cn",
        "title": '',
        'header': '',
        "content": "",
        'users': ['root', 'admin'],  # 平台传入，全局弱口令，用户自定义弱口令
        'pwds': ['123456', 'admin'], # 平台传入，全局弱口令，用户自定义弱口令
    }
    print(run(vul_target))
