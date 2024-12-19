#!/usr/bin/env python
# -*- coding: utf_8 -*-
# Author: seclover
# Modified： wfsec
from string_operator_module import *

def standard_fence(e):
    # print('标准栅栏暴力破解:')
    print(color_string('标准栅栏暴力破解:',BLUE))

    elen = len(e)
    field=[]
    for i in range(2,elen):
        if(elen%i==0):
            field.append(i)
    
    for f in field:
        b = elen // f
        result = {x:'' for x in range(b)}
        for i in range(elen):
            a = i % b;
            result.update({a:result[a] + e[i]})
        d = ''
        for i in range(b):
            d = d + result[i]
        # print('split '+str(f)+',result: '+d)
        print('split '+str(f)+',result: '+color_string(d,GREEN))


def w_zhalan_jia(text, n, TYPE):
    # n小于2时不满足栅栏的最小形成条件
    if n < 2:
        return ""
    string1 = [[] for _ in range(0, n)]
    for i in range(0, n):
        for j in range(0, int((len(text) / (n-1))+1)):
            string1[i].append(-1)
    flag = 1  # 方向标准 1 向下  -1  向上
    hang = 0  # 行定位变量
    lie = 0  # 列定位变量
    po = 1  # 控制波动
    for password in text:  # 迭代每一个字符
        if hang == 0:
            flag = 1
        if hang == (n - 1):
            flag = -1
        if po == n:
            lie = lie + 1
            po = 1
        string1[hang][lie] = password
        hang = hang + flag
        po = po + 1
    password = ""
    string_password = []
    for i in range(0, n):
        for j in range(0, int((len(text) / (n-1)))+1):
            if string1[i][j] != -1:
                string_password.append(string1[i][j])
    for ps in string_password:
        password = password + str(ps)
    if TYPE == 0:#返回处理后列表
        return password
    if TYPE == 1:
        return string_password#返回字符串
    if TYPE == 2:
        return string1#返回处理前列表

def w_zhalan_jie(text, n):
    # n小于2时不满足栅栏的最小形成条件
    if n < 2:
        return ""
    str_key = list(range(0, len(text)))  # 获取加密数据长度并创建相应的列表
    key_password = list(w_zhalan_jia(str_key, n, 1))  # 密码下标列表
    key_text = list(text)  # 原始密文
    key = ""
    # 对应下标的赋值
    for password in range(0, len(text)):
        str_key[key_password[password]] = key_text[password]
    # 返回字符串
    for tx in str_key:
        key = key + tx
    print('w_split '+str(n)+',result: '+color_string(key,GREEN))
    # print('w_split '+str(n)+',result: '+key)


def w_fence(e):
    # print('W型栅栏暴力破解:')
    print(color_string('W型栅栏暴力破解:',BLUE))

    elen = len(e)
    field=[]
    for i in range(2,elen):
        if(elen%i==0):
            field.append(i)

    for n in field:
        w_zhalan_jie(e,n)

def Fence_burp(e):
    standard_fence(e)
    w_fence(e)

def Fence_decode(input_str):
    print("-"*20+color_string("[尝试栅栏解码]",PURPLE)+"-"*20)   
    if(len(input_str)>200):
        print("密文长度超过200,栅栏爆破就没有意义了!")
        return     
    try:
        Fence_burp(input_str)
    except:
        pass

def fence_example():
    e = 'fa{el_lghlo}'
    Fence_burp(e)

def w_fence_example():
    e = "ccehgyaefnpeoobe{lcirg}epriec_ora_g"
    Fence_burp(e)


if __name__ == "__main__":
    w_fence_example()
    fence_example()