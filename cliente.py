import socket
import threading
import time


cliente_IP = "127.0.0.1" 
porta = 8080

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((cliente_IP, porta))
print("Conectado ao Host!")

valid = False
print("Digita 'sair' para encerrar o chat")
while not valid:
    msgcliente = input("Você: ")
    cliente.send(str(msgcliente).encode("utf-8"))
    if msgcliente == "sair":
        print("O chat foi encerrado")
        valid = True
        break
    msg = cliente.recv(1024).decode("utf-8")
    if msg=="sair":
        print("O chat foi encerrado")
        valid = True
    else: 
        print(f"Host: {msg}")
cliente.close()
