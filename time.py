#encoding=utf-8
import time

class MyTimer:

# 开始时间
    def start(self):
         self.start=time.localtime()
         print ("计时时间开始：")
# 停止计时
    def stop(self):
         self.stop=t.localtime()
         print ("计时时间结束")
         self._calc=()
         print ("计时结束")
    def _calc(self):
        self.lasted =[]
        self.prompt ="总共运行了："
        for index in range(6):
            self.lasted.append(self.stop[index]-self.start[index])
            self.prompt += str(self.lasted[index])
        print (self.prompt)




