# Raspberry Pi Home Automation System
# By Anarghya Mitra (amitra.me)
# Date - 12/29/2012
#
# Wiring for LCD
# 1 : Ground
# 2 : Vcc (5V)
# 3 : Contrast (0-5V) 
# 4 : RS (Register Select) 
# 5 : R/W (Read Write) - needs to be grounded
# 6 : Enable or Strobe 
# 7 : Data Bit 0 - don't use
# 8 : Data Bit 1 - don't use
# 9 : Data Bit 2 - don't use
# 10: Data Bit 3 - don't use 
# 11: Data Bit 4 
# 12: Data Bit 5 
# 13: Data Bit 6 
# 14: Data Bit 7 
# 15: LCD Backlight +5V 
# 16: LCD Backlight Ground (Blue)

import socket
import sys
import os
import time
import threading
import RPi.GPIO as GPIO

#constants for server
SETUP = 0
OUTPUT = 1
CLOSE = 2
RADIO_NEXT = 3
RADIO_PREV = 4
RADIO_PLAY = 5
RADIO_STOP = 6
RADIO_PAUSE = 9
VOLUME_PLUS = 7
VOLUME_MINUS = 8

VOLUME = 100

#constants for LCD
LCD_RS = 25
LCD_E = 24
LCD_DATA4 = 23
LCD_DATA5 = 17
LCD_DATA6 = 21
LCD_DATA7 = 22

LEFT = 1
CENTER = 2
RIGHT = 3

#only GPIO pins left are 18 and 4, used for lights

LCD_WIDTH = 20
LCD_CHR = True
LCD_CMD = False

LCD_LINE1 = 0x80
LCD_LINE2 = 0xC0
LCD_LINE3 = 0x94
LCD_LINE4 = 0xD4

E_PULSE = 0.00005
E_DELAY = 0.00005

#utility functions
def getNetworkIP():
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('google.com',0))
	return s.getsockname()[0]
	
def GPIO_setup(data):
	pinnumber = int(data[1:3])
	statenumber = int(data[3])
	GPIO.setup(pinnumber,statenumber)
	print "Setup ",pinnumber," ",statenumber
	return 0
	
def GPIO_output(data):
	pinnumber = int(data[1:3])
	statenumber = int(data[3])
	GPIO.output(pinnumber,statenumber)
	print "Output",pinnumber," ",statenumber
	return 0


class GPIO_radio(threading.Thread):
	def __init__(self):
		super(GPIO_radio,self).__init__()
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(LCD_E, GPIO.OUT)  # enable
		GPIO.setup(LCD_RS, GPIO.OUT) # register select
		GPIO.setup(LCD_DATA4, GPIO.OUT) # databit4
		GPIO.setup(LCD_DATA5, GPIO.OUT) # databit5
		GPIO.setup(LCD_DATA6, GPIO.OUT) # databit6
		GPIO.setup(LCD_DATA7, GPIO.OUT) # databit7

	def LCD_init(self):
		#init display
		self.LCD_byte(0x33,LCD_CMD)
		self.LCD_byte(0x32,LCD_CMD)
		self.LCD_byte(0x28,LCD_CMD)
		self.LCD_byte(0x0C,LCD_CMD)
		self.LCD_byte(0x06,LCD_CMD) 
		self.LCD_byte(0x01,LCD_CMD)

	def LCD_string(self,message, style):
		#write string to screen
		# 1 = left
		# 2 = center
		# 3 = right
		if style>=1 and style<=3:
			if style==1:
				message = message.ljust(LCD_WIDTH," ")
			elif style==2:
				message = message.center(LCD_WIDTH," ")
			elif style==3:
				message = message.rjust(LCD_WIDTH," ")
			for i in range(LCD_WIDTH):
				self.LCD_byte(ord(message[i]),LCD_CHR)

	def LCD_update(self,string1,string2,string3,string4, orientation):
		#send text to LCD
		self.LCD_byte(LCD_LINE1,LCD_CMD)
		self.LCD_string(string1,orientation)
		self.LCD_byte(LCD_LINE2,LCD_CMD)
		self.LCD_string(string2,orientation)
		self.LCD_byte(LCD_LINE3,LCD_CMD)
		self.LCD_string(string3,orientation)
		self.LCD_byte(LCD_LINE4,LCD_CMD)
		self.LCD_string(string4,orientation)
		time.sleep(5)

	def LCD_byte(self,bits, mode):
		#send byte to data pins
		#bits is data
		#mode is True for chr, False for cmd

		#initialize high bits
		GPIO.output(LCD_RS,mode)
		GPIO.output(LCD_DATA4,False)
		GPIO.output(LCD_DATA5,False)
		GPIO.output(LCD_DATA6,False)
		GPIO.output(LCD_DATA7,False)

		#write data to high bits
		if bits&0x10==0x10:
			GPIO.output(LCD_DATA4,True)
		if bits&0x20==0x20:
			GPIO.output(LCD_DATA5,True)
		if bits&0x40==0x40:
			GPIO.output(LCD_DATA6,True)
		if bits&0x80==0x80:
			GPIO.output(LCD_DATA7,True)

		#toggle enable
		time.sleep(E_DELAY)
		GPIO.output(LCD_E,True)
		time.sleep(E_PULSE)
		GPIO.output(LCD_E,False)
		time.sleep(E_DELAY)

		# initialize low bits
		GPIO.output(LCD_DATA4,False) 
		GPIO.output(LCD_DATA5,False) 
		GPIO.output(LCD_DATA6,False) 
		GPIO.output(LCD_DATA7,False) 

		#write data to low bits
		if bits&0x01==0x01: 
			GPIO.output(LCD_DATA4,True) 
		if bits&0x02==0x02: 
			GPIO.output(LCD_DATA5,True) 
		if bits&0x04==0x04: 
			GPIO.output(LCD_DATA6,True) 
		if bits&0x08==0x08: 
			GPIO.output(LCD_DATA7,True) 
	  
		# toggle enable
		time.sleep(E_DELAY)     
		GPIO.output(LCD_E,True)   
		time.sleep(E_PULSE) 
		GPIO.output(LCD_E,False)   
		time.sleep(E_DELAY)

	def run(self):
		#main method	
		#init display and display splash screen
		self.LCD_init()
		self.LCD_update("Raspberry Pi","MPD Radio","and Light","Control",CENTER)
		time.sleep(5)
		os.system("mpc play")
		while True:
			f = os.popen("mpc current")
			station = ""
			for i in f.readlines():
				station+=i
			self.LCD_update(station,"","","",LEFT)
	
