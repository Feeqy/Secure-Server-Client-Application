#------------------------------------------------------------------------------------------
# Client.py
#------------------------------------------------------------------------------------------
#!/usr/bin/env python3
# Please starts the tcp serverfirst before running this client
import cryptography
from cryptography.fernet import Fernet
import datetime
import sys              # handle system error
import socket
import time
global host, port
import hashlib




host = socket.gethostname()
port = 8888         # The port used by the server
MAX_BUFFER_SIZE = 4096
PASSWORD = "secret_password".encode() # password for authentication



cmd_GET_MENU = b"GET_MENU"
cmd_END_DAY = b"CLOSING"
menu_file = "menu.csv"
return_file = "C:/Users/Shafeeq Amirudeen/Documents/Poly 1.2/ACG/Assignment 2 Baseline v5.0 (1)/Assignment 3 Baseline v5.0/Assignment3v5/client/day_end.csv"

#################################################################################################
# File being RECEIVED from server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    
    my_socket.sendall(cmd_GET_MENU )
    data = my_socket.recv(4096)
    key = my_socket.recv(4096)
    print(key)
    f = Fernet(key)

    with open(menu_file, 'wb') as encrypted_file:
        encrypted_file.write(data)
    
    with open(menu_file, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open(menu_file, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    decrypted_file.close()
    my_socket.close()
    print('Menu today received from server')
    #print('Received', repr(data))  # for debugging use
    my_socket.close()
##############################################################################################

# File being SENT to server
key = Fernet.generate_key()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    
    my_socket.connect((host, port))
    my_socket.sendall(cmd_END_DAY)
   
    f = Fernet(key)
    try:
        out_file = open(return_file,"rb")
    except:
        print("file not found : " + return_file)
        sys.exit(0)

    file_bytes = out_file.read(1024)
    sent_bytes=b''
    while file_bytes != b'':
        # hints: need to protect the file_bytes in a way before sending out.
        encrypted_file_bytes = f.encrypt(file_bytes)
        sent_bytes+=file_bytes
        file_bytes = out_file.read(1024) # read next block from file 
        # my_socket.send(file_bytes)
        my_socket.send(encrypted_file_bytes)
        my_socket.send(key)

    out_file.close()
    my_socket.close()

print('Sale of the day sent to server')
# print('Sent', repr(sent_bytes))  # for debugging use
my_socket.close()
