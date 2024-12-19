#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
#重合指数的应用:
import gmpy2
from string_operator_module import *
best_index=0.065
#sum=0
dic_index={'a': 0.08167,'b': 0.01492,'c': 0.02782,'d':0.04253,'e': 0.12702,'f':0.02228,'g': 0.02015,'h':0.06094,'i':0.06966,'j':0.00153,'k':0.00772,'l':0.04025,'m':0.02406,'n':0.06749,'o':0.07507,'p':0.01929,'q':0.00095,'r':0.05987,'s':0.06327,'t':0.09056,'u':0.02758,'v':0.00978,'w':0.02360,'x':0.00150,'y':0.01974,'z':0.00074}
def index_of_coincidence(s):
    '''
    计算字符串的重合指数(所有字母出现频率的平方和)
    :param s: 给定字符串
    :return: 重合指数
    '''
    alpha='abcdefghijklmnopqrstuvwxyz'#给定字母表
    freq={}#统计字母频率(frequency)
    for i in alpha:
        freq[i]=0
    #先全部初始化为0
    for i in s:
        freq[i]=freq[i]+1
    #统计频率
    index=0
    for i in alpha:
        index = index + (freq[i] * (freq[i] - 1)) / (len(s) * (len(s) - 1))
    return index
def index_of_coincidence_m(s):
    '''
    计算明文s中的各字母的频率与英文字母中的频率的吻合程度.
    :param s:明文s
    :return:吻合程度
    '''
    #print(len(s))
    alpha = 'abcdefghijklmnopqrstuvwxyz'  # 给定字母表
    freq = {}  # 统计字母频率(frequency)
    for i in alpha:
        freq[i] = 0
    # 先全部初始化为0
    for i in s:
        freq[i] = freq[i] + 1
    # 统计频率
    index = 0
    for i in alpha:
        index = index + freq[i] / len(s) * dic_index[i]
    return index
def get_cycle(c):
    '''
    求出最符合统计学的m,n的最小公共周期,方法为通过爆破足够大的周期样本,观察成倍出现的周期.
    计算方法为解出每一个子密文段的重合指数和然后求平均值 再与最佳重合指数相减 误差在0.01以内.
    :param c: 密文
    :return: 公共周期列表
    '''
    cycle=[]
    for i in range(1,100):
        average_index=0#平均重合指数初始化为0
        for j in range(i):
            s = ''.join(c[j+i*x] for x in range(0,len(c)//i))
            index=index_of_coincidence(s)
            average_index+=index
        average_index=average_index/i-best_index
        if abs(average_index)<0.01:
            cycle.append(i)
    return cycle

#爆破keys
def decrypt(c,i,j):
    '''
    通过i,j解出与之相对应的密文段
    :param c: 密文段
    :param i:与明文相乘的key
    :param j: 位移j(维吉尼亚密码)
    :return: 明文段
    '''
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    m=''
    for x in c:
        m+=alpha[((alpha.index(x)-j)*gmpy2.invert(i,26))%26]
    return m
def get_key(c):
    '''
    得到某一密文段的单个字符key i j
    方法为暴力枚举所有的可能性,找到最符合统计学规律的 i,j 即该密文段的重合指数与最佳重合指数误差小于0.01
    :param c: 密文段
    :return: i,j
    '''
    for i in range(26):
        if  gmpy2.gcd(i,26)!=1:#i对26的逆元不只一个,造成明文不唯一,因此不符合条件.
            continue
        for j in range(26):
            m=decrypt(c,i,j)
            index=index_of_coincidence_m(m)
            if abs(index-0.065)<0.01:
                return (i,j)
def get_all_key(s,cycle):
    '''
    得到一个周期内的所有的密文段的key
    :param s: 原密文
    :param cycle: 周期
    :return: 无
    '''
    #print(len(s)//cycle)
    for i in range(cycle):
        temps=''.join([s[i+x*cycle] for x in range(0,len(s)//cycle)])
        print(get_key(temps))

def cipin_mix_fangshe_affine(c):
    try:
        # print("---------------------- \033[1;35m[词频分析结合仿射加密的解密过程]\033[0m --------------")
        print("-"*20+color_string("[词频分析结合仿射加密的解密过程]",PURPLE)+"-"*20)        

        cycle=get_cycle(c)
        print(cycle)#[6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96]
        
        #通过计算得到cycle都是6的倍数,因此cycle最小很有可能为6
        if (len(cycle)>0):
            cycle= input("请根据上述输出判断得到cycle,一般是提供最大公约数:")
            print("you input cycle is :",cycle)
        
            get_all_key(c,int(cycle))
            # (19, 10)
            # (7, 9)
            # (23, 3)
            # (19, 24)
            # (7, 14)
            # (23, 15)
            #此时我们大致可以推测出:keya=[19,7,23],keyb=[10,9,3,24,14,15],因此根据题目给的式子,我们就可以还原出明文了.
            plaintext=''
            #keya=[19,7,23]
            #keyb=[10,9,3,24,14,15]
            keya=[]
            keyb=[]
            print("请根据上述输出，分析循环过程，推测给出keya，keyb。注：仿射密码加密算法默认c = [keya*p+keyb]%26")
            key1=input("请根据第一列，分析并输入keya,一般为第一列的循环体，数字之间以空格分隔，保持原有顺序:")
            key_t = key1.split()
            for _key in key_t:
                keya.append(int(_key))
            key2=input("请根据第二列，分析并输入keyb,一般为第二列的循环体，数字之间以空格分隔，保持原有顺序:")
            key_t = key2.split()
            for _key in key_t:
                keyb.append(int(_key))
            len_a=len(keya)
            len_b=len(keyb)
            alpha='abcdefghijklmnopqrstuvwxyz'
            for i in range(len(c)):
                plaintext+=alpha[((alpha.index(c[i])-keyb[i%len_b])*gmpy2.invert(keya[i%len_a],26))%26]
            print(plaintext)
    except:
            print("词频分析结合仿射加密,affine_mix_char_frequency要求加密文件只支持小写字母，请检查。可尝试转小写，去空格，去除不支持的字符等")

def cipin_mix_fangshe_affine_example(c):
    cycle=get_cycle(c)
    cycle = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96]
    print(cycle)#

    #通过计算得到cycle都是6的倍数,因此cycle最小很有可能为6

    cycle=6

    get_all_key(c,6)
    # (19, 10)
    # (7, 9)
    # (23, 3)
    # (19, 24)
    # (7, 14)
    # (23, 15)
    #此时我们大致可以推测出:keya=[19,7,23],keyb=[10,9,3,24,14,15],因此根据题目给的式子,我们就可以还原出明文了.
    plaintext=''
    keya=[19,7,23]
    keyb=[10,9,3,24,14,15]
    len_a=len(keya)
    len_b=len(keyb)
    alpha='abcdefghijklmnopqrstuvwxyz'
    for i in range(len(c)):
        plaintext+=alpha[((alpha.index(c[i])-keyb[i%len_b])*gmpy2.invert(keya[i%len_a],26))%26]
    print(plaintext)

    #flag{helloxnucagoodluck}

if __name__ == "__main__":
    c=open('affine_mix_char_frequency.txt','r').read()
    cipin_mix_fangshe_affine(c)
    # cipin_mix_fangshe_affine_example(c)