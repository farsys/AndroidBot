
from operator import truediv
import os
from turtle import goto
from xmlrpc.client import TRANSPORT_ERROR
import PIL as pil
from ppadb.client import Client as AdbClient
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from time import time, sleep
from mss import mss
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from PIL import ImageGrab
from Imagen import *
import keyboard as kb
from devices import Devices
import random






#s_img= Source_imagen('MafiaMain')
#device= Devices(53797,0)
class UI_interact:

    img =Targe_Imagen()
    screen= Source_imagen('Farm1')
    device= None

    def __init__(self,screen_name,device) -> None:
        self.screen =Source_imagen(screen_name)
        self.device = device


#validators
    def _inturf(self):
       
        imagen_list=self.img.get_imagen_list('./Targets/UI/InTurf/')

        sleep (2)
        
        res= self.img.isaImgThereFromList(imagen_list,self.screen.get_screen(),0.9)
        #fromdevice=True,device=self.device
        return res


    def _inMap(self):
        imagen_list=self.img.get_imagen_list('./Targets/UI/OnMap/')
        
        res= self.img.isaImgThereFromList(imagen_list,self.screen.get_screen(),0.8)

        return res

    def _inClan_screen(self):
        return False

    def _inTroopsMenu(self):
        imagen_list=self.img.get_imagen_list('./Targets/UI/TroopsMenu/')
        
        res= self.img.isaImgThereFromList(imagen_list,self.screen.get_screen(),0.8)
        return res


    def _inHollowing_even_screen(self):
        return False

    def _inHollowing_even_screen_playing(self):
        return False


    def _inStreetWar_screen(self):
        return False


    def _do_I_out_energy(self):

        imagen=cv.imread('./Targets/UI/Others/energy2.png',0)
        res =self.img.isTheImageThere(imagen,self.screen.get_screen(),0.8)
        return res
   
    def _do_I_Out_Ops(self):

        imagen=cv.imread('./Targets/UI/Others/noOps3.png',0)
        res =self.img.isTheImageThere(imagen,self.screen.get_screen(),0.8) 
        return res


    def _do_i_have_currency(self):
        return False

    def _do_have_ready_troops(self):
        imagen_list=self.img.get_imagen_list('./Targets/UI/ReadyTroops/')

        res= self.img.isaImgThereFromList(imagen_list,self.screen.get_screen())
        
        return res


    #def _goTo_map_search(self,device):
       

#movers
    def _go_to_Turf(self):

        while self._inturf() != True:
            self.device._goBack()
            sleep (2)

        

    def _go_to_map(self):
       
        while  self._inMap() != True:
            
            if self._inturf() ==True:
                self.device.send_click(55,921)
                sleep(2)
            else:
                if( self._inMap() != True):
                    self._go_to_Turf()

            
            #print( self._inMap())

    def _go_toclan(self):
        pass


    def _go_garden(self):
        pass


    def look_for_resources(self):
        pass


    def _select_street_forces(self):
        sleep(1)
        print('Selecting Street Forces')
        self.device.send_click(83,700)
        sleep(1)

        print('Searching for Street Forces')
        self.device.send_click(272,900)
        sleep(1)
    
    def _dispach_troops(self):
        imagen_list_attack=self.img.get_imagen_list('./Targets/UI/Combat/Attack/')
        #img_search2= cv.imread('./Targets/UI/Others/search_for_target.png',0)
        res = False
        tryAgain=0
        #looking for Go or Attack Botton
        while True:
            if self.img.isaImgThereFromList(imagen_list_attack,self.screen.get_screen())== True or tryAgain <3:
                sleep(0.1)
                self.device.send_click(270,685)
                break
            else:
                self._open_map_search()
                self._select_street_forces()
                tryAgain =tryAgain +1
            #
            #

            
            #sleep(1)
       
        #looking for troop dispach menu
        tryAgain=0
        #sleep(1)
        #while True:
        if(self.img.isTheImageThere(cv.imread('./Targets/UI/Others/noOps.png',0), self.screen.get_screen())==True):
            print('Probably no ops going to sleep')
            self._go_to_map()
            sleep (30)
            return False

        while True:
            if self._inTroopsMenu() == True:
                tryAgain =tryAgain +1
                print('Selecting Formation')
                sleep(1)
                self.device.send_click(450,335)
                sleep(1)
                print('Dispathing Troops')
                self.device.send_click(430,925)
                sleep(1)

                if(self._inMap()==True):
                    print('Ops have been dispached')
                    res= True
                    break
                    
                else:
                    print('Ops Ended')
                    # self._go_to_map()
                    res= False
                    break

                #if (tryAgain >=3):
                    #   break
            else:
                self._open_map_search()
                self._select_street_forces()
                res= False
                break
            sleep(0.5)

        return res
        
    def _open_map_search(self):
        print('1')
        img_search= cv.imread('./Targets/UI/OnMap/search.png',0)
        img_search2= cv.imread('./Targets/UI/Others/search_for_target.png',0)
        while True:
            print('2')
            sleep(1)
            if(self._inMap()== True):
                print('3')
                if (self.img.isTheImageThere(img_search,self.screen.get_screen(),0.85)== True  ):
                    sleep(1)
                    self.device.send_click(32,617)
                    sleep(1)
                    while True:
                        print('4')
                        sleep(2)
                        if (self.img.isTheImageThere(img_search2,self.screen.get_screen(),0.85)== True  ):
                            print('5')
                            return True
                        else:
                            sleep(1)
                            print('5.5')
                            self.device.send_click(32,617)
                       
                        #self.device.send_click(32,614)
            else:
                print('6')
                self._go_to_map()
        print('7')
        return False




    def _dispache_street_forces_2(self):
        count =0
        while True:

           if (self._inMap()==True):
            count=count+1
            if count <=3:
                sleep(1)
            else:
                self._go_to_map()