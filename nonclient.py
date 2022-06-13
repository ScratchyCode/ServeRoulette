import socket
import hashlib
import time

ID = "stocazzo"

host = input("Host remoto: ")
port = int(input("Porta: "))

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
risposta = client.recv(2048)
risposta = risposta.decode()
print(risposta)

time.sleep(1)

# invio identificativo
client.send(str.encode(ID))

# risposta validazione identificativo
risposta = client.recv(2048)
risposta = risposta.decode()
print(risposta)

# aspetta a chiudere la connessione
while(True):
    scelta = input('\nVuoi chiudere la connessione? (y/n): ')
    if(scelta == 'n' or scelta == 'N'):
        risposta = client.recv(2048)
        if(not risposta):
            break
        continue
    else:
        break

client.close()
