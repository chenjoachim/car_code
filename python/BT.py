from time import sleep
import serial
# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?

class bluetooth:
    def __init__(self):
        self.ser = serial.Serial()

    def do_connect(self,port):
        self.ser.close()
        print("Connecting...")
        try:
            self.ser = serial.Serial(port,9600,timeout=2)
            print("connect success")
            print("")
        except serial.serialutil.SerialException:
            print("fail to connect")
            print("")
            return False
        return True


    def disconnect(self):
        self.ser.close()

    def SerialWrite(self,output):
        # send = 's'.encode("utf-8")
        send = output.encode("utf-8")
        self.ser.write(send)

    '''
    This part may not be needed
    def SerialReadString(self):
        # TODO: Get the information from Bluetooth. Notice that the return type should be transformed into hex.
        
        waiting = self.ser.in_waiting
        if waiting >= 0:
            rv = self.ser.read(1).decode("utf-8") 
            return rv
        return ""
    '''
    #receive str message from the car
    def SerialReadByte(self):
        # sleep(0.05)
        if(self.ser.in_waiting > 0):
        # if(True):
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]
            # receiveMsg = input("Test message: ")
            self.ser.flushInput()
            return receiveMsg
        else:
            return ""


