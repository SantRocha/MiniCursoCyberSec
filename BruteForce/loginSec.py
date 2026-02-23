# login.py
from flask import Flask, request
import time

app = Flask(__name__)

# Dicionários em memória para a demonstração
TENTATIVAS_IP = {}
TENTATIVAS_USER = {}
LIMITE_FALHAS = 3

@app.route('/login/', methods=['POST', 'GET'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')
        ip = request.remote_addr

        # DEFESA 3: Verifica bloqueio por IP
        if TENTATIVAS_IP.get(ip, 0) >= LIMITE_FALHAS:
            return 'Erro 429: Seu IP foi bloqueado por excesso de tentativas.', 429

        # DEFESA 4: Verifica bloqueio por Usuário
        if TENTATIVAS_USER.get(email, 0) >= LIMITE_FALHAS:
            return 'Erro 429: Conta temporariamente bloqueada por segurança.', 429

        # DEFESA 1: O Tarpit (atraso)
        time.sleep(1.5)

        # Validação das credenciais do Hermes 2025
        if email != 'admin@hermes.com' or senha != 'senha123':
            # Registra a falha somando +1 tentativa
            TENTATIVAS_IP[ip] = TENTATIVAS_IP.get(ip, 0) + 1
            TENTATIVAS_USER[email] = TENTATIVAS_USER.get(email, 0) + 1
            
            # DEFESA 2: Mensagem Genérica
            return 'Erro: Credenciais inválidas.', 401
            
        # Sucesso! Reseta as tentativas de falha
        TENTATIVAS_IP[ip] = 0
        TENTATIVAS_USER[email] = 0
        return 'Sucesso: Bem-vindo ao painel do Hermes 2025!', 200
    
    return 'Envie um POST com email e senha para testar o login.'

# Este é o "motor" que inicia o servidor quando você roda o arquivo!
if __name__ == '__main__':
    print("🚀 Servidor de testes do Hermes 2025 rodando...")
    print("Acesse: http://127.0.0.1:8000/login/")
    app.run(host='0.0.0.0', port=8000)