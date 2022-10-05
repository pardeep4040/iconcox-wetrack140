import socket 
from threading import *
import time 
from time import ctime
from datetime import datetime
from pytz import timezone
from socket import AF_INET as AFI ,  SOCK_STREAM as SKTRM
datalength=20*1024
FORMAT = "utf-8"


class GpsThread(Thread):
    def __init__(self,conn):
        Thread.__init__(self)
        self.conn=conn
    def run(self):
        name=current_thread().getName()
        while True:
            if name=='sender':
                data = conn.recv(datalength)
                if not data: break
                Rdata=data[:].decode(FORMAT)          
                if (Rdata[2:5] == "LGN"):  # login packet
                    global IMEI
                    IMEI = Rdata[21:36]
                    
                    print("[ Request for the Login ]", Rdata)
                    format = "%d%m%Y%I%M%S"
                    now_utc = datetime.now(timezone('UTC'))            
                    st=now_utc.strftime("%d%m%Y%I%M%S") 
                    login_response = f"$LGN{st}*"
                    print("LGN RESPONCE:-",login_response)
                    login_response_byte = login_response.encode(FORMAT)
                    conn.send(login_response_byte)


                elif (Rdata[2:5] == "HBT"):  # Heartbeat packet
                    print("[ Request for the Heartbeat ]"), Rdata
                    heartbeat_response = "$HBT*"
                    heartbeat_response_byte = heartbeat_response.encode(FORMAT)
                    print("HBT RESPONCE:-",heartbeat_response)
                    conn.send(heartbeat_response_byte)


                elif (Rdata[2:5] == "NRM"):  # NRM packet
                    print("[ Request for the NRM ]",Rdata)
                    imei = Rdata[26:41]
                    gps_response = f"$,NRM,{imei},1*"
                    print("NRM RESPONCE:-",gps_response)
                    gps_response_byte = gps_response.encode(FORMAT)
                    conn.send(gps_response_byte)

                elif(Rdata[1:7] == "Header"):
                    print("Responce from client:", Rdata)

                else:
                    print("[ bad request ]", Rdata)
                    bad_response = "Bad request*"
                    bad_response_byte = bad_response.encode(FORMAT)
                    print("BAD RESPONCE:-",bad_response)
                    conn.send(bad_response_byte)
                    
            elif name=='receiver':
                data = input("ENTER PARAM CMD")
                login_response_byte = data.encode(FORMAT)
                conn.send(login_response_byte)
                R = conn.recv(datalength).decode(FORMAT)
                print(R)


if __name__ == '__main__':
    
    print("=========================================")
    print("=                                       =")
    print("=            Server Responce            =")
    print("=                                       =")
    print("=========================================")
    server=socket.socket(AFI,SKTRM)
    server.bind(('139.162.239.62',20000))
    server.listen(5)
    conn,address=server.accept()
    sender=GpsThread(conn)
    sender.setName('sender')
    receiver=GpsThread(conn)
    receiver.setName('receiver')
    print("connected with",address)
    sender.start()
    receiver.start()