class GPIO_server:
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self.PORT = 23476
		self.serversocket = None
		self.threadlist = []

	def open_socket(self):
		self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		netip = getNetworkIP()
		print "IP address: ",netip
		self.serversocket.bind((netip,self.PORT))
		self.serversocket.listen(4)

	
	def run(self):
		self.open_socket()
		try:
			while True:
				print 'Waiting for connection...'
				clientsocket, address = self.serversocket.accept()
				print 'Connection established. IP: ',address
				clientthread = GPIO_client(clientsocket)
				clientthread.start()
				self.threadlist.append(clientthread)
		except Exception:
			if self.serversocket:
				self.serversocket.close()
				for c in self.threadlist:
					c.join()
			
class GPIO_client(threading.Thread):
	def __init__(self,clientsocket):
		super(GPIO_client,self).__init__()
		self.BUFFERSIZE = 1024
		self.cs = clientsocket
	def run(self):
		data = None
		try:
			while True:
				data = self.cs.recv(self.BUFFERSIZE)
				data = data[2:]
				print data[0]
				print data[1]
				print data[2]
				if len(data)<3:
					continue
				if int(data[0])==SETUP:
					GPIO_setup(data)
				elif int(data[0])==OUTPUT:
					GPIO_output(data)
				elif int(data[0])==CLOSE:
					self.cs.close()
				elif int(data[0])==RADIO_NEXT:
					os.system("mpc next")
					time.sleep(.1)
					os.system("mpc play")		
				elif int(data[0])==RADIO_PREV:
					os.system("mpc prev")
					time.sleep(.1)
					os.system("mpc play")
				elif int(data[0])==RADIO_PLAY:
					os.system("mpc play")
				elif int(data[0])==RADIO_STOP:
					os.system("mpc stop")
				elif int(data[0])==RADIO_PAUSE:
					os.system("mpc pause")
				elif int(data[0])==VOLUME_PLUS:
					if VOLUME<100:
						VOLUME+=1
						os.system('amixer set Master {vol}%'.format(vol=VOLUME))
				elif int(data[0])==VOLUME_MINUS:
					if VOLUME>0:
						VOLUME-=1
						os.system('amixer set Master {vol}%'.format(vol=VOLUME))
		except Exception:
			if self.cs:
				self.cs.close()
				
if __name__=='__main__':
	os.system('amixer set Master {vol}%'.format(vol=VOLUME))
	radiothread = GPIO_radio()
	radiothread.start()
	gpioserv = GPIO_server()
	gpioserv.run()
