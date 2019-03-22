##Andrew Plesniak
##3/22/19
##This clas provides the ability to unlock and lock the door for the Smart Door project

import smbus
import time

class door ():
	def __init__():
		self.bus = smbus.SMBus(1)
		self.addr = 0x40
		self.locked = 700 #values were found via experimentation based on what values cuase the door to unlock
		self.unlocked = 1925 

		##Setup and Config
		bus.write_byte_data(self.addr, 0, 0x20) #enable the chip
		time.sleep(0.25)
		bus.write_byte_data(self.addr, 0, 0x10) #enable Prescale change as noted in the datasheet
		time.sleep(0.25) #delay for reset
		bus.write_byte_data(self.addr, 0xfe, 0x11) #changes the Prescale register value for 333Hz, using the equation in the datasheet
		bus.write_byte_data(self.addr, 0, 0x20) #enable the chip

		##Initalize
		self.state = self.locked
		bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   

	def unlock(self):
		self.state = self.unlocked
		bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   

	def lock(self):
		self.state = self.locked
		bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   



