#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
from Crypto.Util.number import *
import math
from string_operator_module import *

# 字节逆序
def byteinvert(str_bin):
    ret = ''
    for i in range(len(str_bin) // 8):
        ret += str_bin[i * 8:i * 8 + 8][::-1]
    return ret


# 标准曼彻斯特
def MCST_stand(str_bin):
    ret = ''
    for i in range(len(str_bin) // 2):
        x = str_bin[i * 2:i * 2 + 2]
        if x == '01':
            ret += '0'
        elif x == '10':
            ret += '1'
        else:
            return 'stand manchester decode wrong!'
    return ret


# IEEE规范的曼彻斯特
def MCST_IEEE(str_bin):
    ret = ''
    for i in range(math.ceil(len(str_bin) / 8)):
        x = str_bin[i * 2:i * 2 + 2]
        if x == '01':
            ret += '1'
        elif x == '10':
            ret += '0'
        else:
            return 'stand manchester decode wrong!'
    return ret


# 从第二位开始的差分曼彻斯特
def MCST_diff_from_2(str_bin):
    ret = ''
    for i in range(0, len(str_bin) // 2 - 1):
        x1 = str_bin[i * 2:i * 2 + 2]
        x2 = str_bin[i * 2 + 2:i * 2 + 4]
        if x1 == x2:
            ret += '0'
        else:
            ret += '1'
    return ret

# 从第二位开始的差分曼彻斯特规则是一致的，但是第一位的值需要考虑考虑时钟周期起点电平是否变化
# 也就是说，第一位有两种情况，可能是0，也可能是1
# refer: https://wenku.baidu.com/view/abde65d6f524ccbff0218432.html?fr=sogou&_wkts_=1687268864904
def MCST_diff(str_bin):
    res=[]
    res.append('0'+MCST_diff_from_2(str_bin))
    res.append('1'+MCST_diff_from_2(str_bin))
    return res

def MCST_burp(str_hex):
    str_bin = str(bin(int(str_hex, 16)))[2:]
    m1 = MCST_IEEE(str_bin)
    m2 = MCST_stand(str_bin)
    m3 = MCST_diff(str_bin)
    if 'wrong' not in m1:
        print(color_string('\nIEEE曼彻斯特:',BLUE))
        print(m1)
        print(hex(int(m1, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(m1, 2)),GREEN))
        # print("maybe SUCCESS",long_to_bytes(int(m1, 2)))
    if 'wrong' not in m2:
        print(color_string('\n 标准曼彻斯特:',BLUE))
        print(m2)
        print(hex(int(m2, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(m2, 2)),GREEN))
        # print("maybe SUCCESS",long_to_bytes(int(m2, 2)))
    # print('\n 差分曼彻斯特:')
    print(color_string('\n 差分曼彻斯特:',BLUE))
    for i in m3:
        print(i)
        print(hex(int(i, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(i, 2)),GREEN))
        # print("maybe SUCCESS",long_to_bytes(int(i, 2)))
    # print('\n=============字节逆序，未经实测=============')
    print(color_string('\n=============字节逆序，未经实测=============',BLUE))
    if 'wrong' not in m1:
        m1 = byteinvert(m1)
        # print('\nIEEE曼彻斯特:')
        print(color_string('\nIEEE曼彻斯特:',BLUE))
        print(m1)
        print(hex(int(m1, 2)))
        # print("maybe SUCCESS ",long_to_bytes(int(m1, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(m1, 2)),GREEN))
    if 'wrong' not in m2:
        m2 = byteinvert(m2)
        # print('\n 标准曼彻斯特:')
        print(color_string('\n 标准曼彻斯特:',BLUE))
        print(m2)
        print(hex(int(m2, 2)))
        # print("maybe SUCCESS ",long_to_bytes(int(m2, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(m2, 2)),GREEN))
    m3 = byteinvert(m3)
    # print('\n 差分曼彻斯特:')
    print(color_string('\n 差分曼彻斯特:',BLUE))
    for i in m3:
        print(i)
        print(hex(int(i, 2)))
        # print("maybe SUCCESS ",long_to_bytes(int(i, 2)))
        print("maybe "+color_string("SUCCESS",GREEN),color_string(long_to_bytes(int(i, 2)),GREEN))

def Manchester_decode(input_str):
    print("-"*20+color_string("[尝试曼彻斯特解码]",PURPLE)+"-"*20)        
    try:
        MCST_burp(input_str)
    except:
        pass

def example():
    str_hex = '2559659965656A9A65656996696965A6695669A9695A699569666A5A6A6569666A59695A69AA696569666AA6'   #b'BJD{DifManchestercode}' 标准曼彻斯特
    # str_hex = '295965569a596696995a9aa969996a6a9a669965656969996959669566a5655699669aa5656966a566a56656'   #b'\Sakura_Love_Strawberry' 差分曼彻斯特1
    # str_hex = '9a9a9a6a9aa9656699a699a566995956996a996aa6a965aa9a6aa596a699665a9aa699655a696569655a9a9a9a595a6965569a59665566955a6965a9596a99aa9a9566a699aa9a969969669aa6969a9559596669'    #b'flag{zw1tt1hl-7zcv-ebfk-akxt-i4xdsxeuv5d3}' 差分曼彻斯特0
    # str_hex = 'AAAAA56A69AA556A965A5999596AA95656'    #    0x8024d8845abf34119 差分曼彻斯特1
    # str_hex = '5555555595555A65556AA696AA6666666955'  #    802.3&字节逆序 未完成 # refer https://www.hetianlab.com/specialized/20220307151442
    # str_hex = '3EAAAAA56A69AA55A95995A569AA95565556'  #    未解出 refer https://blog.csdn.net/qq_43165101/article/details/97377830

    MCST_burp(str_hex)

if __name__ == "__main__":
    example()
