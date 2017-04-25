from socket import *

# name and port number of the server we are connecting to
serverName = "localhost"
serverPort = 12000
clientPort = 12001

# create a socket, connect
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# string to send
#data = "Hello world! This is a very long string."


# send the string
#clientSocket.send(bytes(data, 'utf-8'))
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
