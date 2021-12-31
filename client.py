import socket
import threading
import sys
from colorama import init
from termcolor import colored
import os
from dotenv import load_dotenv

init()

dotenv_path = os.path.dirname(__file__) + '\\.env'
load_dotenv(dotenv_path)

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

#Get host and port
try:
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT"))
except:
    host = input("Host: ")
    port = int(input("Port: "))

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
while True:
    message = input('[*]: ')
    sock.sendall(str.encode(message))

    if message == 'exit':
        os._exit(0)
