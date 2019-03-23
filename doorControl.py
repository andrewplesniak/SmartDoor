##Andrew Plesniak
##3/22/19
##This clas provides the ability to unlock and lock the door for the Smart Door project

import smbus
import time

class door:
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.addr = 0x40
		self.locked = 700 #values were found via experimentation based on what values cuase the door to unlock
		self.unlocked = 1925 

		##Setup and Config
		self.bus.write_byte_data(self.addr, 0, 0x20) #enable the chip
		time.sleep(0.25)
		self.bus.write_byte_data(self.addr, 0, 0x10) #enable Prescale change as noted in the datasheet
		time.sleep(0.25) #delay for reset
		self.bus.write_byte_data(self.addr, 0xfe, 0x11) #changes the Prescale register value for 333Hz, using the equation in the datasheet
		self.bus.write_byte_data(self.addr, 0, 0x20) #enable the chip

		##Initalize
		self.state = self.locked
		self.bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		self.bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   

	def unlock(self):
		self.state = self.unlocked
		self.bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		self.bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   

	def lock(self):
		self.state = self.locked
		self.bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		self.bus.write_word_data(self.addr, 0x08, self.state) #writes to the stop address of Ch0   

	def shutdown(self):
		self.bus.write_byte_data(self.addr, 0x06, 0) #ch0 start time = 0s
		self.bus.write_word_data(self.addr, 0x08, 0) #writes to the stop address of Ch0
		self.bus.write_word_data(self.addr, 0x09, 0x10) #orderly shutdown of channel 0
		self.bus.write_byte_data(self.addr, 0, 0x10) #puts the chip to sleep



