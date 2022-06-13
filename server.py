import os
import sys
import socket
import threading
import hashlib
import time
from datetime import datetime, date
import signal

# lista ip connessi (oggetto globale)
iplista = []


def signal_handler(signal,frame):
    print("\nExit...")
    sys.exit(0)


def f_dizionario():
    filename = input("Filename databese utenti: ")
    
    dizionario = {}
    with open(filename,'r') as f:
        for line in f:
            key = line.split()[0]
            val = line.split()[1]
            dizionario[key] = val
    
    return dizionario


def f_scadenza(dataScadenza):
    scadenza = datetime.strptime(dataScadenza,"%d/%m/%Y").date()
    oggi = date.today()
    
    if(scadenza < oggi):
        return 0 # scaduto
    else:
        return 1 # valido


# funzione per ogni client
def threaded_client(connection,dizionario,ip):
    
    # ricezione identificativo
    try:
        connection.send(str.encode("Connesso al server..."))
        identificativo = connection.recv(2048)
        if(not identificativo):
            print("** utente disconnesso")
            connection.close()
            return
        identificativo = identificativo.decode()
    except:
        print("** disconnessione: errore in fase di handshake")
        connection.close()
        return
    
    # validazione id
    if(identificativo not in dizionario):
        connection.send(str.encode("Utente non autorizzato."))
        print("** '%s' non presente nel database" %identificativo)
        connection.close()
        print("** '%s' disconnesso" %identificativo)
        
        # rimuovo l'ip del client dalla lista
        ipindice = iplista.index(ip)
        del iplista[ipindice]
        return
    else:
        if(f_scadenza(dizionario[identificativo])):
            connection.send(str.encode("Abbonamento valido."))
            print("** '%s' utente connesso" %identificativo)
            # codice...
            
        else:
            connection.send(str.encode("Abbonamento scaduto."))
            print("** '%s' abbonamento scaduto" %identificativo)
            connection.close()
            print("** '%s' disconnesso" %identificativo)
            
            # rimuovo l'ip del client dalla lista
            ipindice = iplista.index(ip)
            del iplista[ipindice]
            return
    
    # fai qualcosa finchè client è connesso
    while(True):
        # check dati ricevuti dal client
        try:
            #dati = client.recv(2048)
            dati = connection.recv(2048)
            if(not dati):
                break
        except:
            print("** fine connessione")
            connection.close()
            break
    
    # chiusura
    connection.close()
    print("** '%s' connessione chiusa" %identificativo)
    
    # rimuovo l'ip e l'id del client dalle liste
    ipindice = iplista.index(ip)
    del iplista[ipindice]
    return


##############
#    main    #
##############
if(__name__ == "__main__"):
    # gestisco il segnale di chiusura
    signal.signal(signal.SIGINT,signal_handler)
    
    # definisco e poi riempo le entry del dizionario da file
    dizionario = f_dizionario()
    
    # per l'antibrute
    maxconnessioni = 2
    
    # SERVER: creazione socket connessioni TCP
    try:
        serverSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM) 
        host = ""
        port = int(input("Porta su cui ascoltare: "))
        threadCount = 0
    except:
        print("Errore creazione socket.")
    
    try:
        serverSocket.bind((host,port))
    except socket.error as errore:
        print(str(errore))
    
    print("* Attesa di connessioni...")
    serverSocket.listen(10)
    
    while True:
        client,address = serverSocket.accept()
        
        # check antibrute
        iplista.append(address[0])
        if(iplista.count(address[0]) >= maxconnessioni):
            client.send(str.encode("Ban anti bruteforce attivato per il tuo IP."))
            print("* Antibrute attivato per l'ip: %s" %address[0])
            client.close()
            
            # elimina gli ip duplicati derivanti da brute-> rimangono solo i veri utenti connessi
            iplista = list(set(iplista))
            #ipindice = iplista.index(ip)
            #del iplista[ipindice]
        else:
            threadCount += 1
            print("\n* Richiesta di connessione: " + str(threadCount),end='\n')
            
            # passa la connessione ad un nuovo thread
            client_handler = threading.Thread(target=threaded_client,args=(client,dizionario,address[0]))
            client_handler.daemon = True
            client_handler.start()
            #client_handler.join()
    
    serverSocket.close()


