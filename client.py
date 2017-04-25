from socket import *

from connectioninfo import *

# name and port number of the server we are connecting to
# connectioninfo.py contains the information to easily edit it in the future
serverName = SERVER_NAME
serverPort = PORT_NUMBER

# create a socket, connect
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# string to send
data2 = ""


while str(data2).lower() != "exit":
    try:
        data2 = input("send a string (type exit to exit): ")
        if str(data2).lower() == "exit":
            break
        elif str(data2).isprintable():
            clientSocket.send(bytes(data2, 'utf-8'))
    except ConnectionAbortedError:
        print("Connection aborted, closing.\n")
    finally:
        print("Message sent.\n")
# close the socket
clientSocket.close()
print("Connection closed.\n")
