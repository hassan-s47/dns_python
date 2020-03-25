from socket import *
from support import *
import threading
import time


recordtable= loadrecordtable('local.txt')
delay = 1

def process(message):
    response = ' '
    
    message = message.split(' ')
    print(message[1],' ',message[3])
    result = searchrecord(recordtable,message[1],int(message[3]))
    if result.value!='???':
        response = result.encode() 
    else:
        for rec in recordtable:
            if(rec.flag==3):
                if(message[1].find(rec.name)>0):  #Could be generic code but we are testing it on localhost therefore we simply hard code it :)
                    temp = message
                    message = ' '
                    message =message.join(temp)
                    if(rec.name == 'qualcomm.com'):
                        serverPort = 21000
                    elif rec.name == 'viasat.com':
                        serverPort = 22000
                    serverName = 'localhost'
                    clientSocket = socket(AF_INET, SOCK_DGRAM)
                    clientSocket.sendto(message.encode(),(serverName, serverPort))
                    response, serverAddress = clientSocket.recvfrom(2048)
                    clientSocket.close()
                    insertrec(recordtable,response.decode())
                    return response.decode()

       
        message[2] = 'Not_Found'
        response = response.join(message)
            
        
        
    return response



def serve():
    serverPort = 15000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print ('The server is ready to receive')
    while 1:
        print('ID   Name       Value         Type  TTL  Static')
        for rec in recordtable:
            rec.show()
        message, clientAddress = serverSocket.recvfrom(2048)
        response = process(message.decode())
        serverSocket.sendto(response.encode(), clientAddress)



if __name__ == "__main__":
   

    t1 = threading.Thread(target=serve,args=())
    t2 = threading.Thread(target=delrecord,args=(recordtable,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()