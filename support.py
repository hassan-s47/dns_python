import time

class query:
    name=''
    value=''
    flag=''
    qr=0
    tx_id=0
    name_len=0
    val_len=0

    def __init__(self):
        pass

    def encode(self):
        result = str(self.tx_id)
        result = result + ' ' + self.name
        result = result + ' ' + self.value
        result = result + ' ' + str(self.flag)
        result = result + ' ' + str(self.qr)
        return result

class record:
    id=0
    name=''
    value=''
    ttl=0
    static=0
    flag=0
    def __init__(self):
        pass
    def show(self):
        print(self.id,' ',self.name,' ',self.value,' ',self.flag,' ',self.ttl,' ',self.static)
    def encode(self):
        result = str(self.id)
        result = result+' '+ self.name
        result = result + ' ' + self.value
        result = result + ' ' + str(self.flag)
        result = result + ' ' + '1' #for QR flag 1 for response
        result = result + ' ' + '60' #for TTL = 60
        result = result + ' ' + '0' #for static = 0
        return result

def loadrecordtable(filestr):
    file = open(filestr)
    lines = file.readlines()
    records = []
    for line in lines:
        data = line.split(' ')
        r1 = record()
        r1.id = int(data[0])
        r1.name = data[1]
        r1.value = data[2]
        r1.flag = int(data[3])
        r1.static = 1
        r1.ttl = 60
        records.append(r1)
    return records

def delrecord(records):
    while(True):
        time.sleep(1)
        for rec in records:
            if rec.ttl ==1:
                print('\nRecord Expired by TTL\n')
                records.remove(rec)
                continue
            if rec.static != 1:
                rec.ttl = rec.ttl -1 

def searchrecord(records,name,flag):
    for rec in records:
        if rec.name == name and rec.flag == flag:
            return rec
    r1 = record()
    r1.value='???'
    return r1

def insertrec(records,message):
    
    r1 = record()
    message = message.split(' ')
    ans = searchrecord(records,message[1],int(message[3]))
    if(ans.value!='???'):
        return
    r1.ttl = 60
    r1.static =0
    if(len(records)!=0):
        r1.id = records[-1].id+1
    else:
        r1.id = 1
    r1.name = message[1]
    r1.value = message[2]
    r1.flag = int(message[3])
    records.append(r1)
    