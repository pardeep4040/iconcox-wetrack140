import socket
import threading
from threading import *
import time 
from time import ctime
from datetime import datetime
from pytz import timezone

ct=ctime()

DATA_LENGTH = 10*1024
PORT = 41700
SERVER = "127.0.0.1"
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
                
        if (Rdata[0:3] == "LGN"):  # login packet
            print("[ Request for the Login ]", Rdata)
            format = "%d%m%Y%I%M%S"
            now_utc = datetime.now(timezone('UTC'))            
            st=now_utc.strftime("%d%m%Y%I%M%S")       
            login_response = f"$LGN{st}*"
            print("LGN RESPONCE:-",login_response)
            login_response_byte = login_response.encode(FORMAT)
            conn.send(login_response_byte)


        elif (Rdata[0:3] == "HBT"):  # Heartbeat packet
            print("[ Request for the HBT ]", Rdata)
            heartbeat_response = "$HBT,OK*"
            heartbeat_response_byte = heartbeat_response.encode(FORMAT)
            print("HBT RESPONCE:-",heartbeat_response)
            conn.send(heartbeat_response_byte)

        elif (Rdata[0:3] == "BTH"):  # BTH packet
            print("[ Request for the BTH ]", Rdata)
            BTH_response = "$BTH,OK*"
            BTH_response_byte = BTH_response.encode(FORMAT)
            print("BTH RESPONCE:-",BTH_response)
            conn.send(BTH_response_byte)

        elif (Rdata[0:3] == "ACK"):  # ACK packet
            print("[ Request for the ACK ]", Rdata)
            ACK_response = "$ACK,OK*"
            ACK_response_byte = ACK_response.encode(FORMAT)
            print("ACK RESPONCE:-",ACK_response)
            conn.send(ACK_response_byte)

        elif (Rdata[0:3] == "FUL"):  # FUL packet
            print("[ Request for the FUL ]", Rdata)
            FUL_response = "$FUL,OK*"
            FUL_response_byte = FUL_response.encode(FORMAT)
            print("FUL RESPONCE:-",FUL_response)
            conn.send(FUL_response_byte)

        elif (Rdata[0:3] == "HLM"):  # HLM packet
            print("[ Request for the HLM ]", Rdata)
            HLM_response = "$HLM,OK*"
            HLM_response_byte = HLM_response.encode(FORMAT)
            print("HLM RESPONCE:-",HLM_response)
            conn.send(HLM_response_byte)

        elif (Rdata[0:3] == "ALT"):  # ALT packet
            print("[ Request for the ALT ]", Rdata)
            ALT_response = "$ALT,OK*"
            ALT_response_byte = ALT_response.encode(FORMAT)
            print("ALT RESPONCE:-",ALT_response)
            conn.send(ALT_response_byte)

        elif (Rdata[0:3] == "CRT"):  # CRT packet
            print("[ Request for the CRT ]", Rdata)
            CRT_response = "$CRT,OK*"
            CRT_response_byte = CRT_response.encode(FORMAT)
            print("CRT RESPONCE:-",CRT_response)
            conn.send(CRT_response_byte)

        elif (Rdata[0:3] == "EPB"):  # EPB packet
            print("[ Request for the EPB ]", Rdata)
            EPB_response = "$EPB,OK*"
            EPB_response_byte = EPB_response.encode(FORMAT)
            print("EPB RESPONCE:-",EPB_response)
            conn.send(EPB_response_byte)

        elif (Rdata[0:3] == "NRM"):  # NRM packet
            print("[ Request for the NRM ]", Rdata)
            NRM_response = "$NRM,OK*"
            NRM_response_byte = NRM_response.encode(FORMAT)
            print("NRM RESPONCE:-",NRM_response)
            conn.send(NRM_response_byte)
                    
           
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
