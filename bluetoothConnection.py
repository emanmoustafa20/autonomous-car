# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $


import bluetooth


CAR_MAC_ADDRESS = '98:D3:A1:FD:4B:1E'

port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((CAR_MAC_ADDRESS, port))
while 1:
    text = input() # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    s.send(text)
s.close()

