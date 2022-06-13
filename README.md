# ServeRoulette
Per usare il programma bisogna eseguire manualmente i seguenti passi:
1) aggiungere un utente al database db.txt runnando lo script "idGen.py" che associa un ID unico ad una data di scadenza
2) copiare il file "client.py" da distribuire al nuovo utente cambiando nel sorgente l'ID creato al passo 1)
3) runnare il server
4) il nuovo client è abilitato a connettersi al server fino alla data di scadenza assegnata al punto 1)

Il file nonclient.py è un esempio di come un utente sprovvisto di ID non registrato venga rifiutato.
