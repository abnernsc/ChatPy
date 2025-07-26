# guest.py

import socket
import threading

# --- FUNÇÃO QUE CUIDA DO RECEBIMENTO DE MENSAGENS ---
# Esta função é praticamente IDÊNTICA à do Host.
# Ela também vai rodar em uma thread separada para não travar o programa.
def receber_mensagens(s):
    while True:
        try:
            msg = s.recv(1024).decode('utf-8')
            if not msg:
                print("Host se desconectou.")
                break
            
            print(f"\nHost: {msg}")

        except:
            print("Conexão perdida.")
            break

# --- CONFIGURAÇÃO DO CLIENTE (GUEST) ---
# O Guest precisa saber o endereço IP do Host para se conectar.
# Para testar no mesmo computador, usamos '127.0.0.1', que é um endereço especial
# que significa "este próprio computador".
HOST_IP = '127.0.0.1' 
PORT = 65432 # A MESMA porta que o Host está usando

# Cria o objeto socket do cliente
# As configurações (AF_INET, SOCK_STREAM) devem ser as mesmas do Host.
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tenta se conectar ao Host usando o IP e a Porta
cliente.connect((HOST_IP, PORT))
print("Conectado ao Host!")


# --- INICIA A THREAD DE RECEBIMENTO ---
# A lógica é a mesma do Host: cria e inicia uma thread para
# a função 'receber_mensagens', passando o socket do cliente como argumento.
thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
thread_recebimento.start()


# --- LOOP PRINCIPAL PARA ENVIAR MENSAGENS ---
# Loop principal para o Guest digitar e enviar suas mensagens.
while True:
    msg_para_enviar = input("Você: ")
    cliente.sendall(msg_para_enviar.encode('utf-8'))