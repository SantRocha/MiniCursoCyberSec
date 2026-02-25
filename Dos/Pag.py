from flask import Flask, request
import time

app = Flask(__name__)

TENTATIVAS_IP = {}
TENTATIVAS_USER = {}
LIMITE_FALHAS = 3

@app.route('/login/', methods=['POST', 'GET'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')
        ip = request.remote_addr

        if TENTATIVAS_IP.get(ip, 0) >= LIMITE_FALHAS:
            return 'Erro 429: Seu IP foi bloqueado por excesso de tentativas.', 429

        if TENTATIVAS_USER.get(email, 0) >= LIMITE_FALHAS:
            return 'Erro 429: Conta temporariamente bloqueada por segurança.', 429

        time.sleep(1.5)

        if email != 'admin@hermes.com' or senha != 'senha123':
            TENTATIVAS_IP[ip] = TENTATIVAS_IP.get(ip, 0) + 1
            TENTATIVAS_USER[email] = TENTATIVAS_USER.get(email, 0) + 1
            
            return 'Erro: Credenciais inválidas.', 401
            
        TENTATIVAS_IP[ip] = 0
        TENTATIVAS_USER[email] = 0
        return 'Sucesso: Bem-vindo ao painel do Hermes 2025!', 200
    
    return 'Envie um POST com email e senha para testar o login.'

if __name__ == '__main__':
    print("🚀 Servidor de testes do Hermes 2025 rodando...")
    print("Acesse: http://127.0.0.1:8000/login/")
    app.run(host='0.0.0.0', port=8000)