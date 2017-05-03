from socket import *

from connectioninfo import *

# name and port number of the server we are connecting to
# connectioninfo.py contains the information to easily edit it in the future
serverName = SERVER_NAME
serverPort = PORT_NUMBER
inputData = ""
PARTITION_SIZE = 40


# connects to a socket using server an port as arguments
def client_connect_tcp(server, port):
    try:
        connSocket = socket(AF_INET, SOCK_STREAM)
        connSocket.connect((server, port))

    except ConnectionRefusedError as e:
        # happens when client cannot connect to server
        print("Client can't connect. Ensure server is running.\nMessage: %s" % e)

    finally:
        return connSocket

def send_data(data, dataSock):
    bytesSent = 0
    sectionNumber = 1


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


while str(inputData).lower() != "exit":

    inputData = input("Send a string (type exit to exit): ")
    if str(inputData).lower() == "exit":
        break

    # connect and send
    dataSocket = client_connect_tcp(serverName, serverPort)
    send_data(inputData, dataSocket)
    print("Message sent")

    # close the socket when the message is done being sent
    # print("Closing connection")
    dataSocket.close()
    # print("Connection closed.\n")


