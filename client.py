from socket import *
from support import *
import threading
import time


recordtable=[]



def connect(message):
    response=''
    serverName = 'localhost'
    serverPort = 15000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    clientSocket.close()
    return response.decode()


def request():
    counter = 0
    while(True):
        print('ID   Name       Value         Type  TTL  Static')
        for rec in recordtable:
            rec.show()
        counter = counter + 1
        dns  = input('Enter the hostname/domain name for query:')
        flag = input('Enter query type:\n0.A\n1.AAAA\n2.CNAME\n3.NS\n')
        
        key = searchrecord(recordtable,dns,flag)
        if key.value!='???':
            print('Found')
            key.show()
            continue
        message = query()
        message.name = dns
        message.value='???'
        message.flag=flag
        message.qr=0
        message.tx_id=counter
        message = message.encode()
        response = connect(message)
        temp=response
        response = response.split(' ')
        if(response[2]=='Not_Found'):
            print('IP Not Found')
        else:
            insertrec(recordtable,temp)
        
        

if __name__ == "__main__":
    
    t1=threading.Thread(target=delrecord,args=(recordtable,))
    t2=threading.Thread(target=request,args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
