# checkascii
## 安装
```shell
python3 -m pip install -r requirement.txt
```
## 使用说明
```
  -h, --help  显示帮助信息
  -f, --file  读取txt文本，不区分换行
  -t, --txt   读取输入字符串

  例1：python3 checkascii.py -t "348ufrf4rt34rufdvzcvrt34rhfdshaskasff&)*)%&^"
       --------------------直接检测输入字符串---------------

  例2：python3 checkascii.py -f ./testfile.txt
       --------------------读取指定文件并检测-------------------
```
## 支持的功能
1. Base全家桶
2. 字频统计
3. 云影密码
4. 曼彻斯特
5. 普通栅栏和W型栅栏
6. 仿射爆破解码
7. 希尔爆破解码
8. 维吉尼亚解码/字典攻击/简单明文攻击
9. 仿射+维吉尼亚攻击
## 实例    
```shell
python3 checkascii.py -t "H4sIAAAAAAAAAFvz1oG1uThBNzk/V68otbgON7UYg87NTOnNOQsC85zzS/NKgt9/nfvHul6ZiYHRi4G1LDGnNLWigAECGAGGalhyUgAAAA=="

python3 checkascii.py -f shanghai.txt

python3 checkascii.py -f vigenere.txt
```
