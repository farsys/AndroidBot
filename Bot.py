#from curse import window
from optparse import Option
import os
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
from ui_interactor import UI_interact as uic

selected_device=''

device1= Devices(55329,0)
device2= Devices(64650,1)
window_name='Farm0'
t_Img = Targe_Imagen()
s_img= Source_imagen(window_name)
ui =uic(window_name,device1)


#s_img= Source_imagen('MafiaMain')


def rand(start,range):
   return np.random.uniform(start,range)




def hollowing_event():
    t_image_list =t_Img.get_imagen_list('./Targets/Events/Hollowen/')
    #t_special_image_list =t_Img.get_imagen_list('./Targets/Events/Hollowen/Special/')
    #t_ui_image_list =t_Img.get_imagen_list('./Targets/Events/Hollowen/UI/')
    s_img.get_screen()

    play_count=0
    max_play_count=0

    max_play_count =int(input('How many times do you want to play:'))
    while play_count <max_play_count:
        
        play_count =play_count+1
        #img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        continuebt =cv.imread('./Targets/Events/Hollowen/UI/continue.png',0)
        scorebt=cv.imread('./Targets/Events/Hollowen/UI/score.png',0)
        hardmodebt=cv.imread('./Targets/Events/Hollowen/UI/HardMode.png',0)
        no_tickets=cv.imread('./Targets/Events/Hollowen/UI/no_cards.png',0)
        
        sleep (3)
        print('looking for continue bt')
        if (t_Img.isTheImageThere(continuebt,s_img.get_screen(),0.8)== True  ):
            device.send_click(250,655)
            sleep (3)
            device.send_click(150,520)
        print('looking for hard mode bt')
        if (t_Img.isTheImageThere(hardmodebt,s_img.get_screen(),0.8)== True):
            sleep (2)
            device.send_click(250,570)
            sleep (2)
            device.send_click(150,520)
       
        sleep (1)

        print('cheking for tickets')
        if (t_Img.isTheImageThere(no_tickets,s_img.get_screen(),0.9)== True):
            print('No tickets ')
            ui._go_to_Turf()
        #     break
        #hprint (score)
        #score =t_Img.isTheImageThere(scorebt,image_screen,0.9)
        sleep (1)

        print('Playing')
        while  t_Img.isTheImageThere(scorebt,s_img.get_screen(),0.9) == True:
           #h print('playing')

           
            #score =t_Img.isTheImageThere(scorebt,image_screen,0.92)

           
            t_Img.find_img_to_Click(cv.imread('./Targets/Events/Hollowen/Special/p1.png',0),s_img.get_screen(),device,0.80,10,rand(0.0001,0.0005))
           
            
            t_Img.find_img_to_Click(cv.imread('./Targets/Events/Hollowen/Special/cc1.png',0),s_img.get_screen(),device,0.80,1,rand(0.0001,0.0005))
           

            for i2 in t_image_list:
                t_Img.find_img_to_Click(i2,s_img.get_screen(),device,0.80,1,rand(0.0001,0.0005))

            #print (score)
            if(kb.is_pressed('c')==True):
            #cv.destroyAllWindows()
                print('Hollowing Ended')
                break

        #t_Img.find_a_destroy(t_ui_image_list,img_gray,device,0.75,1,delay=rand(0.45,0.6))




        if(kb.is_pressed('c')==True):
            #cv.destroyAllWindows()
            print('Hollowing Ended')
            break
            #break
    print('Hollowing Event Completed| Played:'+ str( play_count))       
    ui._go_to_Turf()


def street_wars():
    image_screen = s_img.get_screen()
   
    search_bt=cv.imread('./Targets/Street War/UI/stw.png',0)
    ref_bt=cv.imread('./Targets/Street War/UI/ref.png',0)

    t_image_list =t_Img.get_imagen_list('./Targets/Street War/')



    if (t_Img.isTheImageThere(search_bt,image_screen,0.9)== True  ):
            device.send_click(500,721)
    sleep(5)
    image_screen = s_img.get_screen()
   
    while (t_Img.isTheImageThere(ref_bt,image_screen,0.9)== True):
        image_screen = s_img.get_screen()
        while True:
            t_Img.find_a_destroy(t_image_list,image_screen,device,0.80,rand(2,4))

    print ('street wars ended')


