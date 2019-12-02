from __future__ import print_function
from encodedSerialXbox import sendToArduino, arduino, test_send
import multiprocessing
import serial
import xbox


manager = multiprocessing.Manager()
Process = multiprocessing.Process
dataSet = manager.list()


def map(val, low_in, high_in, low_op, high_op):
    return (((val-low_in)/(high_in - low_in)) * (high_op - low_op)) + low_op


# mode = True

# if mode:
# 	read_xbox()

def sendData():
	while(len(dataSet)==0):
		pass
	print("Starting")
	while(True):

		x = b'j'

		toSend = []

		if x == b'e': #This one's for Left stick
			switcher = 1.0
			for axis in dataSet[0][0:2]:
				val = int(map(axis, -1.0 * switcher, 1.0 * switcher, 0, 65535))
				switcher = switcher * -1.0
				toSend.append(val >> 8 & 0b11111111)
				toSend.append(val & 0b11111111)
			#print(toSend)
			sendToArduino(toSend)

		elif x == b'g': #This one's for Right stick
			switcher = 1.0
			for axis in dataSet[0][2:]:
				val = int(map(axis, -1.0 * switcher, 1.0 * switcher, 0, 65535))
				switcher = switcher * -1.0
				toSend.append(val >> 8 & 0b11111111)
				toSend.append(val & 0b11111111)
			#print(toSend)
			sendToArduino(toSend)   

		elif x == b'j': #This one's for Triggers
			for trig in dataSet[2]:
				val = int(map(trig, 0, 1.0, 0, 65535))           
				toSend.append(val >> 8 & 0b11111111)
				toSend.append(val & 0b11111111)
				#print(val, val >> 8 & 0b11111111, val & 0b11111111, end = ' | ')
			#print()
			# print(toSend, end ='')
			# print(dataSet[2])
			sendToArduino(toSend)
			#print(dataSet[2])
			#test_send()

		elif x == b'i': #This one's for Buttons
			val = 0
			for butt in dataSet[1][0:8]:
				val = val << 1 | butt # UP | Down | Left | Right | A | B | X | Y  
			toSend.append(val)
			val = 0
			for butt in dataSet[1][8:]:
				val = val << 1 | butt # L1 | R1 | START | HOME | BACK 
			toSend.append(val)
			# print(toSend)
			sendToArduino(toSend)

def Main():
	print("Started sending data")
	process1 = Process(target = xbox.read_xbox, args = (True, dataSet))
	process2 = Process(target = sendData, args = ())
	
	process1.start()
	process2.start()
	process1.join()
	process2.join()
	


if __name__ == "__main__":
	Main()


