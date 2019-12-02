import serial

arduino = serial.Serial('/dev/ttyACM0',115200)

#def sendToArduino(toSend):
#   arduino.write(encodeToString(toSend).encode('latin_1'))

startMarker = 254
endMarker = 255
specialByte = 253

def sendToArduino(val):
	show("Sending values NOW :")
	arduino.write(encodeToString(val).encode('latin_1'))
	# print(encodeToString(val))
	# show(chr(13))
	
def test_send():
	# show("Sending here")
	arduino.write('Hello'.encode('latin_1'))


def encodeToString(data):
	global startMarker, endMarker, specialByte
	outString = ""
	outString = outString + chr(startMarker)

	for val in data:
		if val >= specialByte:
 			outString = outString + chr(specialByte)
 			outString = outString + chr(val - specialByte)
		else:
			outString = outString + chr(val)

	outString = outString + chr(endMarker)
	return outString 

def show(*args):
    for arg in args:
        print(arg, end="")


