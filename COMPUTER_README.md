## Computer connection code

> First update: 20220415

The code should be able to ask the car to go shape C, changing direction automatically

Some important notice:

1. send `"Nd\n"` for reaching a node
2. send the RFID in HEX
3. the computer will send following codes: `"start", "stop", "R", "L"`

update on OPENLAB 20220416:
- 09:56 AM RFID individual test success

update on 20220419
To compile the code, use following command in your terminal:
1. (using local point system) python main.py 1 1
2. (using remote point system) python main.py 1 2