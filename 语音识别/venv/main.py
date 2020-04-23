import requests
import json
import base64
import os
from PyQt5.QtWidgets import QFileDialog
import tkinter as tk
from tkinter import filedialog

from pyaudio import PyAudio,paInt16
import wave

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2

#调用百度语音识别api  技术文档：https://cloud.baidu.com/doc/SPEECH/s/ek38lxj1u
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
        print("error")
        return "error"


#获取百度token，以调用百度api
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

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    print('录音开始')
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)#一次性录音采样字节大小
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('01.wav',my_buf)
    print("录音结束")
    stream.close()

if __name__ == "__main__":
    #从百度中获取
    API_Key = "bPw8CNwGWvaC0UnIXDXHG27C"
    Secret_Key = "sAGtXlP6mGGRcmChtIb14p6lUklkLaS2"

    #获取token
    token = get_baidu_token(API_Key,Secret_Key)

    #打开文件
    #root = tk.Tk()
    #root.withdraw()
    #file_path = filedialog.askopenfilename()
    #print(file_path)

    #录音开始
    my_record()


    #fileName, ftype = QFileDialog.getOpenFileNames(None, "选取文件", "./","All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
    
    #解析音频文件
    get_baidu_api('F:/大三/多媒体通信/实验/实验八/语音识别/venv/01.wav' ,token)