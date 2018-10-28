#encoding=utf-8
import hashlib

def md5_encrypt(text):
    m5=hashlib.md5()#实例化一个md5的实例
    m5.update(text)#处理text加密
    value=m5.hexdigest()
    return value

if __name__ == '__main__':
    print "md5 encrypt of 'xiaxiaoxu':",md5_encrypt('xiaxiaoxu')