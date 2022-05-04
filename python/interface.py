import BT
import sys
import maze
import score
import time

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface():
    def __init__(self, route):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        if (port == ""):
            port = "COM4"
            #TODO: change port name if needed
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        print("Please test RFID")
        while (True):
            rv = self.get_message()
            if (rv != ""):
                print("result:", rv)
                k = 'J'
                while (k != 'Y' and k != 'N'):
                    k = str(input("Is RFID correct? (Y/N)"))
                if (k == 'Y' or k == 'y'):   break
                if (k == 'N' or k == 'n'):
                    print("WTF?")
                    sys.exit(1)
        input("Press put the car on route and press enter to start.")
        try:
            self.ser.SerialWrite(route)
            time.sleep(5)
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
        self.ser.SerialWrite('stop')
        self.ser.disconnect()