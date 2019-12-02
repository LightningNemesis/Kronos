import subprocess
import select
import time
import threading


###########################################################################
analog = [0,0,0,0]
button = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hatButton = [0, 0]
trigger = [0, 0]
###########################################################################

mode = True

class Joystick:

    def __init__(self,refreshRate = 30):
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE, bufsize=0)
        self.pipe = self.proc.stdout
        #
        self.connectStatus = False  #will be set to True once controller is detected and stays on
        self.reading = '0' * 140    #initialize stick readings to all zeros
        #
        self.refreshTime = 0    #absolute time when next refresh (read results from xboxdrv stdout pipe) is to occur
        self.refreshDelay = 1.0 / refreshRate   #joystick refresh is to be performed 30 times per sec by default
        #
        # Read responses from 'xboxdrv' for upto 2 seconds, looking for controller/receiver to respond
        found = False
        waitTime = time.time() + 3
        while waitTime > time.time() and not found:
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                response = self.pipe.readline()
                # Hard fail if we see this, so force an error
                if response[0:7] == b'No Xbox':
                    raise IOError('No Xbox controller/receiver found')
                # Success if we see the following
                if response[0:12].lower() == b'press ctrl-c':
                    found = True
                # If we see 140 char line, we are seeing valid input
                if len(response) == 140:
                    found = True
                    self.connectStatus = True
                    self.reading = response
        # if the controller wasn't found, then halt
        if not found:
            self.close()
            raise IOError('Unable to detect Xbox controller/receiver - Run python as sudo')


    def refresh(self):
        # Refresh the joystick readings based on regular defined freq
        if self.refreshTime < time.time():
            self.refreshTime = time.time() + self.refreshDelay  #set next refresh time
            # If there is text available to read from xboxdrv, then read it.
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                # Read every line that is availabe.  We only need to decode the last one.
                while readable:
                    response = self.pipe.readline()
                    # A zero length response means controller has been unplugged.
                    if len(response) == 0:
                        raise IOError('Xbox controller disconnected from USB')
                    readable, writeable, exception = select.select([self.pipe],[],[],0)
                # Valid controller response will be 140 chars.  
                if len(response) == 140:
                    self.connectStatus = True
                    self.reading = response
                else:  #Any other response means we have lost wireless or controller battery
                    self.connectStatus = False


    def connected(self):
        self.refresh()
        return self.connectStatus

    # Left stick X axis value scaled between -1.0 (left) and 1.0 (right) with deadzone tolerance correction
    def LX(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[3:9])
        return self.axisScale(raw,deadzone)

    # Left stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def LY(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[13:19])
        return self.axisScale(raw,deadzone)

    # Right stick X axis value scaled between -1.0 (left) and 1.0 (right)
    def RX(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[24:30])
        return self.axisScale(raw,deadzone)

    # Right stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def RY(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[34:40])
        return self.axisScale(raw,deadzone)

    # Scale raw (-32768 to +32767) axis with deadzone correcion
    # Deadzone is +/- range of values to consider to be center stick (ie. 0.0)
    def axisScale(self,raw,deadzone):
        if abs(raw) < deadzone:
            return 0.0
        else:
            if raw < 0:
                return (raw + deadzone) / (32768.0 - deadzone)
            else:
                return (raw - deadzone) / (32767.0 - deadzone)

    # Dpad Up status - returns 1 (pressed) or 0 (not pressed)
    def UP(self):
        self.refresh()
        return int(self.reading[45:46])
        
    # Dpad Down status - returns 1 (pressed) or 0 (not pressed)
    def DOWN(self):
        self.refresh()
        return int(self.reading[50:51])
        
    # Dpad Left status - returns 1 (pressed) or 0 (not pressed)
    def LEFT(self):
        self.refresh()
        return int(self.reading[55:56])
        
    # Dpad Right status - returns 1 (pressed) or 0 (not pressed)
    def RIGHT(self):
        self.refresh()
        return int(self.reading[60:61])
        
    # Back button status - returns 1 (pressed) or 0 (not pressed)
    def BACK(self):
        self.refresh()
        return int(self.reading[68:69])

    # Guide button status - returns 1 (pressed) or 0 (not pressed)
    def HOME(self):
        self.refresh()
        return int(self.reading[76:77])

    # Start button status - returns 1 (pressed) or 0 (not pressed)
    def START(self):
        self.refresh()
        return int(self.reading[84:85])

    # Left Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def AXIS_LBUTTON(self):
        self.refresh()
        return int(self.reading[90:91])

    # Right Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def AXIS_RBUTTON(self):
        self.refresh()
        return int(self.reading[95:96])

    # A button status - returns 1 (pressed) or 0 (not pressed)
    def A(self):
        self.refresh()
        return int(self.reading[100:101])
        
    # B button status - returns 1 (pressed) or 0 (not pressed)
    def B(self):
        self.refresh()
        return int(self.reading[104:105])

    # X button status - returns 1 (pressed) or 0 (not pressed)
    def X(self):
        self.refresh()
        return int(self.reading[108:109])

    # Y button status - returns 1 (pressed) or 0 (not pressed)
    def Y(self):
        self.refresh()
        return int(self.reading[112:113])

    # Left Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def L1(self):
        self.refresh()
        return int(self.reading[118:119])

    # Right Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def R1(self):
        self.refresh()
        return int(self.reading[123:124])

    # Left Trigger value scaled between 0.0 to 1.0
    def L2(self):
        self.refresh()
        return int(self.reading[129:132]) / 255.0
        
    # Right trigger value scaled between 0.0 to 1.0
    def R2(self):
        self.refresh()
        return int(self.reading[136:139]) / 255.0

    # Returns tuple containing X and Y axis values for Left stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.leftStick()
    def leftStick(self,deadzone=4000):
        self.refresh()
        return (self.leftX(deadzone),self.leftY(deadzone))

    # Returns tuple containing X and Y axis values for Right stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.rightStick() 
    def rightStick(self,deadzone=4000):
        self.refresh()
        return (self.rightX(deadzone),self.rightY(deadzone))

    # Cleanup by ending the xboxdrv subprocess
    def close(self):
        self.proc.kill()

