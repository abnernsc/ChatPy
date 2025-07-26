# host.py

import socket
import threading

# --- FUNÇÃO QUE CUIDA DO RECEBIMENTO DE MENSAGENS ---
# Esta função vai rodar em uma thread separada (em segundo plano)
# para ficar constantemente ouvindo por novas mensagens.
def receber_mensagens(conn):
    while True:
        try:
            # Tenta receber uma mensagem do cliente (até 1024 bytes)
            msg = conn.recv(1024).decode('utf-8')
            
            # Se não receber nada (ou uma msg vazia), significa que o cliente desconectou
            if not msg:
                print("Guest se desconectou.")
                break # Sai do loop
            
            # Imprime a mensagem recebida do Guest
            print(f"\nGuest: {msg}")

        except:
            # Se der qualquer erro, assume que a conexão foi perdida
            print("Conexão perdida.")
            break

# --- CONFIGURAÇÃO DO SERVIDOR (HOST) ---
# Define o endereço IP do host. '0.0.0.0' significa que ele vai aceitar
# conexões de qualquer interface de rede do computador.
HOST = '0.0.0.0'
PORT = 65432 # Porta que será usada para a conexão

# Cria o objeto socket do servidor
# AF_INET indica que estamos usando o protocolo de endereçamento IPv4.
# SOCK_STREAM indica que estamos usando o protocolo de transporte TCP.
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o socket ao endereço e porta definidos
servidor.bind((HOST, PORT))

# Coloca o servidor em modo de escuta, aguardando por conexões
servidor.listen()

print("Aguardando conexão de um Guest...")

# Aceita uma nova conexão. O programa fica "travado" aqui até um Guest se conectar.
# 'conn' é um novo socket para a comunicação com o Guest que se conectou.
# 'addr' é o endereço (IP e porta) do Guest.
conn, addr = servidor.accept()
print(f"Conectado com {addr}")


# --- INICIA A THREAD DE RECEBIMENTO ---
# Cria uma nova thread que vai executar a função 'receber_mensagens'.
# 'args=(conn,)' passa o socket da conexão como argumento para a função.
# 'daemon=True' faz com que a thread seja encerrada quando o programa principal fechar.
thread_recebimento = threading.Thread(target=receber_mensagens, args=(conn,), daemon=True)
thread_recebimento.start()


# --- LOOP PRINCIPAL PARA ENVIAR MENSAGENS ---
# Este loop fica na thread principal, permitindo que o Host digite suas mensagens.
while True:
    msg_para_enviar = input("Você: ")
    # Envia a mensagem digitada para o Guest, codificada em UTF-8
    conn.sendall(msg_para_enviar.encode('utf-8'))