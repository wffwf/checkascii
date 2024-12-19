#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: wfsec
import string
import itertools
import multiprocessing
import numpy as np
from string_operator_module import *
import gmpy2

class HillCipherBreaker:
    def __init__(self,mingwen='',miwen='',miwen_all='',miwen_all_all='',dic=string.ascii_lowercase):
        self.RUN = True
        self.dictionary = dic
        self.Module = len(dic)
        self.H = 2 # 密文矩阵高度，默认只支持密文为2*2的矩阵爆破，3*3的太大了
        self.CC = self.charencode(miwen)
        self.MM = self.charencode(mingwen)
        # 将明文M格式化成np格式[m0,m1,m2,m3,m4,m5]==>[m0,m3][m1,m4][m2,m5]
        self.M = self.formatCM_T(mingwen)
        self.C = self.formatCM_T(miwen)
        # print("明文"+self.chardecode(self.charencode(mingwen))+"转置矩阵:")
        # print(self.M)
        # print("密文"+self.chardecode(self.charencode(miwen))+"转置矩阵:")
        # print(self.C)
        self.MA = self.formatCM_T(miwen_all)
        self.miwen_all_all = miwen_all_all
        self.mingwen = mingwen


    def formatCM_T(self,cm): # 针对明文的矩阵处理，_T意思是需要转置
        miwen_or_mingwen = self.charencode(cm)
        if len(miwen_or_mingwen)%self.H != 0:
            print("Error, not support "+cm)
            self.RUN = False
        else:
            # print(self.chardecode(miwen_or_mingwen)+"矩阵:")
            # print(np.array(miwen_or_mingwen).reshape(len(miwen_or_mingwen) // self.H, self.H).T)
            return np.array(miwen_or_mingwen).reshape(len(miwen_or_mingwen) // self.H, self.H).T
    def charencode(self,str):
        str = str.lower()
        result = [self.dictionary.index(i) for i in str if i in self.dictionary]
        return result
    def chardecode(self,shuzu):
        result = "".join([self.dictionary[i] for i in shuzu])
        return result

    def Hillencode(self,key):
        # 默认K是2*2
        # 将K格式化成np格式[k0,k1,k2,k3]==>[k0,k1][k2,k3],不用转置
        K = np.array(self.charencode(key)).reshape(self.H, len(key)//self.H)
        C = (K @ self.M) % self.Module
        # 本来应该直接返回C，报一个关于nparray的返回错误，没有细看
        return C.T.flatten().tolist()
        # print(C.T.flatten().tolist())
    def Hilldecode(self,key):
        # 默认K是2*2
        # 将K格式化成np格式[k0,k1,k2,k3]==>[k0,k1][k2,k3]
        K = np.array(self.charencode(key)).reshape(self.H, len(key)//self.H)
        # 解密需要求K的逆
        K_inv = self.matrix_mod_inverse(K)
        try:
            C = (K_inv @ self.MA) % self.Module
            # 本来应该直接返回C，报一个关于nparray的返回错误，没有细看
            return C.T.flatten().tolist()
        except:
            return []

    def matrix_mod_inverse(self,matrix):
        # 求矩阵模26的逆元
        # self.Module = 26
        # refer https://wenku.csdn.net/answer/2c1tb4wbt9

        # 计算矩阵的行列式
        # det = int(np.linalg.det(matrix))
        det = np.round(np.linalg.det(matrix)).astype(int)
        # 计算模26下的逆元
        mod_inverse = -1
        for i in range(self.Module):
            if (det * i) % self.Module == 1:
                mod_inverse = i
                break
        # 如果逆元不存在，返回空
        if mod_inverse == -1:
            return np.array([])
        # 计算矩阵的伴随矩阵
        adj_matrix = np.linalg.inv(matrix) * det
        # 计算模26下的逆矩阵
        mod_inverse_matrix = (adj_matrix * mod_inverse) % self.Module
        return mod_inverse_matrix.astype(int)



    def work(self,key):
        if self.Hillencode(key)==self.CC:
            print("爆破成功，发现密码："+key,end=' ')
            print(self.charencode(key))
            return 1
        else:
            return 0

    def run(self):
        # Hill定义K*M=C，爆破K
        if self.RUN:
            pools = []
            for i in itertools.product(self.dictionary,repeat=self.H**2):
                pools.append(''.join(i))
            print("一共有"+str(len(pools))+"组"+str(self.H)+"*"+str(self.H)+"矩阵数据需要尝试, 开始爆破...",)
            num_processes = multiprocessing.cpu_count()  # 根据CPU核心数确定进程数量，可按需调整
            pool = multiprocessing.Pool(num_processes)
            results = pool.map(self.work, pools)
            pool.close()
            pool.join()
            # 可以根据results进一步处理，比如查看是否有符合条件的结果
            for index, result in enumerate(results):
                if result == 1:
                    print(f"在索引 {index} 处的元素 {pools[index]} 符合要求",end=' ')
                    result = self.chardecode(self.Hilldecode(pools[index]))
                    if self.mingwen in result:
                        print(color_string(result,GREEN))
                        print(f"请补齐 26 个字母外的其他字符,参考   {color_string(self.miwen_all_all,GREEN)}")
                    else:
                        print()
        else:
            return 0
    def printSageCode1(self,miwen_all,mingwen,miwen,key):
        print("已知密文:"+self.chardecode(self.charencode(miwen)),end=' ')
        print(self.charencode(miwen))
        print("已知明文:"+self.chardecode(self.charencode(mingwen)),end=' ')
        print(self.charencode(mingwen))
        print("原始密文:"+self.chardecode(self.charencode(miwen_all)),end=' ')
        print(self.charencode(miwen_all)) 
        print("推荐使用sage计算密钥K,以下输出sage代码")
        print("参考[UTCTF2020]hill.pdf")
        print("# please run in sage")
        def format(x):
            return str(x).replace(' ',',').replace('\n',',').replace(',,',',').replace('[,','[')
        print("# 理论上要用2*2的正方形矩阵C和M，手动改下")
        C = np.array(self.charencode(miwen)).reshape(self.H, len(miwen)//self.H)
        print("C = Matrix("+format(C.T)+")")
        M = np.array(self.charencode(mingwen)).reshape(self.H, len(mingwen)//self.H)
        print("M = Matrix("+format(M.T)+")")
        print("K = C*M.inverse()%26")
        print("print(K)")
        # print("K_inv = K.inverse()%26")
        # print("print(K_inv)")
        # print("# 得到K逆向矩阵后以下代码求解原文")

    def printSageCode2(self,miwen_all,mingwen,miwen,key):
        def format(x):
            return str(x).replace(' ',',').replace('\n',',').replace(',,',',').replace('[,','[')
        print("# 结合爆破得到的一个或多个key，利用密文求解明文")
        print("# 当key = "+key+"时")
        K = np.array(self.charencode(key)).reshape(self.H, len(key)//self.H)
        print("# K = Matrix("+format(K)+") #这里可以直接修改用爆破得到的密钥")
        print("K_inv = K.inverse()%26")
        print("s = '"+self.chardecode(self.charencode(miwen_all))+"'")
        print("ans = ''")
        print("for i in range(0,len(s),2):")
        print("    T = Matrix([[ord(s[i]) - 97], [ord(s[i + 1]) - 97]])")
        print("    R = K_inv * T%26")
        print("    ans += chr(R[0][0] + 97) + chr(R[1][0] + 97)")
        print("print(ans)")

def Hill_key_burp(miwen_all,flag):
    print("-"*20+color_string("[尝试Hill希尔解码]",PURPLE)+"-"*20)   
    if len(miwen_all) > 200:
        choose= input("输入字符较长，为避免刷屏，请确认是否继续，输入N/n退出，任意字符继续:")   
        if choose == "N" or choose == "n":
            return     
    miwen_all_all = miwen_all
    pre = HillCipherBreaker()
    miwen_all = pre.chardecode(pre.charencode(miwen_all))
    print("去除密文中的非字典字符，得到原始密文:"+ miwen_all)
    if len(flag) % 2 > 0:
        print("输入的已知明文非偶数，不符合Hill加密，如果确认是Hill加密，请直接尝试修改Hill_key_burp.py")
        return 
    mingwen = flag # 已知明文，提示必须时2的倍数
    miwen = miwen_all[0:len(flag)] # 默认根据全部密文提取前len(mingwen)个字符，实际以获取的输入为准
    if len(mingwen)%2 == 0:
        try:
            # 根据提供的成对的已知密文与猜测明文
            breaker = HillCipherBreaker(mingwen,miwen,miwen_all,miwen_all_all)
            breaker.run()
        except:
            pass
def sage(miwen_all,flag):
    if len(flag) < 4:
        print("明文太短，sage无解")
        return
    print("以下开始一个sage解题demo，默认使用了明文前4个字符")
    # miwen_all="oxks{yuzkuidnbrzkbmqrlr}"  # 从主函数继承全部密文
    print("原始密文"+miwen_all)
    pre = HillCipherBreaker()
    miwen_all = pre.chardecode(pre.charencode(miwen_all))
    print("去除密文中的非字典字符，得到原始密文:"+ miwen_all)
    mingwen = flag[0:4] # 要求输入已知明文，提示必须时2的倍数
    miwen = miwen_all[0:len(mingwen)] # 默认根据全部密文提取前len(mingwen)个字符，实际以获取的输入为准
    # 要求输入keys
    # 根据爆破结果要求输入可能的密钥key列表
    pre.printSageCode1(miwen_all,mingwen,miwen,'')
    keystr = "ntyd"
    keys = [i.strip() for i in keystr.split(',')]
    for key in keys:
        if len(key) %2 == 0:
            pre.printSageCode2(miwen_all,mingwen,miwen,key)   


if __name__ == "__main__":
    # Hill_key_burp("wznqca{d4uqop0fk_q1nwofDbzg_eu}",'utflag')  # 从主函数继承全部密文
    Hill_key_burp("oxks{yuzkuidnbrzkbmqrlr}",'flag')  # 从主函数继承全部密文    
    # 如果确认hill加密，且密码不是2*2，请看到这里的sage代码提示，尝试修改
    print()
    print()
    print()
    print()
    print()
    print()
    sage("oxks{yuzkuidnbrzkbmqrlr}",'flag')
    # sage("wznqca{d4uqop0fk_q1nwofDbzg_eu}",'utflag')  # utflag
