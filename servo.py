##Andrew Plesniak
##2/15/19
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
    locked = 700 #values were found via experimentation based on what values cuase the door to unlock
    unlocked = 1925 

    ##Setup and Config
    bus.write_byte_data(addr, 0, 0x20) #enable the chip
    time.sleep(0.25)
    bus.write_byte_data(addr, 0, 0x10) #enable Prescale change as noted in the datasheet
    time.sleep(0.25) #delay for reset
    bus.write_byte_data(addr, 0xfe, 0x11) #changes the Prescale register value for 333Hz, using the equation in the datasheet
    bus.write_byte_data(addr, 0, 0x20) #enable the chip

    ##Initalize
    state = locked
    bus.write_byte_data(addr, 0x06, 0) #ch0 start time = 0s
    
    while True:
        x=stdscr.getch()
        if x == curses.KEY_LEFT:
            state = locked
            print("Locked")
        elif x == curses.KEY_RIGHT:
            state = unlocked
            print("Unlocked")

        bus.write_word_data(addr, 0x08, state) #writes to the stop address of Ch0   

try:
    curses.wrapper(main)
    
except KeyboardInterrupt:
    print('User Ended Program')
    bus.write_word_data(0x40, 0x08, 0) #writes to the stop address of Ch0



