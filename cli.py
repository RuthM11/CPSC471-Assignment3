from socket import *
import os, sys

#remove and uncomment to use at end
from connectioninfo import *

serverName = SERVER_NAME
serverPort = PORT_NUMBER
size = 1024
inputData = ""
PARTITION_SIZE = 40
#if 3 != len(sys.argv):
   # print "Wrong number of arguments."
   # return -1
#serverName = sys.argv[1]
#serverPort = sys.argv[2]

def convert_data_str(data, size):
    # converts 'data' into a string of length 'size' and returns a new string
    formattedData = str(data)
    while len(formattedData) <= size:
        formattedData = formattedData + '\0'

    return formattedData


#Control Connection Function
def client_connect_tcp(server, port):
    # connects to a socket using 'server' and 'port'
    # receives amount of bytes to send at a time

    try:
        global PARTITION_SIZE
        connSocket = socket(AF_INET, SOCK_STREAM)
        connSocket.connect((server, port))

        # set the size of data delivery
        bytesToSend = connSocket.recv(10)
        #print("Server: %d byte sections" % int(bytesToSend.decode('utf-8')))
        PARTITION_SIZE = int(bytesToSend.decode('utf-8').strip('\x00'))

    except ConnectionRefusedError as e:
        # happens when client cannot connect to server
        print("Client can't connect. Ensure server is running.\nMessage: %s" % e)

    finally:
        return connSocket


#Function for sending data -- will be replaced to send file as packet
def send_data(data, dataSock):
    # interactions:
        # sends a 10-byte string to tell size of data
        # sends data
        # accepts a receipt
        

    # tell server how much is being sent
    dataLength = str(len(data))
    message = convert_data_str(dataLength, 10)
    dataSock.send(bytes(message, 'utf-8'))

    bytesSent = 0
    sectionNumber = 1
    # start sending data
    while bytesSent <= len(data):
        try:
            sectionBytes = 0
            # input("say something: ")

            # send data part by part
            sectionBytes += dataSock.send(bytes(data[bytesSent:(PARTITION_SIZE * sectionNumber)], 'utf-8'))
            sectionNumber += 1

            # fill in section if it's too small because the server
            # is waiting for all the data (can also do a timeout)
            while sectionBytes < PARTITION_SIZE:
                sectionBytes += dataSock.send(bytes(str('\0'), 'utf-8'))

            # keep track of total bytes sent
            bytesSent += sectionBytes

            # progress report
            print("Total bytes sent so far: %d" % bytesSent)

        except ConnectionRefusedError as e:
            # happens when server is down and client tries to send
            print("Error with connection: %s" % e)
            break

        except ConnectionAbortedError as e:
            # happens when server cuts connection and client tries to send
            print("Error with connection: %s" % e)
            break

        finally:
            # break if we're done
            if bytesSent >= len(data):
                break
#Main

#FTP handler
rinput = input("ftp>")
user_cmd = rinput.split(" ")
while user_cmd[0] != "exit":
    if user_cmd[0] == "get":
        #stuff for get
        #Check to see if existing file
        if not os.path.isfile(user_cmd[1]):
            #open socket
            dataSocket = client_connect_tcp(serverName, serverPort)
            #send Command
            send_data(rinput,dataSocket)
            #Check to see if we have a file to be receieved
            receipt = dataSocket.recv(3)
            proceed = receipt.decode('utf-8').strip('\x00')
            print("Proceed? ",proceed)
            if proceed != "NO":
                #open file with name stored in cmd[1]
                user_file = open(user_cmd[1],"wb")
                #receive file
                fileBytesSent = 0
            #We have to receieve twice for some reason unknown
                fileSize = dataSocket.recv(10)
                #fileSize = dataSocket.recv(10)
                fSize = int(fileSize.decode('utf-8').strip('\x00'))
                print("Size of file: ",fSize)
                while fileBytesSent < fSize:
                        tmp2Buff = dataSocket.recv(10)
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
                dataSocket.send(bytes(ack, 'utf-8'))
                dataSocket.close()
            else:
                print("File does not exist on server!")
        else:
            print("File already exists in your directory!")                  
    elif user_cmd[0] == "put" and os.path.isfile(user_cmd[1]):
        #open socket
        dataSocket = client_connect_tcp(serverName, serverPort)
        #send string "put filename"
        send_data(rinput,dataSocket)
        #receive ok to send
        receipt = dataSocket.recv(3)
        proceed = receipt.decode('utf-8').strip('\x00')
        #Check to see if file exists
        if proceed == "NO":
            print("File cannot be received!")
        else:
            #open file to be put
            put_file = open(user_cmd[1],"rb")
            #send file
            fileSize = int(str(os.stat(user_cmd[1]).st_size))
            bytesSent = 0
            sfileSize = str(fileSize)
            sizeSend = convert_data_str(sfileSize,100)
            send_data(sizeSend,dataSocket)
            while bytesSent < fileSize:
                buff = put_file.read(10)
                sendData = convert_data_str(buff,10)
                send_data(sendData,dataSocket)
                #dataSocket.send(bytes(sendData,'utf-8'))
                #dataSocket.send(buff)
                bytesSent += 10
            put_file.close()
            print("file closed, waiting for receipt")
            receipt = dataSocket.recv(10).decode('utf-8')
            print ("File" + receipt)
        dataSocket.close()
    elif user_cmd[0] == "ls":
        #list whats in server
        dataSocket = client_connect_tcp(serverName, serverPort)
        #send command
        send_data(user_cmd[0],dataSocket)
        #receive size
        dirSize = dataSocket.recv(10)
        dSize = int(dirSize.decode('utf-8').strip('\x00'))
        receipt = dataSocket.recv(dSize).decode('utf-8')
        print (receipt)
        dataSocket.close()
    elif user_cmd[0] == "lls":
        #list whats in client
        cdir = os.listdir()
        for file in cdir:
            print(file)
    else:
        print("Invalid command or file does not exist!")
    rinput = input("ftp>")
    user_cmd = rinput.split(" ")
#controlSocket.close()
print("Done")

