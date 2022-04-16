import BT
import sys
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
        try:
            self.ser.SerialWrite('start\n')
            print("Start send succesfully")
        except:
            print("writing fail!")
            sys.exit(1)

    def get_message(self) -> str:
        #TODO: seperate RFID code and node arrival
        rv = self.ser.SerialReadByte()
        #reach Nd
        if (rv == ""):
            return ""
        elif (rv == 'Nd'):
            #TODO: send next direction
            print("We are at node!")
            return "Node"
        else:
            #send RFID to score
            print("UID received: " + rv)
            return rv

    def send_action(self,dirc):
        # TODO : send the action to car
        self.ser.SerialWrite(dirc)
        return

    def end_process(self):
        self.ser.SerialWrite('stop\n')
        self.ser.disconnect()