############################################################################

def show(*args):
    for arg in args:
        print(arg, end="")


def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)



def read_xbox(externalDataset = False, dataSet = []):
    #print("Reading data");
    global analog
    global button
    global hatButton
    global trigger

    joy = Joystick()

    if externalDataset:
        dataSet.extend((analog, button, hatButton, trigger))

    while True:
        
        analog = [joy.LX(),joy.LY(),joy.RX(),joy.RY()]
        button = [joy.UP(), joy.DOWN(), joy.LEFT(), joy.RIGHT(), joy.A(), joy.B(), joy.X(), joy.Y(), joy.L1(), joy.R1(), joy.START(), joy.BACK(), joy.HOME()]
        trigger = [joy.L2(), joy.R2()]
        
        if externalDataset:
            
            dataSet[0] = analog
            dataSet[1] = button
            dataSet[2] = trigger
            

        
def print_all():
    while True:
        print(analog, end = '')
        print(button, end = '')
        print(hatButton, end = '')
        print(trigger, end = '')
        print()


def Main():
    Thread1 = threading.Thread(target = read_xbox)
    #Thread2 = threading.Thread(target = print_all)
    #Thread1.start()
    Thread1.start()
    # reading()



def reading():
    joy = Joystick()

    while not joy.BACK():
        #Showing connection status
        show("Connected:")
        showIf(joy.connected(), "Y", "N")
        
        # Left analog stick
        show("  Left X/Y:", joy.LX(), "/", joy.LY())
        
        # Move cursor back to start of line
        show(chr(13))


# if mode == True:
#     Main()
