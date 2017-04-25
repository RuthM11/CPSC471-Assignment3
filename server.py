from socket import *

serverPort = 12000

# TCP Socket and bind
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))

# Listen on the port
serverSocket.listen(1)

print("Server ready to listen.\n")

#data buffer
data = ""

while 1:
    # Accept a connection request: get the client's socket
    connectionSocket, addr = serverSocket.accept()

    # Receive whatever the newly conneted client has sent
    data = connectionSocket.recv(40)

    print(data.decode('utf-8'))

    # Close the socket after receipt
    connectionSocket.close()

