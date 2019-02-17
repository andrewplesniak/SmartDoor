##Andrew Plesniak
##2/15/18
##This program controls a 270 degree, 333Hz servo motor based on Keyboard input

import smbus
import time
import curses
from random import randint

def main(stdscr):
    stdcr =curses.initscr()
    global bus
    bus = smbus.SMBus(1)
    addr = 0x40
    minvalue1 = 682 #values were found via experimentation based on rotational limits
    maxvalue1 = 3409 #roughly equiv to 0.5ms to 2.5ms
    stepsize = 3    #increase to increase speed

    ##Setup and Config
    bus.write_byte_data(addr, 0, 0x20) #enable the chip
    time.sleep(0.25)
    bus.write_byte_data(addr, 0, 0x10) #enable Prescale change as noted in the datasheet
    time.sleep(0.25) #delay for reset
    bus.write_byte_data(addr, 0xfe, 0x11) #changes the Prescale register value for 333Hz, using the equation in the datasheet
    bus.write_byte_data(addr, 0, 0x20) #enable the chip

    ##Initalize
    angle1 = int(round((minvalue1+maxvalue1)/2))
    bus.write_byte_data(addr, 0x06, 0) #ch0 start time = 0s
    
    while True:
        x=stdscr.getch()
        if x == curses.KEY_LEFT and (angle1 + stepsize) < maxvalue1:
            angle1 = angle1 + stepsize
            print(angle1)
        elif x == curses.KEY_RIGHT and (angle1 - stepsize) > minvalue1:
            angle1 = angle1 - stepsize
            print(angle1)

        bus.write_word_data(addr, 0x08, angle1) #writes to the stop address of Ch0   

try:
    curses.wrapper(main)
    
except KeyboardInterrupt:
    print('User Ended Program')
    bus.write_word_data(0x40, 0x08, 0) #writes to the stop address of Ch0



