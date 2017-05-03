from socket import *

from connectioninfo import *

# connectioninfo.py contains connection information for easier editing
serverPort = PORT_NUMBER

# TCP Socket and bind
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))

# Listen on the port
serverSocket.listen(1)

print("Server ready to listen.\n")

#data buffer
data = ""
tmpBuff = bytes()
BYTES_TO_ACCEPT = 40

while 1:
    # Accept a connection request: get the client's socket
    connectionSocket, addr = serverSocket.accept()
    print("%s says: " % str(addr[0]), end="")
    #connectionSocket.settimeout(3)

    try:
        # Receive whatever the newly conneted client has sent
        while len(bytes(data, 'utf-8')) != BYTES_TO_ACCEPT:
            tmpBuff = connectionSocket.recv(BYTES_TO_ACCEPT)
            if not tmpBuff:
                print("Socket closed unexpectedly.")
                break
            data += tmpBuff.decode('utf-8')
    except timeout:
        pass

    finally:
        print(data)
        data = ""
        #tmpBuff = bytes("", 'utf-8')

    connectionSocket.close()
