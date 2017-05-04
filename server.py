from socket import *

from connectioninfo import *


def convert_data_str(data, size):
    # converts 'data' into a string of length 'size' and returns a new string
    formattedData = str(data)
    while len(formattedData) < size:
        formattedData = formattedData + '\0'

    return formattedData


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

    # tell connection how many bytes to send at a time
    acceptSizeString = convert_data_str(BYTES_TO_ACCEPT, 10)
    connectionSocket.send(bytes(acceptSizeString, 'utf-8'))

    # receive length of data to be received
    recvDataLength = connectionSocket.recv(10)
    DATA_LENGTH = int(recvDataLength.decode('utf-8').strip('\x00'))
    #print("Length of data: %d" % DATA_LENGTH)

    try:
        # record session in a log file
        logfile = open("data.txt", "a+")

        # Receive whatever the newly connected client has sent
        while len(bytes(data, 'utf-8')) != DATA_LENGTH:
            tmpBuff = connectionSocket.recv(BYTES_TO_ACCEPT)
            if not tmpBuff:
                print("Socket closed unexpectedly.")
                break
            data += tmpBuff.decode('utf-8').strip('\x00')
    except timeout:
        pass

    finally:
        print(data)

        # put data into file
        logfile.write(data)
        logfile.write("\n")
        data = ""

        # tell connection that message was good
        ack = convert_data_str("OK", 10)
        connectionSocket.send(bytes(ack, 'utf-8'))

    connectionSocket.close()
    logfile.close()