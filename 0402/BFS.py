import BT0402 as BT
import threading
import time
import sys
import serial

bt = BT.bluetooth("COM9")
while not bt.is_open(): pass
print("BT Connected!")

readThread = threading.Thread(target=BT.read)
readThread.daemon = True
readThread.start()

while True:
    msgWrite = input()
    if msgWrite == "go": break

bt.write('start')
