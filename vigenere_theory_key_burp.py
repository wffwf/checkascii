#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
from string_operator_module import *
# 说明:基于维吉尼亚理论，对KEY的暴力破解
# 需要:完整的明文、密文对应关系
import string

# ---------------- 基础算法,留着万一有用 ----------------
# ---------------- 可见 ASCII 94 字符表 ----------------
# 密钥是 0x20–0x7E 共 94 个字符，空格到 ~
class classic_vigenere_expand:
    def __init__(self):
        self.ALPHABET = ''.join([chr(i) for i in range(0x20, 0x7F)])  # 基础算法字典，采用可见 ASCII 94 字符表
        self.ALPHABET_SIZE = len(self.ALPHABET)
    def set_dictionary(self,dic: str):
        self.ALPHABET = dic
    def char_index(self, ch: str) -> int:
        """字符 -> 在 94 字符表中的索引"""
        return ord(ch) - 0x20

    def index_char(self, idx: int) -> str:
        """索引 -> 对应字符（自动循环）"""
        return chr((idx % self.ALPHABET_SIZE) + 0x20)

    # ---------------- 加/解密实现 ----------------
    def vigenere_enc(self, plain: str, key: str) -> str:
        """维吉尼亚加密（可见字符版）"""
        cipher = []
        for i, ch in enumerate(plain):
            if ch not in self.ALPHABET:           # 非可见字符原样保留
                cipher.append(ch)
                continue
            k = key[i % len(key)]            # 密钥循环使用
            shift = self.char_index(k)            # 密钥字符对应的偏移量
            new_idx = (self.char_index(ch) + shift) % self.ALPHABET_SIZE
            cipher.append(self.index_char(new_idx))
        return ''.join(cipher)

    def vigenere_dec(self, cipher: str, key: str) -> str:
        """维吉尼亚解密（可见字符版）"""
        plain = []
        for i, ch in enumerate(cipher):
            if ch not in self.ALPHABET:           # 非可见字符原样保留
                plain.append(ch)
                continue
            k = key[i % len(key)]
            shift = self.char_index(k)
            new_idx = (self.char_index(ch) - shift) % self.ALPHABET_SIZE
            plain.append(self.index_char(new_idx))
        return ''.join(plain)

    def crack_key(self, plain: str, cipher: str) -> str:
        """根据已知明文和密文破解密钥"""
        if len(plain) != len(cipher):
            raise ValueError("明文和密文长度必须一致")
        
        key_chars = []
        # 计算每个位置的密钥字符
        for m, c in zip(plain, cipher):
            if m not in self.ALPHABET or c not in self.ALPHABET:
                # 忽略非可见字符位置（原明文和密文无此类字符）
                continue
            # 计算密钥索引：(密文索引 - 明文索引) % 字符集大小
            key_idx = (self.char_index(c) - self.char_index(m)) % self.ALPHABET_SIZE
            key_chars.append(self.index_char(key_idx))

        key = ''.join(key_chars)
        
        return key

def classic_vigenere_expand_test(c,m):
    m = "Hello,good morning!How are you?" # 2024年省网信安竞赛题
    c = "u_LcYsM^UWeM[XhIX[`<Q^eb@__pY]%"
    v = classic_vigenere_expand()
    v.set_dictionary(''.join([chr(i) for i in range(0x40, 0x7F)])) # 故意设置错误的字典
    key = v.crack_key(m, c)
    print(key)
    key = "My_vigenere_key_is_safe!"
    ENC = [0x34,0x66,0x41,0x5e,0x65,0x5e,0x76,0x56,0x78,0x61,0x78,0x52,0x7e,0x45,0x2b,0x53,0x49,0x34,0x3f,0x5b,0x54,0x79,0x26,0x75,0x2d,0x5d,0x52,0x70,0x5a,0x5c,0x75,0x4e,0x78,0x27,0x4d,0x44,0x52,0x77,0x2d,0x52,0x7d,0x6b,0x45,0x71]
    encenc = ''.join(chr(i) for i in ENC)
    print(v.vigenere_dec(encenc,key))

def another_theory_key_burp(c,m): # 现场写的另外一种原理破解，与可见字符版的有区别，对于字典格式要求更低
    def myprint(a,idx): # idx为行标，构造第idx行的结构
        res = []
        for i in range(idx,len(a)):
            res.append(a[i])
        for j in range(idx):
            res.append(a[j])
        return(res)

    juzheng=[] # 维吉尼亚多字母映射表结构
    def output(a):
        length = len(a)
        for i in range(length):
            juzheng.append(myprint(a,i)) # 生成多字母映射表

    ALPHABET = ''.join([chr(i) for i in range(0x20, 0x7F)])  # 2024年省网信安竞赛题字典

    print("-"*20+color_string("[结合一段已知的明文和密文,爆破vigenere密钥]",PURPLE)+"-"*20) 
    if len(c) != len(m):
        print("-"*20+color_string("输入明文密文长度不一致，退出原理破解，仍需破解，请修改代码",YELLOW)+"-"*20) 
    else:
        dic = input("请输入"+color_string("已知字典",GREEN)+",直接回车则使用默认字典"+color_string(ALPHABET,GREEN)+",请输入：")
        if len(dic) > 0 :
            ALPHABET = list(dic)

        output(ALPHABET)
        key = ''
        for i in range(len(m)): # 原理破解
            a = juzheng[0].index(m[i])
            for j in range(len(juzheng)):
                if juzheng[j][a] == c[i]:
                    key += juzheng[0][j]
        print(color_string("密钥破解结果: ",YELLOW) + key)

def test_another_theory_key_burp(c,m):
    def myprint(a,idx): # idx为行标，构造第idx行的结构
        res = []
        for i in range(idx,len(a)):
            res.append(a[i])
        for j in range(idx):
            res.append(a[j])
        return(res)

    juzheng=[] # 维吉尼亚多字母映射表结构
    def output(a):
        length = len(a)
        for i in range(length):
            juzheng.append(myprint(a,i)) # 生成多字母映射表

    ALPHABET = ''.join([chr(i) for i in range(0x20, 0x7F)])  # 2024年省网信安竞赛题字典

    print("-"*20+color_string("[结合一段已知的明文和密文,爆破vigenere密钥]",PURPLE)+"-"*20) 
    if len(c) != len(m):
        print("-"*20+color_string("输入明文密文长度不一致，退出原理破解，仍需破解，请修改代码",YELLOW)+"-"*20) 
    else:
        output(ALPHABET)
        key = ''
        for i in range(len(m)): # 原理破解
            a = juzheng[0].index(m[i])
            for j in range(len(juzheng)):
                if juzheng[j][a] == c[i]:
                    key += juzheng[0][j]
        print(color_string("密钥破解结果: ",YELLOW) + key)    
        
def vigenere_theory_key_burp(c,m):
    another_theory_key_burp(c,m)

if __name__ == "__main__":
    m = "Hello,good morning!How are you?" # 2024年省网信安竞赛题
    c = "u_LcYsM^UWeM[XhIX[`<Q^eb@__pY]%"
    test_another_theory_key_burp(c,m)
