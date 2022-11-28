import os
from pickle import FALSE
from turtle import Screen
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from PIL import ImageGrab
import numpy as np
import win32con
import cv2 as cv
from time import time, sleep
import pygetwindow
import random as rn

class Source_imagen:
    debuging =False
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name,deb =False):
       
        self.debuging =deb
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
  

        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screen(self):


        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        #debug
        # convert the raw data into a format opencv can read
        if (self.debuging== True):
            dataBitMap.SaveBitmapFile(cDC, 'screen.png')


        signedIntsArray = dataBitMap.GetBitmapBits(True)
        #ataBitMap.SaveBitmapFile('')
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)
        
       # print('finsh')
        return img




class Targe_Imagen:

    # folder path
    
   


    def __init__(self):
       pass

    def get_imagen_list(self,dir_path):
        res = []
        # list to store files
                 
        # Iterate directory
        for file in os.listdir(dir_path):
            # check only text files
            if file.endswith('.png'):
                res.append( cv.imread(dir_path+file,0))
            #res.append(file)
        return(res)


    def  find_img_list_Click(self,image_list,img_screen,device, threshold=0.9,times_click=1,delay=0.005,fromdevice=False):
        
        count =0
       
        img_gray = cv.cvtColor(img_screen, cv.COLOR_BGR2GRAY)

        for i in image_list:
            w, h = i.shape
            res = cv.matchTemplate(img_gray,i,cv.TM_CCOEFF_NORMED)
            threshold = threshold
            loc = np.where( res >= threshold)
            retangle =[]
            for pt in zip(*loc[::-1]):
                retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
                retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
            # print (pt)
            #print(len(retangle))
            retangle, weight =cv.groupRectangles(retangle,groupThreshold=1, eps=0.5)

            for (x,y,w,h) in retangle:
                count = count +1
                #cv.rectangle(img_screen, (x,y), (x+w, y+h), (0,255,0), 2)
                click=0
                while click < times_click:
                    device.send_click((x+(w/2)) ,(y+(h/2)))
                    click=click+1
                    sleep(delay)
            
           # cv.imshow('Test',img_screen)
           # cv.waitKey(3)
        #print(len(retangle))
        if count >=1:
            return True
        else:
            return False

        


    def  find_img_to_Click(self,img_target,img_screen,device, threshold=0.9,times_click=1,delay=0.005,):
        
        count =0
       
        img_gray = cv.cvtColor(img_screen, cv.COLOR_BGR2GRAY)

       
        w, h = img_target.shape
        res = cv.matchTemplate(img_gray,img_target,cv.TM_CCOEFF_NORMED)
        threshold = threshold
        loc = np.where( res >= threshold)
        retangle =[]
        for pt in zip(*loc[::-1]):
            retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
            retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
        # print (pt)
        #print(len(retangle))
        if len(retangle) > 0:
            retangle, _ =cv.groupRectangles(retangle,groupThreshold=1, eps=0.5)
            
            for (x,y,w,h) in retangle:
                
                #cv.rectangle(img_screen, (x,y), (x+w, y+h), (0,255,0), 2)
                click=0
                while click < times_click:
                    device.send_click((x+(w/2)) ,(y+(h/2)))
                    click=click+1
                    sleep(delay)
            
           # cv.imshow('Test',img_screen)
           # cv.waitKey(3)
        #print(len(retangle))
       

                
    def  isaImgThereFromList(self,image_list,img_screen, threshold=0.9,times_click=1,delay=0.005):
        Screen
        # if(fromdevice==True):
        #     image =device.screencap()
        #     image = cv.imdecode( np.frombuffer(image,dtype=np.uint8),cv.IMREAD_COLOR)
        #    # img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # else:
        #     image=img_screen
        img_gray = cv.cvtColor(img_screen, cv.COLOR_BGR2GRAY)
        count=0
        for i in image_list:
            w, h = i.shape
            res = cv.matchTemplate(img_gray,i,cv.TM_CCOEFF_NORMED)
            loc = np.where( res >= threshold)
            #print (loc)
            retangle =[]
            for pt in zip(*loc[::-1]):
                retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
            # print (pt)

            for (x,y,w,h) in retangle:
                count = count +1
                cv.rectangle(img_screen, (x,y), (x+w, y+h), (0,255,0), 2)
                
            #cv.imshow('Test',img_screen)
            #cv.waitKey(1)
        if count >=1:
               
            return True
        else:
            return False
        
        

        



    def  isTheImageThere(self,target_img,img_screen, threshold=0.9,fromdevice=False,device=None):
        
        # if(fromdevice==True):
        #     img_gray = cv.cvtColor(device.screencap(), cv.COLOR_BGR2GRAY)
        # else:
        img_gray = cv.cvtColor(img_screen, cv.COLOR_BGR2GRAY)

        res= cv.matchTemplate(img_gray,target_img,cv.TM_CCOEFF_NORMED)
        _, max_conf, _, max_loc_target = cv.minMaxLoc(res)
        #print(max_conf,)
        
        ## test

        w, h= target_img.shape[::-1]
        loc = np.where( res >= threshold)
        retangle =[]
        for pt in zip(*loc[::-1]):
                retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
        for (x,y,w,h) in retangle:
                cv.rectangle(img_screen, (x,y), (x+w, y+h), (0,255,0), 2)
        #end test   
       # cv.imshow('Test',img_screen)
       # cv.waitKey(1)

        if max_loc_target is not None and max_conf >=threshold:
            return True
        else:
            return False


    def is_there_by_cordenates(self,x,y):
        pass

        







"""  def  find_and_click_nouse(self,image_list,source_img,device, threshold,times_click=1,delay=0.005):
        for i in image_list:
            w, h = i.shape[::-1]
            res = cv.matchTemplate(source_img,i,cv.TM_CCOEFF_NORMED)
            threshold = threshold
            loc = np.where( res >= threshold)
            retangle =[]
            for pt in zip(*loc[::-1]):

                retangle.append([int(pt[0]),int(pt[1]),int(w),int(h)])
            # print (pt)
            retangle, weight =cv.groupRectangles(retangle,groupThreshold=1, eps=0.5)

            for (x,y,w,h) in retangle:
                cv.rectangle(source_img, (x,y), (x+w, y+h), (0,255,0), 2)
                click=0
                while click < times_click:
                    device.send_click((x+(w/2)) ,(y+(h/2)))
                    click=click+1
                    sleep(delay) """