def street_forces():
    # image_screen = s_img.get_screen()
   
    # sf_bt=cv.imread('./Targets/Street War/UI/sf.png',0)
    count_all =0
    units_dispached =0
    #while True:
    print('starting Street Forces')
    _try=0
    
    while True:
        units_dispached =0
        if (ui._do_I_out_energy()== True):
            print('No Enough Energy go to sleep')
            sleep(10) 
       
        sleep(1)
        if (ui._inMap() != True):
            ui._go_to_map()

        while units_dispached <= 3:
            
            # if (ui._do_I_Out_Ops()== True):
            #     print('No Avaible Ops')
            #     break2

            if (ui._do_I_out_energy()== True):
                print('No Enough Energy')
                break
                
               # break
            sleep(1)
            print('Opening Map Search')
            if (ui._open_map_search()== True ):
                sleep(1)

                
                ##i need to see if i found something
                ui._select_street_forces()
                sleep(2)
                if (ui._dispach_troops()==True):
                    units_dispached = units_dispached +1
                    count_all = count_all+1
                    print('Units Dispached: '+str(units_dispached))

                        #check if the search failed
                else:
                    ui._go_to_map()
        print('ops out: Total ops: '+ str(count_all))
        sleep(1)
        if(kb.is_pressed('c')==True):
            #cv.destroyAllWindows()
            print('treet Forces has Ended')
            break

    #ui._go_to_Turf()
    #print ('street Forces ended:total Ops'+ str(units_dispached))
    #return units_dispached
    

 #look for targets
           #image_screen = s_img.get_screen()
            # if (t_Img.isTheImageThere(sf_bt,image_screen,0.9)== True  ):
            #     #if (t_Img.isTheImageThere(avatar_bt,image_screen,0.9)!= True):
            #     if(_try<2):
            #         _try = _try+1
            #         print('Trying1 Lower Forces- tries: '+str(_try))
            #         device.send_click(116,820)
            #     else:
            #         device._goBack()
            #         print('No Forces found')
                    
            #         break
            #     sleep(2)
            #         #device.send_click(30,30)
            # else:



                #accept go
                # #go
                # device.send_click(270,685)
                # sleep(1)
                
                # if (ui._inTroopsMenu()== True):
                #     print('selecting formation')
                #     device.send_click(450,335)
                #     sleep(1)
                #     print('dispathing troops')
                #     device.send_click(430,925)
                    
                #     units_dispached = units_dispached+1
                #     print('Units Dispached: '+str(units_dispached))
                # else:
                #     #go Back
                #     image_screen = s_img.get_screen()
                #     if (ui._inMap()!= True):
                #         ui._go_to_map(device)
                       
                #         break
                #         #sleep(200)
                # sleep(3)
                #print('Street Forces has has been dispached')
            
                

        #sleep(3)



def collect_resorces():
    print('starting resources collection')
    t_image_list_resources =t_Img.get_imagen_list('./Targets/Resouces/')
    #t_special_image_list =t_Img.get_imagen_list('./Targets/Events/Hollowen/Special/')
    #t_ui_image_list =t_Img.get_imagen_list('./Targets/Events/Hollowen/UI/')
    s_img.get_screen()

  
    print('Cheking ubication')
    if (ui._inturf()!= True  ):
        print("tring to find turf")
        ui._go_to_Turf()
        sleep(5)
            


    image_screen = s_img.get_screen()
            #img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY
            
                #in tuf
    print ('Searching for resources')
    image_screen = s_img.get_screen()
    while( t_Img.find_img_list_Click(t_image_list_resources,image_screen,device,0.9)==False):
        print('No Resources Found')
        break


    print('Collection completed')

    
            

        
    if(kb.is_pressed('c')==True):
        #cv.destroyAllWindows()
        print('Collection Ended')
        return 0


def collectCrops():
    pass

def clanContribuite():
    pass




def _menu():
   
    print('Current Device: '+ window_name)
    print('-'*20)
    print('Felix Bot 1.0')
    print('='*20)
    print('')
    print('Press [H] : Hollowin Event')
    print('Press [W] : Street Wars')
    print('Press [F] : Street Forces')
    print('Press [R] : Collect Resources')
    print('-'*20)
    print('Press [Q] : Quit')
    print('-'*20)
    # print('Press [1] : Farm1')
    # print('Press [2] : Farm0')
    print('')



#device= Devices(62689,1)

    return False
print('-'*20)
print('----Chose a Device:----')
print('-'*20)
print('Device:#1 : Main')
print('Device:#2 : Farm1')

option =int(input('Chose a Device#: '))

if(option ==1):
    device= device1
    window_name='Farm0'
    t_Img = Targe_Imagen()
    s_img= Source_imagen(window_name)
    ui =uic(window_name,device)

if(option==2):

    device= device2
    window_name='Farm1'
    t_Img = Targe_Imagen()
    s_img= Source_imagen(window_name)
    ui =uic(window_name,device)

else:
    print('Invalid option')


_menu() 

option =str(input('Select One: '))

while option !='q':
    if(option== 'h'):
        print('Hollowing selected')
        hollowing_event()
    if(option== 'w'):
        print('Street Wars selected')
        street_wars()
    if(option== 'f'):
        print('Street Forces selected')
        street_forces()
    if(option== 'r'):
        print('Collect Resources')
        collect_resorces()
    #if(option== '1'):
     #   print('Device  1 farm1')
            
   # if(option== '2'):
    #    print('Device  2 Farm 0')
        # device = Devices(62689,1)
        # window_name='Farm0'
        # selected_device = 'Farm0'
        # s_img= Source_imagen(window_name,False)
        # ui =  uic(window_name,device)
        

        
    sleep(.1)
    _menu()
    option =str(input('Select One: '))

    #print(selected_device)
    if(kb.is_pressed('q')==True):
        print('Bot Ended')
        break
