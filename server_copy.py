#------------------------------------------------------------------------------------------
# Server.py
#------------------------------------------------------------------------------------------
from threading import Thread    # for handling task in separate jobs we need threading
import socket           # tcp protocol
import datetime         # for composing date/time stamp
import sys              # handle system error
import traceback        # for print_exc function
import time             # for delay purpose
global host, port
import cryptography
from cryptography.fernet import Fernet

cmd_GET_MENU = "GET_MENU"
cmd_END_DAY = "CLOSING"
# default_menu = "C:/Users/Shafeeq Amirudeen/Documents/Poly 1.2/ACG/Assignment 2 Baseline v5.0 (1)/Assignment 3 Baseline v5.0/Assignment3v5/server/menu_today.txt"
default_menu = "menu_today.txt"
default_save_base = "result-"

host = socket.gethostname() # get the hostname or ip address
port = 8888                # The port used by the server


key = Fernet.generate_key()
with open('mykey.key', 'wb') as mykey:
    mykey.write(key)
with open('mykey.key', 'rb') as mykey:
    key = mykey.read()



def process_connection( conn , ip_addr, MAX_BUFFER_SIZE):  
    blk_count = 0
    f = Fernet(key)
    net_bytes = conn.recv(MAX_BUFFER_SIZE)
    dest_file = open("temp","w")  # temp file is to satisfy the syntax rule. Can ignore the file.
    while net_bytes != b'':
        if blk_count == 0: #  1st block
            usr_cmd = net_bytes[0:15].decode("utf8").rstrip()

            if cmd_GET_MENU in usr_cmd: # ask for menu
       
                try:
                    with open(default_menu, 'rb') as src_file:
                        original = src_file.read()
                    
                except:
                    print("file not found : " + default_menu)
                    sys.exit(0)

                while True:
                    # read_bytes = src_file.read(MAX_BUFFER_SIZE)
                    # if read_bytes == b'':
                    #     break
                    #hints: you may apply a scheme (hashing/encryption) to read_bytes before sending to client.
                    encrypted = f.encrypt(original)
                    conn.send(encrypted)
                    conn.send(key)
                    break
                conn.close()
                print("Processed SENDING menu") 
                return

            elif cmd_END_DAY in usr_cmd: # ask for to save end day order
                #Hints: the net_bytes after the cmd_END_DAY may be encrypted. 
               
                now = datetime.datetime.now()
                filename = default_save_base +  ip_addr + "-" + now.strftime("%Y-%m-%d_%H%M")                
                dest_file = open(filename,"wb")
                # f = Fernet(key)
                
                while True:
                    net_bytes = conn.recv(MAX_BUFFER_SIZE)
                    print(net_bytes)
                    if not net_bytes:
                        break
                    decrypted = f.decrypt(net_bytes)
                    dest_file.write(decrypted)

                
                # Hints: net_bytes may be an encrypted block of message.
                # e.g. plain_bytes = my_decrypt(net_bytes)
                dest_file.write( net_bytes[ len(cmd_END_DAY): ] ) # remove the CLOSING header    
                blk_count = blk_count + 1
        else:  # write subsequent blocks of END_DAY message block
            # Hints: net_bytes may be an encrypted block of message.
            net_bytes = conn.recv(MAX_BUFFER_SIZE)
            decrypted = f.decrypt(net_bytes)
            dest_file.write(decrypted)
    # last block / empty block
    dest_file.close()
    print("saving file as " + filename)
    time.sleep(3)
    print("Processed CLOSING done") 
    return

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    process_connection( conn, ip, MAX_BUFFER_SIZE)
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")
    return

def start_server():
    global host, port
    # Here we made a socket instance and passed it two parameters. AF_INET and SOCK_STREAM. 
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    
    try:
        soc.bind((host, port))
        print('Socket bind complete')
    except socket.error as msg:
        
        print('Bind failed. Error : ' + str(sys.exc_info()))
        print( msg.with_traceback() )
        sys.exit()

    #Start listening on socket and can accept 10 connection
    soc.listen(10)
    print('Socket now listening')

    # this will make an infinite loop needed for 
    # not reseting server for every client
    try:
        while True:
            conn, addr = soc.accept()
            # assign ip and port
            ip, port = str(addr[0]), str(addr[1])
            print('Accepting connection from ' + ip + ':' + port)
            try:
                Thread(target=client_thread, args=(conn, ip, port)).start()
            except:
                print("Terrible error!")
                traceback.print_exc()
    except:
        pass
    soc.close()
    return

start_server()  