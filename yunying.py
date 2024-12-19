#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
'''
#云影密码
又叫“01248密码”，即编码只有01248几个数字
1248：通过加法来用这四个数字表示0-9中的任何一个数字，列如0=28， 也就是0=2+8，同理7=124， 9=18。这样之后再用1-26来表示26个英文字母；0：作为间隔。
'''
#a="8842101220480224404014224202480122"
#yourpiniseightfourtwozeroeightfourtwoonezeroeighteightfourzerotwofourzeroeightfourzeroonezeroonetwofourx
from string_operator_module import *
def yunying_01248_decode(a):
    print("-"*20+color_string("[尝试云影密码解码]",PURPLE)+"-"*20)    
    try:
        s=a.split('0')
        l=[]
        for i in s:
            sum=0
            for j in i:
                sum+=eval(j)
            l.append(chr(sum+64))
        print("maybe "+color_string("SUCCESS",GREEN)+" decode result is : ",end='')
        print(color_string(''.join(l),GREEN))
    except:
        # print("maybe "+color_string("FAILED",YELLOW)+" 云影密码解密失败")
        pass

if __name__ == "__main__":
    a="8842101220480224404014224202480122"
    yunying_01248_decode(a)
