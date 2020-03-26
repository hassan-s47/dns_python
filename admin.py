from socket import *
from support import *
import threading
import time




if __name__ == "__main__":
    response=''
    print()
    serverName = 'localhost'
    message = 'admin'
    print('ID\tName\tValue\t\t\t\t\tType\tTTL\tStatic')
       
    serverPort = 15000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    while(True):
        response, serverAddress = clientSocket.recvfrom(2048)
        count = int(response.decode())
        for i in range(count):
            response, serverAddress = clientSocket.recvfrom(2048)
            response = response.decode()
            response = response.split(' ')
            print(response[0],'\t',response[1],'\t',response[2],'\t\t\t',response[3],'\t',response[5],'\t',response[6])
        break
    clientSocket.close()
    