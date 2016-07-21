# -*- coding: utf8 -*-
import threading, time, http.client

HOST = 'www.baidu.com' #主机地址
PORT = 80  #端口号
URI = "/"  #URI地址
TOTAL = 0   #总数
SUCC = 0    #成功数
FAIL = 0    #失败数
EXCEPT = 0   #报错数
MAXTIME = 0   #最大响应时间
MINTIME = 100  #最小响应时间
GT3 = 0       #响应时间大于3s次数
LT3 = 0       #响应时间小于3s次数

class RequestThread(threading.Thread):
    def __init__(self,thread_name):
        threading.Thread.__init__(self)
        #self.test_count = 0

    def run(self):
        self.test_performance()

    def test_performance(self):
        global TOTAL, SUCC , FAIL, EXCEPT, GT3, LT3
        try:
            st = time.time() #获取当前时间的时间戳
            conn = http.client.HTTPConnection(HOST,PORT)
            conn.request('GET',URI)
            res = conn.getresponse()
            if res.status == 200:
                TOTAL += 1
                SUCC += 1
            else:
                TOTAL += 1
                FAIL += 1
            time_span = time.time() - st  #计算响应时间
            self.maxtime(time_span)
            self.mintime(time_span)
            print('%s:%f\n'%(self.name,time_span))
            if time_span > 3:
                GT3 += 1
            else:
                LT3 += 1
        except Exception as e:
            print(e)
            TOTAL += 1
            EXCEPT += 1
        conn.close()

    def maxtime(self,ts):
        global MAXTIME
        if ts > MAXTIME:
            MAXTIME = ts

    def mintime(self,ts):
        global MINTIME
        if ts < MINTIME:
            MINTIME = ts

print("========task start========")
start_time = time.time()
thread_count = 100   #设置并发数
threads = []

for i in range(thread_count):
    t = RequestThread("thread"+str(i+1))
    t.start()
    threads.append(t)

# 等待所有线程完成
for t in threads:
    t.join()

total_time = time.time() - start_time
print("========task end=======")
print("total time:",total_time)
print("total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT))
print('response maxtime:',MAXTIME)
print('response minitime:',MINTIME)
print("great than 3 seconds:%d,percent:%0.2f"%(GT3,float(GT3)/TOTAL))
print("less than 3 seconds:%d,percent:%0.2f"%(LT3,float(LT3)/TOTAL))


