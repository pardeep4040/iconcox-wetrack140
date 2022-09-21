import socket
import threading
from threading import *
from datetime import datetime
import time 
from time import ctime
ct=ctime()

DATA_LENGTH = 10*1024
PORT = 6071
SERVER = "172.105.51.53"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION]{addr} connected.")    
    connected =True
    while connected:
        data=conn.recv(DATA_LENGTH)
        if not data: break
        
        Rdata=data[:].decode(FORMAT) 
                #print(Rdata)

        f = open("wr.txt", "a")
        f.writelines('\n')
        f.write(ct + Rdata)            
        f.close()   
                
                     
        if (Rdata[2:5] == "LGN"):  # login packet
            print("[ Request for the Login ]", Rdata)
            st = time.strftime("%d%m%Y%I%M%S")
            login_response = f"$LGN{st}*"
            print("LGN RESPONCE:-",login_response)
            login_response_byte = login_response.encode(FORMAT)
            conn.send(login_response_byte)


        elif (Rdata[2:5] == "HBT"):  # Heartbeat packet
            print("[ Request for the Heartbeat ]", Rdata)
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
           
    conn.close()
def start():
    server.listen()
    print(f"[server listening on]{SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        thread.start()
        print(f"[active connections]{threading.activeCount() - 1}")
        while True:

            print("I have Been waiting for clients. . .")
            conn, addr = server.accept()
            print("Got connection from:", addr)
            thread = threading.Thread(target=handle_client, args = (conn, addr))
            thread.start()


print("[starting] server is starting...")
start()
