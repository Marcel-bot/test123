from serial import Serial
from serial.tools.list_ports import comports
from time import sleep

print(comports())

ser = Serial('/dev/ttyUSB0', 9600)


def msg_hand(msg: str) -> None:
    ser.write(msg.encode())


def msg_head():
    pass


sleep(2)
msg_hand('1')
sleep(2)


msg_hand('1')
sleep(2)


msg_hand('1')
sleep(2)


msg_hand('1')
sleep(2)


msg_hand('1')
sleep(2)
