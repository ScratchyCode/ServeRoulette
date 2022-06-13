import uuid

print("**********************************************")
print("* Inserimento nel database di una nuova voce *")
print("**********************************************")

filename = input("Nome file database: ")
user = input("Nuovo username (mnemonico): ")
scadenza = input("Data di scadenza (gg/mm/aa): ")
identificativo = uuid.uuid4() # uuid.uuid1() li genera a partire dal mac address

print("Nuova entry generata:")
print("%s %s %s" %(identificativo,scadenza,user))

with open(filename,'a') as f:
    f.write("%s %s %s\n" %(identificativo,scadenza,user))
