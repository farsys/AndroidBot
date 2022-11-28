from PIL import Image
import numpy
import time
import os
from ppadb.client import Client as AdbClient
import random as rn

class Devices:
    device = AdbClient.device


    def __init__(self,aport,dindex):
        os.system('cmd /c ":\ADB>adb connect 127.0.0.1:'+str(aport)+'"')

        #print('Connecting ...')
        client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

        devices = client.devices()
      
        client.remote_connect('127.0.0.1',aport)
        self.device = devices[dindex]
        #return (device)

    def send_click(self,x,y):
        self.device.shell(f'input tap '+ str(x+rn.randrange(0,1,1))+' '+str(y+rn.randrange(0,2,1)))

    def _goBack(self):
        self.device.shell(f'input keyevent 4')
        
    def _grabScreen(self):
      return  self.device.screencap()
        


