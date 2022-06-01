import re

reg = 'Www-Authenticate: Basic realm=".*?(?P<app_name>PEPLINK (?P<app_version>[\w/\s]+) VPN[-/]{1}Firewall)"'    #正则表达式语句
#val = 'WWW-Authenticate: Basic realm="XUNBO PEPLINK NG320 VPN/Firewall"'    #要匹配的值
# Www-Authenticate: Basic realm="Matrix 3D Firewall"

val = 'HTTP/1.0 401 Unauthorized\
Date: Sat, 07 Apr 2012 14:04:43 GMT\
Content-Type: text/html; charset=gb2312\
Cache-Control: no-cache, no-store, must-revalidate, private\
Expires: Thu, 31 Dec 1970 00:00:00 GMT\
Pragma: no-cache\
Www-Authenticate: Basic realm="XUNBO PEPLINK NG500 VPN-Firewall"\
Connection: close'

c = re.compile(reg, re.I)
result = c.search(val)
import pdb;pdb.set_trace()
result = result.groupdict()
print(result)

# Basic realm="(?P<app_name>TP-LINK[\s*\w+]*Wireless[\s*\w+]+Router) (?P<app_version>[\w/\s]+)"
# 可匹配
# WWW-Authenticate: Basic realm="TP-LINK Wireless Router WR340G"
# app_name： TP-LINK Wireless Router
# app_version： WR340G

# <span class="branding">(?P<app_name>FireBrick) (?P<app_version>[\w/\s]+)</span>
