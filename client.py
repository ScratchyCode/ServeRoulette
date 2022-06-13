import os
import sys
import socket
import hashlib
import time
import signal

ID = "2c9fef9b-ce19-450d-ac59-90f665fd17e4"

def signal_handler(signal,frame):
    print("\nExit...")
    sys.exit(0)


##############
#    main    #
##############
if(__name__ == "__main__"):
    
    # gestisco il segnale di chiusura
    signal.signal(signal.SIGINT,signal_handler)
    
    host = input("Host remoto: ")
    port = int(input("Porta: "))
    
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
    except:
        print("Errore di connessione")
        client.close()
        sys.exit(0)
    
    try:
        risposta = client.recv(2048)
        if(not risposta):
            print("Disconnesso")
            client.close()
            sys.exit(0)
        risposta = risposta.decode()
    except:
        print("Disconnessione: errore durante l'handshake")
        client.close()
        sys.exit(0)
    
    print(risposta)
    
    # invio identificativo
    try:
        client.send(str.encode(ID))
    except:
        print("Errore identificazione: server down")
        client.close()
        sys.exit(0)
    
    # risposta validazione identificativo
    try:
        risposta = client.recv(2048)
        if(not risposta):
            client.close()
            sys.exit(0)
        risposta = risposta.decode()
    except:
        print("Errore connessione")
        client.close()
        sys.exit(0)
    
    print(risposta)
    
    # aspetta a chiudere la connessione
    while(True):
        scelta = input('\nVuoi chiudere la connessione? (y/n): ')
        if(scelta == 'n' or scelta == 'N'):
        #risposta = client.recv(2048)
        #if(not risposta):
        #    break
            continue
        else:
            break
    
    client.close()

