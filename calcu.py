from mimetypes import init
from statistics import mean
from copy import deepcopy
import sys
print('参与厂商：{}家,报价分别为{}'.format(len(sys.argv)-1,sys.argv[1:]))
rightnum_int = list(map(int, sys.argv[1:]))
init_price = deepcopy(rightnum_int)
if len(sys.argv)-1 > 5:
    print('参与厂商大于等于6家,需要去除最高价{},和最低价:{}'.format(max(rightnum_int),min(rightnum_int)))
    rightnum_int.remove(max(rightnum_int))
    rightnum_int.remove(min(rightnum_int))
    print('去完最高价和最低价之后的报价有{}'.format(rightnum_int))
print('开始计算基准价...')
a = 0.5
A = mean(rightnum_int)*a + min(rightnum_int)*(1-a)
print('基准价为{}'.format(A)) 
print('开始计算每个报价的得分')  
for num in init_price:            
    if num > A:
        score = 50-(float(num-A)/30/0.03)*1                       
    else:
        diff_percent = float(A-num)/A
        if  diff_percent <=0.3:
            score = 50
        else:    
            score = 50-float(diff_percent-0.3)/0.03*0.5                                    
    print('报价：{}得分为：{}'.format(num,score))
