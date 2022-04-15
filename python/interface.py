import BT
import maze
import score

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        input("Press enter to start.")
        self.ser.SerialWrite('start\n')

    def get_message(self):
        #TODO: seperate RFID code and node arrival
        rv = self.ser.SerialReadByte()
        #reach Nd
        if (rv == 'Nd\n'):
            #TODO: send next direction
            pass
        else:
            #send RFID to score
            pass

    def send_action(self,dirc):
        # TODO : send the action to car
        self.ser.SerialWrite(dirc)
        return

    def end_process(self):
        self.ser.SerialWrite('stop\n')
        self.ser.disconnect()