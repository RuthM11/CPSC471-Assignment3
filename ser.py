from socket import *

from connectioninfo import *

import os

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
    print("Length of data: %d" % DATA_LENGTH)

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
            cmd = data.split(" ")
            if cmd[0] == 'ls':
                sdir = os.listdir(os.getcwd())
                response = ""
                for file in sdir:
                    response = response + file + '\n'
                bytesSent = 0
                dirSize = convert_data_str(len(response),10)
                connectionSocket.send(bytes(dirSize,'utf-8'))
                while bytesSent < len(response): 
                    bytesSent += connectionSocket.send(bytes(response[bytesSent:], 'utf-8'))
            elif cmd[0] == 'put':
                #Check to see if existing file
                if not os.path.isfile(cmd[1]):
                    #Tell its okay to send                    
                    plsSend = convert_data_str("YES",3)
                    connectionSocket.send(bytes(plsSend,'utf-8'))
                    #open file with name stored in cmd[1]
                    user_file = open(cmd[1],"wb+")
                    #receive file
                    fileBytesSent = 0
                    #receieve until we get a number - random nums in buffer?
                    fileSize = connectionSocket.recv(10)
                    fileSize = connectionSocket.recv(10)
                    fileSize = connectionSocket.recv(10)
                    while not fileSize.decode('utf-8').strip('\x00').isdigit():
                        print("No size obtained")
                        fileSize = connectionSocket.recv(10)
                    fSize = int(fileSize.decode('utf-8').strip('\x00'))
                    print("Size of file: ",fSize)
                    while fileBytesSent < fSize:
                        tmp2Buff = connectionSocket.recv(10)
                        if not tmp2Buff:
                            print("Socket closed unexpectedly.")
                            break
                        fileData = tmp2Buff.decode('utf-8').strip('\x00')
                        print("Writing: ",fileData)
                        user_file.write(fileData.encode('ascii'))
                        fileBytesSent += len(fileData)
                        print (fileBytesSent)
                    #tell connection that file was received
                    user_file.close()
                    ack = convert_data_str("Received", 10)
                    connectionSocket.send(bytes(ack, 'utf-8'))
                else:
                    print("File already exists!")
                    #Tell not to send                    
                    skipSend = convert_data_str("NO",3)
                    connectionSocket.send(bytes(skipSend,'utf-8'))
            elif cmd[0] == 'get':
                 #Check to see if file exists
                if os.path.isfile(cmd[1]):
                    #Tell client to get ready
                    yesSend = convert_data_str("YES",3)
                    connectionSocket.send(bytes(yesSend,'utf-8'))
                    #open file to be put
                    get_file = open(cmd[1],"rb")
                    #send file
                    fileSize = int(str(os.stat(cmd[1]).st_size))
                    bytesSent = 0
                    sfileSize = str(fileSize)
                    sizeSend = convert_data_str(sfileSize,100)
                    connectionSocket.send(bytes(sizeSend,'utf-8'))
                    while bytesSent < fileSize:
                        buff = get_file.read(10)
                        connectionSocket.send(buff)
                        bytesSent += 10
                        print("in while loop")
                    get_file.close()
                    print("file closed, waiting for receipt")
                    receipt = connectionSocket.recv(10).decode('utf-8')
                    print ("File" + receipt)
                else:
                    skipSend = convert_data_str("NO",3)
                    connectionSocket.send(bytes(skipSend,'utf-8'))
    except timeout:
        pass

    finally:
        print(data)

        # put data into file
        logfile.write(data)
        logfile.write("\n")
        data = ""
        # tell connection that message was good
        #ack = convert_data_str("OK", 10)
        #connectionSocket.send(bytes(ack, 'utf-8'))

    connectionSocket.close()
    logfile.close()
