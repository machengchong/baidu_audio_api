from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QFileDialog
from au import Ui_MainWindow
import requests
import json
import base64
import os
from pyaudio import PyAudio,paInt16
import wave
import sys

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
fileName = ""
API_Key = "bPw8CNwGWvaC0UnIXDXHG27C"
Secret_Key = "sAGtXlP6mGGRcmChtIb14p6lUklkLaS2"

def get_baidu_token(API_Key,Secret_Key):
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        "grant_type" : "client_credentials",
        "client_id" : API_Key,
        "client_secret" :Secret_Key
    }
    r = requests.post(url, data=data).json()
    print(r["access_token"])
    return r["access_token"]

def get_baidu_api(au_name,token):

    #读取文件并转换为base64格式
    wav_name = open(au_name, "rb")
    wav_base64 = base64.b64encode(wav_name.read())
    wav_name.close()
    wav_base64_str = str(wav_base64, encoding="utf-8")
    #获取文件字节数
    wav_len = os.path.getsize(au_name)

    url = "http://vop.baidu.com/server_api"
    headers = {'Content-Type': 'application/json'}
    data = {
                "format": "wav",
                "rate": 16000,
                "dev_pid": 1537,
                "channel": 1,
                "token": token,
                "cuid": "527424",
                "len": wav_len,
                "speech": wav_base64_str
            }
    data_json = json.dumps(data)
    r = requests.post(url, data=data_json, headers=headers).json()
    print(r)
    if r["err_msg"] == "success.":
        print(r["result"])
        return r["result"]
    else:
        print(["error"])
        return ["error"]

def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


class pyqt5_main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(pyqt5_main,self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("语音识别")
        self.fileName = ""

    def init(self):
        self.pushButton.clicked.connect(self.inputaudio)

        self.pushButton_2.clicked.connect(self.openfile)

        self.pushButton_3.clicked.connect(self.showtxt)

        self.pushButton_4.clicked.connect(self.outtxt)

    def openfile(self):
        self.fileName,filetype = QFileDialog.getOpenFileNames(self, "选取文件", "./",
                                                          "All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
        print("\n你选择的文件为:")
        print(self.fileName[0])
        print("文件筛选器类型: ", filetype)


    def inputaudio(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1,
                         rate=framerate, input=True,
                         frames_per_buffer=NUM_SAMPLES)
        my_buf = []
        count = 0
        print('录音开始')
        while count < TIME * 10:  # 控制录音时间
            string_audio_data = stream.read(NUM_SAMPLES)  # 一次性录音采样字节大小
            my_buf.append(string_audio_data)
            count += 1
            print('.')
        save_wave_file('01.wav', my_buf)
        self.fileName = ['01.wav']
        print("录音结束")
        stream.close()

    def showtxt(self):
        #self.textBrowser.setText(self.fileName)
        token = get_baidu_token(API_Key, Secret_Key)
        self.get_text = get_baidu_api(self.fileName[0], token)
        self.textBrowser.setText(self.get_text[0])

    def outtxt(self):
        outname = 'write_data.txt'
        with open(outname, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(self.get_text[0])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = pyqt5_main()
    myshow.show()
    sys.exit(app.exec_())